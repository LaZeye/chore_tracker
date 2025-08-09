// password_change.js
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('changePasswordForm');
    form.addEventListener('submit', function (event) {
        const newPassword = document.getElementById('new_password').value.trim();
        if (!newPassword) {
            event.preventDefault();
            alert('Please enter a new password.');
        }
    });
});