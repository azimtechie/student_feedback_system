let menuicn = document.querySelector(".menuicn");
let nav = document.querySelector(".navcontainer");

menuicn.addEventListener("click", () => {
  nav.classList.toggle("navclose");
});
$(document).ready(function () {
  // add active class to student login tab and remove it from admin login tab
  $("#student-login-tab").click(function () {
    $(this).addClass("active");
    $("#admin-login-tab").removeClass("active");
  });

  // add active class to admin login tab and remove it from student login tab
  $("#admin-login-tab").click(function () {
    $(this).addClass("active");
    $("#student-login-tab").removeClass("active");
  });
});
