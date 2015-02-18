function sendText(evt) {
  var f = document.getElementById("user_text");
  var checkboxes = document.getElementsByName("pos");
  var checked = [];
  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      checked.push(checkboxes[i].value);
    }
  }
  console.log(checked);
  var checkedParams = "";
  for (var i = 0; i < checked.length; i++ ) {
    checkedParams += checked[i];
  }
  var encodedChecked = encodeURIComponent(checkedParams);
  var params = "user_text=" + f.value + "&pos=" + encodedChecked;
  var req = new XMLHttpRequest();
  req.open("POST", "/result", true);
  req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  req.send(params);
  evt.preventDefault();
  req.onreadystatechange = function () {
    if (req.readyState === 4 && req.status === 200) {
      var data = JSON.parse(req.responseText);
      document.getElementById("title").innerText = "shuffled~";
      document.getElementById("content").innerText = data.shuffled;
    }
  };
}

var b = document.getElementsByTagName("button")[0];
b.addEventListener("click", sendText);
