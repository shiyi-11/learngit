// js读取cookie
function getCookie(name) {
    // \\b....\\b单词边界
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    // 三元运算
    return r ? r[1] : undefined;
}

// 图片验证码id编号设置为全局变量
imageCodeId="";

// 生成图片验证码id编号
function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}



// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    //向后端发送请求：/imageCode?uuid=uuid&last_uuid=last_uuid
    imageCodeId = generateUUID();  //生成UUID
    var url='/api/v1.0/image_codes/' + imageCodeId;//+ '&last_uuid=' + last_uuid;   //拼接请求地址
    $('.image-code img').attr('src',url);  //设置img的src属性
}

function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    // 组织参数
    var params={
        "image_code_id":imageCodeId,
        "image_code":imageCode
    };
    // 发起获取短信验证码请求
    $.get('/api/v1.0/sms_codes/'+mobile, params, function (res) {
            if (res.re_code == '0'){
                $('#phonecode').attr('placeholder','验证码发送成功')
                // 验证码发送成功，设置倒计时60秒定时器
                var time=60;
                // setInterval() 方法会不停地调用函数，直到 clearInterval() 被调用或窗口被关闭。
                var timer=setInterval(function () {
                    $('.phonecode-a').html(time+'秒');
                    time-=1;
                    if (time<0){
                    // 由 setInterval() 返回的 ID 值可用作 clearInterval() 方法的参数。
                    clearInterval(timer);
                    $('.phonecode-a').html('获取验证码');
                    $('.phonecode-a').attr('onclick','sendSMSCode();')
                    }
                },1000,60) // 延时1000毫秒
            }else {
                alert(res.msg);
                $('.phonecode-a').attr('onclick','sendSMSCode();')
            }
    })
}



// 页面加载完成执行function
$(document).ready(function() {
    generateImageCode();  // 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });


    // TODO: 注册的提交(判断参数是否为空)
    $('.form-register').submit(function (event) {
        // 阻止自己默认的提交表单事件
        event.preventDefault();
        // 获取后端需要的数据，电话号，短信验证码，密码
        var phone_num = $('#mobile').val();
        var phonecode = $('#phonecode').val();
        var password= $ ('#password').val();
        var password2 = $('#password2').val();
        var regix=/^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$/;
        // 判断是否为空,校验
        if(!regix.exec(phone_num)){
            $('#mobile-err span').text('手机号错误');
            $('#mobile-err').show();
        }
        if(!phonecode) {
            $('#phone-code-err span').text('手机验证码不能为空！');
            $('#phone-code-err').show();
        }
        if(!password){
            $('#password-err span').text('密码不能为空!');
            $('#password-err').show()
        }
        //组织参数
        var params={
            "phone_num":phone_num,
            "phonecode":phonecode,
            "password":password,
            "password2":password2
        };
        var req_json = JSON.stringify(params);
        // 提交表单发起请求
        $.ajax({
            url:"/api/v1.0/users",
            type:"post",
            data:req_json,
            contentType:"application/json",
            dataType:"json",
//            headers:{"X-CSRFToken":getCookie("csrf_token")},
            success:function(response){
                if(response.re_code=='0'){
                    // 成功跳转到首页
                    alert(response.msg);
                    location.href='/'
                }else {
                    alert(response.msg)
                }
            }
        })
    });
})
