<?php
// Check if the email parameter is set in the POST request
if (isset($_POST['email'])) {
    $email = $_POST['email'];

    // You can save the email to a file or a database
    $file = 'subscribers.txt';

    // Append the email to the file
    file_put_contents($file, $email . PHP_EOL, FILE_APPEND);

    // Return a success message (you can customize this)
    echo 'Subscription successful. Thank you!';
} else {
    // Return an error message if the email parameter is not set
    echo 'Error: Email parameter is missing.';
}
?>
