// single image preview in browser
var loadFile = function (event) {
  var output = document.getElementById("output");
  output.src = URL.createObjectURL(event.target.files[0]);
  output.onload = function () {
    URL.revokeObjectURL(output.src); // free memory
  };
};

setTimeout(function () {
  if ($("#message").length > 0) {
    $("#message").fadeToggle();
  }
}, 2000);
