document.getElementById('consultation-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    // Get form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const symptoms = document.getElementById('symptoms').value;
    const date = document.getElementById('date').value;

    // Show a success message
    document.getElementById('response-message').innerText = `Thank you, ${name}. Your consultation request has been submitted!`;
    
    // Clear the form
    document.getElementById('consultation-form').reset();
});
