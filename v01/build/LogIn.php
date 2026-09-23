<?php
if (isset($_POST['submit'])) {
    if (isset($_POST['username']) && isset($_POST['password'])) {
        
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
            $Select = "SELECT Username, Password FROM userinfo WHERE Username = ? and Password = ? LIMIT 1";
            $stmt = $conn->prepare($Select);
            $stmt->bind_param("ss", $username, $password);
            $stmt->execute();
            $stmt->bind_result($resultUser, $resultPassword);
            $stmt->store_result();
            $stmt->fetch();
            $rnum = $stmt->num_rows;
            if ($rnum == 0) {
                if ($stmt->execute()) {
                    // echo "New record inserted sucessfully.";
                    echo '<script>alert("Account does not exist");</script>';
                    include 'LogIn.html';
                }
                else {
                    echo $stmt->error;
                }
            }
            else {
                // echo "Someone already registers using this username.";
                include 'Dashboard.html';
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