// close alerts after on clicking
document.addEventListener('DOMContentLoaded', function() {
    const closeButtons = document.querySelectorAll('.custom-close');
  
    closeButtons.forEach(button => {
      button.addEventListener('click', function() {
        const alert = this.closest('.custom-alert');
        if (alert) {
          alert.classList.add('closing');
        }
      });
    });
  });


  $(document).ready(function(){
    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();
  })