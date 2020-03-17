from apps.product.models import ProductSKU
from django.shortcuts import HttpResponse

# Create your views here.
def test(request):
    lst = []
    # ress = ProductSKU.objects.filter(desc='特价').order_by('-id')
    ress = ProductSKU.objects.filter(desc__endswith='产')
    for res in ress:
        lst.append(res)
        lst.append('**')
    ress = ProductSKU.objects.filter(type_id=5).exclude(id=4)
    for res in ress:
        lst.append(res)
        lst.append('**')
#
#
#     return HttpResponse(lst)

# __exact 精确等于 like ‘aaa’ __iexact 精确等于 忽略大小写 ilike ‘aaa’
# __contains 包含 like ‘%aaa%’ __icontains 包含 忽略大小写 ilike ‘%aaa%’，但是对于sqlite来说，contains的作用效果等同于icontains。
# __gt 大于
# __gte 大于等于
# __lt 小于
# __lte 小于等于
# __in 存在于一个list范围内
# __startswith 以…开头
# __istartswith 以…开头 忽略大小写
# __endswith 以…结尾
# __iendswith 以…结尾，忽略大小写
# __range 在…范围内
# __year 日期字段的年份
# __month 日期字段的月份
# __day 日期字段的日
# __isnull=True/False

# Person.objects.all()[:10]
# 切片操作，前10条
# Person.objects.all()[-10:]
# 会报错！！！
#

# QuerySet 不支持负索引
#
# Person.objects.all()[:10] 切片操作，前10条
# Person.objects.all()[-10:] 会报错！！！
# # 1. 使用 reverse() 解决
# Person.objects.all().reverse()[:2]  # 最后两条
# Person.objects.all().reverse()[0]  # 最后一条
#


# # 2. 使用 order_by，在栏目名（column name）前加一个负号
# Author.objects.order_by('-id')[:20]  # id最大的20条

# 去重方法
# qs = qs.distinct()



























