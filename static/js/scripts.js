if (/\/admin/.test(window.location.pathname)) {
  document.addEventListener('DOMContentLoaded', function () {
    var passwordField = document.getElementById('password');
    passwordField.addEventListener('click', function () {
      if (passwordField.type === 'password') {
        passwordField.type = 'text';
      } else {
        passwordField.type = 'password';
      }
    });
    var generatePasswordBtn = document.getElementById('generate-password');
    generatePasswordBtn.addEventListener('click', function () {
      var phoneticLetters = ['alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliet', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor', 'whiskey', 'xray', 'yankee', 'zulu'];
      var firstLetter = phoneticLetters[Math.floor(Math.random() * phoneticLetters.length)];
      var secondLetter = phoneticLetters[Math.floor(Math.random() * phoneticLetters.length)];
      var digits = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
      var password = firstLetter + digits + secondLetter;
      passwordField.value = password;
      passwordField.type = 'text';
    });
  })
}

if (/\/games/.test(window.location.pathname)) {
  function searchTable() {
    // Get the search box element
    var input = document.getElementById("search-box");
    // Get the table element
    var table = document.getElementById("games-table");
    // Get the table rows
    var rows = table.getElementsByTagName("tr");
    // Convert the search query to lowercase
    var query = input.value.toLowerCase();
    // Loop through the table rows
    for (var i = 0; i < rows.length; i++) {
      // Get the table cells in the current row
      var cells = rows[i].getElementsByTagName("td");
      // Loop through the table cells
      for (var j = 0; j < cells.length; j++) {
        // Convert the cell value to lowercase
        var cellValue = cells[j].textContent.toLowerCase();
        // Check if the cell value contains the search query
        if (cellValue.indexOf(query) > -1) {
          // Show the row if it matches the search query
          rows[i].style.display = "";
          break;
        } else {
          // Hide the row if it doesn't match the search query
          rows[i].style.display = "none";
        }
      }
    }
  }

  function hideClaimed(value) {
    var table = document.getElementById("games-table");
    var rows = table.getElementsByTagName("tr");
    var visibleRowCounter = 0;
    for (var i = 1; i < rows.length; i++) {
      var cells = rows[i].getElementsByTagName("td");
      var redeemedCell = cells[2];
      var redeemedValue = redeemedCell.textContent.trim();
      if (redeemedValue.indexOf(value.toString()) !== -1) {
        rows[i].style.display = "none";
      } else {
        visibleRowCounter++;
        if (visibleRowCounter % 2 == 0) {
          rows[i].style.backgroundColor = "#c0c0c0";
        } else {
          rows[i].style.backgroundColor = "#f0f0f0";
        }
      }
    }
  }
}