document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide both toasts after 3 seconds
    setTimeout(() => {
        const successToast = document.getElementById('toast-success');
        const errorToast = document.getElementById('toast-error');
        
        if (successToast) successToast.style.display = 'none';
        if (errorToast) errorToast.style.display = 'none';
    }, 3000);

    // Handle close buttons
    document.querySelectorAll('[data-dismiss-target], [onclick*="parentElement.style.display"]').forEach(button => {
        button.addEventListener('click', function() {
            this.closest('[id^="toast-"]').style.display = 'none';
        });
    });
});