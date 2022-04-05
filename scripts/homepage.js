$(document).ready(function () {
  console.log("loaded");

  $("#btn_home").click(function () {
    $("#homepage").show();
    $("#about").hide();
    $("#backpack").hide();
  });

  $("#btn_about").click(function () {
    $("#homepage").hide();
    $("#about").show();
    $("#backpack").hide();
  });

  $("#btn_backpack").click(function () {
    $("#homepage").hide();
    $("#about").hide();
    $("#backpack").show();
  });
});
