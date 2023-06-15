
<?php
$username=$_POST["user"];
$password=$_POST["pass"];
$place=$_POST["place"];
$time=$_POST["time"];
$gender=$_POST["gender"];
$otp=$_POST["ver"];
$code="python3 /opt/bath/commit.py -u $username -p $password -g $gender -o $otp -t $time -r $place";
exec($code,$array);
print_r ($array);
?>
