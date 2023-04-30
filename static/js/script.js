document.addEventListener('DOMContentLoaded', function() {
  var showPasswordBtn = document.getElementById('show-password');
  var passwordField = document.getElementById('password');

  showPasswordBtn.addEventListener('click', function() {
    if (passwordField.type === 'password') {
      passwordField.type = 'text';
      showPasswordBtn.textContent = 'Hide';
    } else {
      passwordField.type = 'password';
      showPasswordBtn.textContent = 'Show';
    }
  });

  var generatePasswordBtn = document.getElementById('generate-password');
  generatePasswordBtn.addEventListener('click', function() {
    var phoneticLetters = ['alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliet', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor', 'whiskey', 'xray', 'yankee', 'zulu'];
    var firstLetter = phoneticLetters[Math.floor(Math.random() * phoneticLetters.length)];
    var secondLetter = phoneticLetters[Math.floor(Math.random() * phoneticLetters.length)];
    var digits = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
    var password = firstLetter + digits + secondLetter;
    passwordField.value = password;
    passwordField.type = 'text';
    showPasswordBtn.textContent = 'Hide';
  });
});