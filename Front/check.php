<?php
$username=$_POST["user"];
$password=$_POST["pass"];
$code="python3 /opt/bath/check_single.py -u $username -p $password";
exec($code,$array);
print_r ($array);
?>
