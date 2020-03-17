# Generated by Django 2.2.6 on 2019-12-22 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0003_auto_20191222_1921'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=True, verbose_name='删除标记')),
                ('order_id', models.CharField(max_length=100, verbose_name='订单编号')),
                ('pay_method', models.SmallIntegerField(choices=[(1, '货到付款'), (2, '微信支付'), (3, '支付宝'), (4, '银联支付')], default=3, verbose_name='支付方式')),
                ('order_status', models.SmallIntegerField(choices=[(1, '待支付'), (2, '代发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')], default=1, verbose_name='订单状态')),
                ('product_count', models.IntegerField(verbose_name='产品数量')),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='总价格')),
                ('transit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='运费')),
                ('trance_num', models.CharField(default='', max_length=100, verbose_name='支付编号')),
                ('addr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserAddress', verbose_name='地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
                'db_table': 'order_info',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=True, verbose_name='删除标记')),
                ('count', models.SmallIntegerField(default=1, verbose_name='商品数目')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('comment', models.CharField(default='', max_length=128, verbose_name='评论')),
                ('order_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.OrderInfo', verbose_name='订单信息')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductSKU', verbose_name='商品SKU')),
            ],
            options={
                'verbose_name': '商品订单',
                'verbose_name_plural': '商品订单',
                'db_table': 'product_order',
            },
        ),
    ]
