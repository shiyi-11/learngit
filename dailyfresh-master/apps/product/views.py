from django.shortcuts import render, HttpResponse
from .models import ProductCategory, ProductBanner, PromotionPc, TypeShow
from django_redis import get_redis_connection
from django.core.cache import cache
from apps.product.models import ProductSKU
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import View



class Home(View):
    def get(self,request):
        # url传参的？sort
        sort = request.GET.get('sort')
        print(sort)

        context = cache.get('index_page_cache')
        print('有缓存')
        if context is None:
            print('没有缓存')
            types = ProductCategory.objects.all() #类型
            banners = ProductBanner.objects.all().order_by('index')# index轮播索引
            promotion = PromotionPc.objects.all().order_by('index')# index展示顺序
            # 遍历所有类型
            for type in types:
                # 每个类型的展现方式
                word_show = TypeShow.objects.filter(product_type=type, display_type=0).order_by('index')
                pic_show = TypeShow.objects.filter(product_type=type, display_type=1).order_by('index')

                pic_word_show = TypeShow.objects.filter(product_type=type).order_by('index')
                # print(word_show)
                # print(pic_word_show)
                # print(pic_show)
                # 动态添加属性
                type.word_show = word_show
                type.pic_show = pic_show

            context = {
                'types': types,
                'banners': banners,
                'promotion': promotion,
                'pic_word_show':pic_word_show,
            }
            # 设置缓存
            print('没有缓存')
            cache.set('index_page_cache', context)
        # 有缓存验证是否登陆，登陆了拼接购物车的键，获取购物车数量转给前端，没登陆直接返回前端，购物车不显示数量
        user = request.user
        if user.is_authenticated:
            cart_key = 'cart_%d' % user.id
            print(cart_key)
            con = get_redis_connection('default')
            cart_count = con.hlen(cart_key)
            context['cart_count'] = cart_count
        return render(request, 'products/home.html', context)

class Detail(View):
    def get(self, request,sku_id):
        # print('detaildetaildetaildetail')
        # types = ProductCategory.objects.all()
        try:
            product = ProductSKU.objects.get(id=sku_id,status=1)
            print(product.status)
        except ProductSKU.DoesNotExist:
            return HttpResponse('商品以下线')
        # 新商品
        new_products = ProductSKU.objects.filter(type=product.type).order_by('-update_date')[:3]
        # 获取同类型其他规格的商品
        same_spu_products = ProductSKU.objects.filter(products=product.products).exclude(id=sku_id)
        print(same_spu_products)
        context = {
            'product': product,
            # 'types': types,
            'new_products': new_products,
            'same_spu_products': same_spu_products,
        }
        user = request.user
        if user.is_authenticated:
            cart_key = 'cart_%d' % user.id
            history_key = 'history_%user' % user.id
            con = get_redis_connection('default')
            # count > 0: 从表头开始向表尾搜索，移除与VALUE相等的元素，数量为COUNT 。
            # count < 0: 从表尾开始向表头搜索，移除与VALUE相等的元素，数量为COUNT的绝对值。
            # count = 0: 移除表中所有与VALUE相等的值。在这里移除统一商品id
            con.lrem(history_key, 0, sku_id)
            con.lpush(history_key, sku_id)
            # LTRIM KEY_NAME START STOP切片[0,1,2,3,4,5]
            con.ltrim(history_key, 0, 5)
            cart_count = con.hlen(cart_key)
            context['cart_count'] = cart_count
        return render(request, 'products/detail.html', context)



class List(View):
    def get(self,request,type,page_num):
        user = request.user
        sort = request.GET.get('sort', 'default')
        try:
            page_num = int(page_num)
        except Exception:
            page_num = 1
        # types = ProductCategory.objects.all()
        # print(types)
        # 把类型的id转成类型
        current_type = ProductCategory.objects.get(id=type)
        print(current_type)
        if sort == 'price':
            skus = ProductSKU.objects.filter(type=current_type).order_by('price')
        elif sort == '-price':
            skus = ProductSKU.objects.filter(type=current_type).order_by('-price')
        elif sort == 'sales':
            skus = ProductSKU.objects.filter(type=current_type).order_by('-sales')
        else:
            skus = ProductSKU.objects.filter(type=current_type)

        # 详情页商品数量，skus的数量按5 分页
        page_manage = Paginator(skus, 5)
        print(page_manage)
        print(1111111111111)
        try:
            # page总页数的第几页
            page = page_manage.page(page_num)
            print(page)
        except EmptyPage:
            page = page_manage.page(1)

        # 新品推荐数量[:2]前面两个
        new_products = ProductSKU.objects.filter(type=current_type).order_by('-update_date')[0:3]

        # 控制页码显示页数或5页
        total_page_num = page_manage.num_pages
        if total_page_num < 5:
            show_nums = range(1, total_page_num + 1)
        # 当前页page_num
        # 显示按钮页数show_nums
        elif page_num <= 3:
            show_nums = range(1, 6)
            # 倒数页数
        elif total_page_num - page_num <= 2:
            show_nums = range(page_num - 4, total_page_num + 1)
        else:
            show_nums = range(page_num - 2, page_num + 3)
        # show_nums = range(10)
        if user.is_authenticated:
            cart_key = 'cart_%d' % user.id
            con = get_redis_connection('default')
            cart_count = con.hlen(cart_key)
        else:
            cart_count = 0
        # types为所有种类
        # current_type为当前显示种类
        # page为分页后的显示页（包含商品sku）
        context = {
            # 'types': types,
            'page': page,
            'new_products': new_products,
            'current_type': current_type,
            'sort': sort,
            'show_nums': show_nums,
            'cart_count': cart_count,
        }
        return render(request, 'products/list.html', context)

