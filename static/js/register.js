$(function () {
    var error_name = false;
    var error_pwd = false;
    var error_confirm_pwd = false;
    var error_mail = false;
    var error_check = false;

    // blur是失去光标事件的校验
    $("#username").blur(function () {
        check_user_name();
    });

    $("#password").blur(function () {
        check_pwd();
    });

    $("#confirm_password").blur(function () {
        check_confirm_pwd();
    });

    $("#email").blur(function () {
        check_email();
    });

    // 同意协议复选框，后续拓展需要
    $("#allow").click(function () {
        if ($(this).is(':checked')) {
            error_check = false;
            $(this).siblings('span').hide();
        } else {
            error_check = true;
            $(this).siblings('span').html('请勾选同意');
            $(this).siblings('span').show();
        }
    });


    function check_user_name() {
        var len = $('#username').val().length;
        if (len < 5 || len > 12) {
            $("#username").next().html('请输入5-12个字符')
            $("#username").next().show();
            setTimeout("check_user_name()",1000)
            error_name = true;
            return;
        } else {
            $('#username').next().hide();
            error_name = false;
        }

        // 通过ajax查询用户是否被占用，此处开启一个新的路由
        var user_name = $("#username").val();
        $.getJSON('/userprofile/check_user/', {'username': user_name}, function (data) {
            // 判断data的状态，并返回相应提示
            if (data.status == 'fail') {
                $("#username").next().html(data.msg)
                $("#username").next().show();
                error_name = true;
            } else {
                // error_name = false;
                $("#username").next().html(data.msg)
                $("#username").next().show();''
            }
        });
    }

    function check_pwd() {
        var len = $("#password").val().length;
        if (len < 8 || len > 20) {
            $("#password").next().html('密码必须是8-20位字符')
            $("#password").next().show();
            $
            error_pwd = true;
        } else {
            $("#password").next().hide();
            error_pwd = false;
        }
    }

    function check_confirm_pwd() {
        var pwd_1 = $("#password").val();
        var pwd_2 = $("#confirm_password").val();

        if (pwd_1 != pwd_2) {
            $("#confirm_password").next().html('两次输入的密码不一致！')
            $("#confirm_password").next().show();
            error_confirm_pwd = true;
        } else {
            $("#confirm_password").html().hide();
            error_confirm_pwd = false;
        }
    }

    function check_email() {
        var re = /^[a-z0-9][\w\. \-]*@[a-z0-9\-]+(\. [a-z]{2,5}){1,2}$/;
        if (re.test($("#email").val())) {
            $("#email").next().hide();
            error_mail = false;
        } else {
            $("#email").next().html('你输入的邮箱格式不正确！')
            $("#email").next().show();
            error_mail = true;
        }
    }

    // 点击注册按钮校验全部字段
    $("#register_form").submit(function () {
        check_user_name();
        check_pwd();
        check_confirm_pwd();
        check_email();

        if (error_name == false && error_pwd == false && error_confirm_pwd == false) {
            return true;
        } else {
            return false;
        }
    });

});
