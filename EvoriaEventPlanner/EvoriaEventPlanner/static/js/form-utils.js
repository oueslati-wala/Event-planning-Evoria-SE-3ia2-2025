const FormUtils = {
    setupPasswordToggle: function(input, toggleBtn) {
        if (!input || !toggleBtn) return;
        toggleBtn.addEventListener('click', () => {
            if (input.type === 'password') {
                input.type = 'text';
                toggleBtn.querySelector('.eye-icon').classList.add('show-password');
            } else {
                input.type = 'password';
                toggleBtn.querySelector('.eye-icon').classList.remove('show-password');
            }
        });
    }
};