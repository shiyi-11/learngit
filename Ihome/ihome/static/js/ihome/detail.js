function hrefBack() {
    history.go(-1);
}

// 解析提取url中的查询字符串参数
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    // 获取详情页面要展示的房屋编号
    var queryData = decodeQuery();
    var houseId = queryData["id"];

    // 获取该房屋的详细信息
    $.get('/api/v1.0/houses/detail/'+houseId,function (res) {
        if(res.re_code=='0'){

        //                             html中script的id标签               房屋图片地址                     房屋价格
            render_template=template('house-image-tmpl',{'img_urls':res.data.house.img_urls,'price':res.data.house.price});
            console.log(render_template);
            // // 在class=swiper-container中script模板填信息
            $('.swiper-container').html(render_template);




            //               html中script的id          房屋全部信息
            house_detail=template('house-detail-tmpl',{'house':res.data.house});
            console.log(house_detail);
            // 在class=detail-con中script模板填信息
            $('.detail-con').html(house_detail);


            // 数据加载完毕后,需要设置幻灯片对象，开启幻灯片滚动
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });
            //如果不是自己发布的房源，即可预定按钮显示
            if (res.data.login_user_id != res.data.house.user_id){
                $('.book-house').show();
                // 点击跳转预定页面，这里不用请求服务器，跳转之后加载完booking.js发起js里面的请求
                $('.book-house').attr('href','/booking.html?hid='+res.data.house.hid);
            }
        }else {
            alert(res.msg);
            $('.book-house').hide();
        }
    });

});