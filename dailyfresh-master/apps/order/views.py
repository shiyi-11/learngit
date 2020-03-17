from django.shortcuts import render,redirect
from django.urls import reverse
from apps.product.models import ProductSKU
from django_redis import get_redis_connection
from apps.user.models import UserAddress
from django.http import JsonResponse
from apps.order.models import OrderInfo, OrderProduct
from datetime import datetime
from django.db import transaction
# from alipay import AliPay
from alipay import AliPay
from django.views.generic import View
import os
from dailyfresh import settings


# /order/commit/
class Create_order(View):
    # 事物
    @transaction.atomic
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'msg': "用户未登录"})
        # 获取选择的用户收货地址的id、付款方式和商品id列表
        addr = request.POST.get('add_id')
        pay_id = request.POST.get('pay_id')
        skus = request.POST.get('skus')
        print(skus)

        if not all([addr, pay_id, skus]):
            return JsonResponse({'res': 3, 'msg': '数据不完整'})
        # addrs = UserAddress.objects.all()

        # 验证收获地址和付款方式
        try:
            addr = UserAddress.objects.get(id=addr)
        except UserAddress.DoesNotExist:
            return JsonResponse({'res': 1, 'msg': '地址不存在'})
        pays = OrderInfo.PAY_METHOD_DIC
        if pay_id not in pays.keys():
            return JsonResponse({'res': 2, 'msg': '不提供次收货方式'})

        # 想订单信息表中添加记录
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        transition = 10
        total_count = 0
        total_price = 0

        # 设置事务保存点
        s1 = transaction.savepoint()
        try:
            # 新增订单信息
            order = OrderInfo.objects.create(order_id=order_id, pay_method=pay_id, transit_price=transition,
                                             user=user, addr=addr, product_count=total_count, product_price=total_price)
            # 想订单商品表中添加数据
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            # eval把字符串转数值
            for s_id in eval(skus):
                print(s_id)
                try:
                    # s_id = int(s_id)
                    # 悲观锁处理订单并发问题。select_for_update()锁定，用户A处理对象时用户B无法获取对象上的锁定，那么可以确保对象没有被更改。
                    p = ProductSKU.objects.select_for_update().get(id=s_id)
                except ProductSKU.DoesNotExist:
                    # 发生异常事物回滚
                    transaction.savepoint_rollback(s1)
                    return JsonResponse({'res': 4, 'msg': '商品不存在'})
                # 每个商品数量
                count = conn.hget(cart_key, s_id)
                if int(count) > p.inventory:
                    transaction.savepoint_rollback(s1)
                    return JsonResponse({'res': 6, 'msg': '库存不足'})
                # 同一单的每个商品OrderProduct对应同一个商品订单信息表order
                OrderProduct.objects.create(order_info=order, product=p, price=p.price, count=count)

                # 更新销量、库存
                p.inventory -= int(count)
                p.sales += int(count)
                p.save()

                # 累加总金额、总数量
                total_price += p.price * int(count)
                total_count += int(count)
            # 更新订单信息表中的数据
            order.product_count = total_count
            order.product_price = total_price
            order.save()
        except Exception as e:
            transaction.savepoint_rollback(s1) # 回滚


            return JsonResponse({'res': 7, 'msg': '下单失败'})
        # 下订单后清除购物车数据
        conn.hdel(cart_key, *skus)
        return JsonResponse({'res': 5, 'msg': '创建成功'})


# 点击结算跳转请求的视图函数
def payorder(request):
    if request.method == 'POST':
        user = request.user
        # 获取商品id列表skus，（所有商品id）
        skus = request.POST.getlist('sku_id')
        print(skus)
        if not skus:
            return redirect(reverse('cart:cart'))
        conn = get_redis_connection('default')
        total_product = []
        total_price = 0
        total_count = 0
        for sku in skus:
            sku = str(sku)
            s = ProductSKU.objects.get(id=sku)
            cart_id = 'cart_%d' % user.id
            # 获取购物车单个商品数量pro_count
            pro_count = conn.hget(cart_id, sku)
            pro_count = int(pro_count)
            # 单个商品总价pro_amount
            pro_amount = s.price * pro_count
            # 动态添加属性
            s.pro_count = pro_count
            s.pro_amount = pro_amount
            # 商品列表
            total_product.append(s)
            total_count += pro_count
            total_price += pro_amount
        addrs = UserAddress.objects.filter(user=user)
        transition = 10
        total_pricewithtran = transition + total_price
        context = {
            'total_product': total_product,
            'total_price': total_price,
            'total_count': total_count,
            'transition': transition,
            'total_pricewithtran': total_pricewithtran,
            'addrs': addrs,
            'skus': skus,
        }
        print('发起请求成功')
        return render(request, 'order/order.html', context)
    return redirect(reverse('cart:cart'))

# -*- coding:utf-8 -*-
#__author__ = 'zengyun'



# 生成支付链接
def orderpay(request):
    if request.method == 'POST':
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'msg': '用户未登录'})

        # 订单id
        order_id = request.POST.get('order_id')
        print(order_id)

        if not order_id:
            return JsonResponse({'res': 1, 'msg': '无效的订单号'})
        try:
            order = OrderInfo.objects.get(user=user, order_id=order_id, order_status=1, pay_method=3)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'msg': '订单不存在'})
        # 调用支付宝接口
        app_private_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem')).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem')).read()

        alipay = AliPay(
            appid="2016101800713996",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            alipay_public_key_string=alipay_public_key_string,
            # RSA 或者 RSA2
            sign_type="RSA2",
            debug=True
        )

        # 订单总价格和订单名
        total_price = order.product_price+order.transit_price
        subject = "天天生鲜{id}".format(id=order_id)

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        print('电脑网站支付')
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            # Decimal类型需要转化成字符串
            total_amount=str(total_price),
            subject=subject,
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        return JsonResponse({'res': 3, 'pay': pay_url})


# 查询订单状态状态
def checkorder(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'res': 0, 'msg': '用户未登录'})

    order_id = request.POST.get('order_id')
    if not order_id:
        return JsonResponse({'res': 1, 'msg': '无效的订单号'})
    try:
        order = OrderInfo.objects.get(user=user, order_id=order_id, order_status=1, pay_method=3)
    except OrderInfo.DoesNotExist:
        return JsonResponse({'res': 2, 'msg': '订单不存在'})
    # 调用支付宝查询接口
    # app_private_key_string = open(BASE_DIR + '\\order\\app_private_key.pem').read()
    # alipay_public_key_string = open(BASE_DIR + '\\order\\alipay_public_key.pem').read()
    app_private_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem')).read()
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem')).read()

    alipay = AliPay(
        appid="2016101800713996",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    while True:
        response = alipay.api_alipay_trade_query(order_id)
        # 返回订单支付状态
        code = response.get('code')
        if code == '10000' and response['trade_status'] == 'TRADE_SUCCESS':
            order.trance_num = response.get('trade_no')
            order.order_status = 4
            order.save()
            return JsonResponse({'res': 3, 'msg': '支付成功'})
        elif code == '40004' or (code == '10000' and response['trade_status'] == 'WAIT_BUYER_PAY'):
            # 等待支付
            continue
        else:
            return JsonResponse({'res': 4, 'msg': '支付失败'})


