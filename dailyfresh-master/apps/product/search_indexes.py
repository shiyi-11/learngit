from haystack import indexes
from apps.product.models import ProductSKU


# 根据哪个Model类创建索引，类名固定格式，model类 + Index
class ProductSKUIndex(indexes.SearchIndex, indexes.Indexable):
    # use_template指定根据哪些字段建立索引文件的说明放在一个文件中
    text = indexes.CharField(document=True, use_template=True)
    # author = indexes.CharField(model_attr='user')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return ProductSKU

    # 建立索引数据
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
        return self.get_model().objects.all()
