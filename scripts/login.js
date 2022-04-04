$(document).ready(function(){
    
    $("#to_register").click(function(){
        $("#login").hide();
        $("#register").show();
    });

    $("#btn_login").click(function(){
        // if account and password are correct then rederict to homepage
        alert("登入成功！")
        document.location.href="../templates/homepage.html";
    });

    $("#register").click(function(){
        alert("註冊成功！將為您跳轉至登入畫面")
        $("#register").hide();
        $("#login").show();
    });
});