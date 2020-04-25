function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // TODO: 在页面加载完毕向后端查询用户的信息
    $.get('/api/v1.0/users',function (res) {
        if(res.re_code=='0'){
            $('#user-avatar').attr('src',res.user.avatar_url);
            $('#user-avatar').show();
            $('#user-use-avatar').attr('src',res.user.avatar_url);
            $('#user-use-avatar').show();
            $('#user-name').val(res.user.name)
        }else if(res.re_code=='4101'){
            location.href='/'
        }else {
            alert(res.msg)
        }
    });
    // TODO: 管理上传用户头像表单的行为
    $('#form-avatar').submit(function (event) {
        // 组织表单默认提交方式，即不用html中的地址
        event.preventDefault();
        // 异步提交ajaxSubmit表单
        $(this).ajaxSubmit({
            url:'/api/v1.0/users/avatar',
            type:'post',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (res) {
                if(res.re_code=='0'){
//                    alert(res.msg);
                    showSuccessMsg();
                    $('#user-avatar').attr('src',res.avatar_url)
                    // 在装饰器上验证用户是否登陆，4101
                }else if(res.re_code=='4101'){
                    location.href='/login.html'
                }else {
                    alert(res.msg)
                }
            }
        });
    });
    //  管理用户名修改的逻辑
    $('#form-name').submit(function (event) {
         $('.error-msg').hide();
        // 删除默认提交行为
        event.preventDefault();
        //获取用户名
        var name=$('#user-name').val();
        if(!name){
            alert('用户名不能为空！');
            return;
        }
        $.ajax({
            url:'/api/v1.0/users',
            type:'put',
            data:JSON.stringify({'name':name}),
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            contentType:'application/json',
            success:function (res) {
                if(res.re_code=='0'){
                    showSuccessMsg();

                }else if(res.re_code=='4101'){
                    location.href='/login.html'
                }else {
                    $('.error-msg').show();
                }
            }
        });
    });
});

