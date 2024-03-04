document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');

  loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = emailInput.value;
    const password = passwordInput.value;

    // Handle login form submission here
    // You can use AJAX or Fetch API to send a request to the server
  });

  // Handle Gmail authentication button click
  document.getElementById('gmail-auth').addEventListener('click', () => {
    // Implement Gmail authentication using OAuth or similar mechanisms
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');

  // Handle login form submission
  loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = emailInput.value;
    const password = passwordInput.value;

    // Handle login form submission here
    // You can use AJAX or Fetch API to send a request to the server
  });

  // Handle Gmail authentication button click
  document.getElementById('gmail-auth').addEventListener('click', () => {
    // Implement Gmail authentication using OAuth or similar mechanisms
  });

  // Handle signup form submission
  signupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    // Validate passwords match
    if (password !== confirmPassword) {
      alert('Passwords do not match.');
      return;
    }

    // Handle signup form submission here
    // You can use AJAX or Fetch API to send a request to the server
  });
});