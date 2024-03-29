function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });

    //  添加登录表单提交操作
    $(".form-login").submit(function(e){
        // 阻止表单提交，执行js
        e.preventDefault();

        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        var params={
            "mobile":mobile,
            "password":passwd
        };
        $.ajax({
                    url:"/api/v1.0/sessions",
                    type:"post",
                    data:JSON.stringify(params), // 转换成json数据
                    contentType:"application/json",
//                    headers:{"X-CSRFToken":getCookie("csrf_token")},
                    success:function(response){
                        if(response.re_code=='0'){
                            // 登录成功
                            console.log('登陆成功');
                            location.href='/'
                        }else {
                            alert(response.msg)
                        }
                    }
                });
    });
});
