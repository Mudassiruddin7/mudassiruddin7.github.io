// script.js
function openModal() {
    document.getElementById('stayInTouchModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('stayInTouchModal').style.display = 'none';
}

function subscribe() {
    // Get the email input value
    var email = document.getElementById('email').value;

    // Validate the email (you can add more sophisticated validation)
    if (email !== '' && validateEmail(email)) {
        // Send the email to the PHP script using AJAX
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'subscribe.php', true);
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                alert(xhr.responseText); // You can handle the response from the server here
                closeModal(); // Close the modal after subscription
            }
        };
        xhr.send('email=' + email);
    } else {
        alert('Please enter a valid email address.');
    }
}

function validateEmail(email) {
    // Basic email validation regex
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}
