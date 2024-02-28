document.addEventListener("DOMContentLoaded", function() {
    const ratingForm = document.getElementById('ratingForm');
    
    ratingForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // Gather form data
        const formData = new FormData(ratingForm);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        
        // Convert data to JSON
        const jsonData = JSON.stringify(data);
        
        // Post data to server endpoint
        fetch('/catch_rating', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData
        })
        .then(response => {
            window.location.href = "/";
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
