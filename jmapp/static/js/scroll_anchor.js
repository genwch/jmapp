$(document).on("click", "button.anchor_btn", function (event) {
    var sectionid = this.id.replace("btn-", "#");
    $("html, body").animate(
      {
        scrollTop: $(sectionid).offset().top - $("#navbar_top").height() - 10,
      },
      800
    );
    event.preventDefault();
  });
  