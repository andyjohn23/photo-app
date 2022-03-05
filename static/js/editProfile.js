setTimeout(function () {
  if ($("#message").length > 0) {
    $("#message").fadeToggle();
  }
}, 2000);

var button = $("#submit-data");
$("form :input")
  .not(button)
  .bind("keyup change", function () {
    // get all that inputs that has changed
    var changed = $("form :input").not(button);
    // disable if none have changed - else enable if at least one has changed
    $("#submit-data").prop("disabled", !changed.length);
    document.getElementById("submit-data").style.backgroundColor = "black";
    document.getElementById("submit-data").style.cursor = "pointer";
  });
