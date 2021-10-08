$(function () {
    var error_name = false;
    var error_pwd = false;


    // blur是失去光标事件的校验
    $("#username").blur(function () {
        check_user_name();
    });

    $("#password").blur(function () {
        check_pwd();
    });


    function check_user_name() {
        var len = $("#username").val().length;
        if (len < 5 || len > 12) {
            $("#username").next().html('请输入5-12个字符的用户名')
            $("#username").next().show();
            setTimeout(function () {
                $("#username").html('')
            },1000
            )
            error_name = true;

            return;
        } else {
            $('#username').next().hide();
            error_name = false;
        }

    }

    function check_pwd() {
        var len = $("#password").val().length;
        if (len < 8 || len > 20) {
            $("#password").next().html('密码必须是8-20位字符')
            $("#password").next().show();
            error_pwd = true;
        } else {
            $("#password").next().hide();
            error_pwd = false;
        }
    }


    // 点击登录按钮校验全部字段
    $("#login_form").submit(function () {
        check_user_name();
        check_pwd();

        if (error_name == false && error_pwd == false) {
            return true;
        } else {
            return false;
        }
    });


});
