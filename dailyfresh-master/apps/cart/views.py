from django.shortcuts import render
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.contrib.auth.decorators import login_required
from apps.product.models import ProductSKU

# 进入购物车
@login_required
def cart(request):
    print('cart')
    user = request.user
    print(user)
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % user.id
    # 获取全部购物车信息
    carts = conn.hgetall(cart_key)
    total_count = 0
    cart_products = []
    # 商品id，数量
    for sku_id, count in carts.items():
		# 结算时所有商品数量
        total_count += int(count)
        p = ProductSKU.objects.get(id=sku_id)
		# 单个商品数量
        p.count = int(count)
        p.product_total_price = float(p.price)*int(count)
        cart_products.append(p)
    return render(request, 'cart/cart.html', {'carts': cart_products, 'total_count': total_count})

# ajax添加购物车
def add_cart(request):
    print('add_cart')
    user = request.user
    if request.method == "POST":
        if not user.is_authenticated:
	        # 返回json数据到ajax函数的data参数
            return JsonResponse({'status': 0, 'msg': '您还没有登录'})
        sku_id = request.POST['sku_id']
        count = request.POST['count']
        print(sku_id, count)
        if not all([sku_id, count]):
            return JsonResponse({'status': 1, 'msg': '数据不完整'})
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'status': 2,'msg': '商品数目出错'})
        try:
            product = ProductSKU.objects.get(id=sku_id)
        except ProductSKU.DoesNotExist:
            return JsonResponse({'status': 3, 'msg': '商品不存在'})
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        try:
            # 同一商品累加数量
            db_count = conn.hget(cart_key, sku_id)
            db_count += count
        except Exception:
            db_count = count
        # cart_key, sku_id, db_count分别为redis表中购物车键，商品id，商品数量
        conn.hset(cart_key, sku_id, db_count)
        # 购买商品种数total_count
        total_count = conn.hlen(cart_key)
        return JsonResponse({'status': 5, 'msg': '添加成功', 'total_count': total_count})

# 购物车内数量增删，购物车html中的js，ajax请求
def update_cart(request):
    user = request.user
    if request.method == "POST":
        if not user.is_authenticated:
            return JsonResponse({'status': 0, 'msg': '您还没有登录'})
        sku_id = request.POST['sku_id']
        count = request.POST['count']
        print('调用update_cart')
        print(sku_id, count)
        if not all([sku_id, count]):
            return JsonResponse({'status': 1, 'msg': '数据不完整'})
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'status': 2, 'msg': '商品数目出错'})
        try:
            product = ProductSKU.objects.get(id=sku_id)
        except ProductSKU.DoesNotExist:
            return JsonResponse({'status': 3, 'msg': '商品不存在'})
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        db_count=count
        if db_count>product.inventory:
            return JsonResponse({'status': 6, 'msg': '库存不足'})
        conn.hset(cart_key, sku_id, db_count)
        num = 0
        for value in conn.hgetall(cart_key).values():
            num += int(value)
            print(value)
            print(num)
        return JsonResponse({'status': 5, 'msg': '添加成功', 'total_count': db_count,'num':num})


def delete(request):
    print('delete')
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status': 0, 'msg': '您还没有登录'})
        sku_id = request.POST['sku_id']
        if not sku_id:
            return JsonResponse({'status': 1, 'msg': '商品为空'})
        try:
            sku_id = int(sku_id)
            product = ProductSKU.objects.get(id=sku_id)
        except ProductSKU.DoesNotExist:
            return JsonResponse({'status': 2, 'msg': '商品不存在'})
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        conn.hdel(cart_key, sku_id)
        count1 = 0
        # 遍历商品数量
        for count in conn.hgetall(cart_key).values():
            count = int(count)
            count1 += count

        return JsonResponse({'status': 3, 'msg': '删除成功', 'count': count1})
