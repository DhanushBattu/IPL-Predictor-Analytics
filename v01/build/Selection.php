<?php
if (isset($_POST['submit'])) {
    if (isset($_POST['team1']) && isset($_POST['team2']) &&
        isset($_POST['city']) && isset($_POST['tosswin']) && isset($_POST['mlalgo'])) {
        
        $team1 = $_POST['team1'];
        $team2 = $_POST['team2'];
        $city = $_POST['city'];
        $tosswin = $_POST['tosswin'];
        $mlalgo = $_POST['mlalgo'];
        $host = "localhost";
        $dbUsername = "root";
        $dbPassword = "";
        $dbName = "ipldb";
        $conn = new mysqli($host, $dbUsername, $dbPassword, $dbName);
        if ($conn->connect_error) {
            die('Could not connect to the database.');
        }
        else {

            if($team1 == $team2)
            {
                echo '<script>alert("Same Teams selected. Prediction not possible.")</script>';
                include 'Selection.html';
            }
            // if($city == "" || $tosswin == "" || $team1 == "" || $team2 == "")
            // {

            // }
            else{

            // $Select = "SELECT email FROM register WHERE email = ? LIMIT 1";
            $Insert = "INSERT INTO iplinfodb(Team1, Team2, CityPlayed, TossWinner, Algorithm) values(?, ?, ?, ?, ?)";
            // $stmt = $conn->prepare($Select);
            // $stmt->bind_param("s", $email);
            // $stmt->execute();
            // $stmt->bind_result($resultEmail);
            // $stmt->store_result();
            // $stmt->fetch();
            // $rnum = $stmt->num_rows;
            // if ($rnum == 0) {
                //$stmt->close();
                $stmt = $conn->prepare($Insert);
                $stmt->bind_param("sssss",$team1, $team2, $city, $tosswin, $mlalgo);
                if ($stmt->execute()) {
                    // echo "New record inserted sucessfully.";
                    // $command = escapeshellcmd('cd predict && python main.py');
                    // shell_exec($command);

                    // $myfile = fopen("temp.txt", "r") or die("Unable to open file!");
                    // $result = fgets($myfile);
                    // fclose($myfile);
                    // echo $result;
                    $command = escapeshellcmd('python output.py');
                    $output = shell_exec($command);
                    echo $output;
                    // include 'output.py';

                }
                else {
                    echo $stmt->error;
                }
            // }
            // else {
            //     echo "Someone already registers using this email.";
            // }
            $stmt->close();
            $conn->close();
        }
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