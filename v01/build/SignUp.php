<?php
if (isset($_POST['submit'])) {
    if (isset($_POST['name']) && isset($_POST['email']) &&
        isset($_POST['gender']) && isset($_POST['phno']) &&
        isset($_POST['username']) && isset($_POST['password'])) {
        
        $name = $_POST['name'];
        $email = $_POST['email'];
        $gender = $_POST['gender'];
        $phno = $_POST['phno'];
        $username = $_POST['username'];
        $password = $_POST['password'];
        $host = "localhost";
        $dbUsername = "root";
        $dbPassword = "";
        $dbName = "ipldb";
        $conn = new mysqli($host, $dbUsername, $dbPassword, $dbName);
        if ($conn->connect_error) {
            die('Could not connect to the database.');
        }
        else {
            $Select = "SELECT EmailId FROM userinfo WHERE EmailId = ? LIMIT 1";
            $Insert = "INSERT INTO userinfo(Name, EmailId, PhoneNumber, Username, Password, Gender) values(?, ?, ?, ?, ?, ?)";
            $stmt = $conn->prepare($Select);
            $stmt->bind_param("s", $email);
            $stmt->execute();
            $stmt->bind_result($resultEmail);
            $stmt->store_result();
            $stmt->fetch();
            $rnum = $stmt->num_rows;
            if ($rnum == 0) {
                $stmt->close();
                $stmt = $conn->prepare($Insert);
                $stmt->bind_param("ssisss",$name, $email, $phno, $username, $password, $gender);
                if ($stmt->execute()) {
                    // echo "New record inserted sucessfully.";
                    // $to      = $email;
                    // $subject = 'Welcome to IPL Predictor';
                    // $message = 'Welcome to the IPL Predictor machine. We hope you enjoy it. Hope you get the right predictions';
                    // $headers = 'From: varunthegreat95@gmail.com'       . "\r\n" .
                    //              'Reply-To: varunb.working@gmail.com' . "\r\n" .
                    //              'X-Mailer: PHP/' . phpversion();
                
                    // mail($to, $subject, $message, $headers);
                    include 'LogIn.html';
                }
                else {
                    echo $stmt->error;
                }
            }
            else {
                echo '<script>alert("Someone already registers using this email.")</script>';
                // echo "Someone already registers using this email.";
                include 'SignUp.html';
            }
            $stmt->close();
            $conn->close();
        }
    }
    else {
        echo "All field are required.";
        die();
    }
}
else {
    echo "Submit button is not set";
}
?>