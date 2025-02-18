
document.querySelector('.select-selected').addEventListener('click', function() {
    this.nextElementSibling.classList.toggle('select-hide');
    this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'block' ? 'none' : 'block';
});

document.querySelectorAll('.select-items div').forEach(item => {
    item.addEventListener('click', function() {
        const selectedValue = this.getAttribute('data-value');
        document.querySelector('.select-selected').innerHTML = this.innerHTML + ' <i class="fas fa-chevron-down"></i>';
        this.parentNode.classList.add('select-hide');
        this.parentNode.style.display = 'none';  // Hide the dropdown after selection
    });
});

// Close the dropdown if the user clicks outside of it
window.addEventListener('click', function(event) {
    if (!event.target.matches('.select-selected')) {
        const dropdowns = document.querySelectorAll('.select-items');
        dropdowns.forEach(dropdown => {
            dropdown.style.display = 'none';
        });
    }
});


function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    section.scrollIntoView({ behavior: 'smooth' });
}
    document.getElementById('contactForm').addEventListener('submit', function(event) {
        event.preventDefault(); 
        document.getElementById('contactForm').style.display = 'none';
        document.getElementById('messageBlock').style.display = 'block';
    });

// Ensure that EmailJS SDK is loaded and ready
window.onload = function() {
    if (typeof emailjs !== 'undefined') {
        // Initialize EmailJS
        emailjs.init('_2-leC1uv_CjG7jb4'); // Replace with your EmailJS Public Key

        document.getElementById('contactForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission
        
            var templateParams = {
                from_name: document.getElementById('name').value,
                reply_to: document.getElementById('email').value,
                message: document.getElementById('message').value
            };

            console.log('Template Parameters:', templateParams); // Debugging line
            // Send the email using EmailJS
            emailjs.send('service_cfxcn05', 'template_3o9d70a', templateParams)
                .then(function(response) {
                    console.log('SUCCESS!', response.status, response.text);
                    document.getElementById('successMessage').style.display = 'block';
                    document.getElementById('errorMessage').style.display = 'none';
                }, function(error) {
                    console.log('FAILED...', error);
                    document.getElementById('successMessage').style.display = 'none';
                    document.getElementById('errorMessage').style.display = 'block';
                });
        });
    } else {
        console.error("EmailJS SDK failed to load or emailjs object is not defined.");
    }
};

