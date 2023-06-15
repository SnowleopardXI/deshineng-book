<?php
$otp=$_POST["otp"];
$code="python3 /opt/bath/check_multiple.py -o $otp";
exec($code,$array);
print_r ($array);
?>
