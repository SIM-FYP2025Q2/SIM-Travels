const togglePassword = document.getElementById('togglePassword');
const passwordField = document.getElementById('password');
const icon = togglePassword.querySelector('ion-icon');

togglePassword.addEventListener('click', function () {
  const isPassword = passwordField.getAttribute('type') === 'password';
  passwordField.setAttribute('type', isPassword ? 'text' : 'password');
  icon.setAttribute('name', isPassword ? 'eye-off-outline' : 'eye-outline');
});