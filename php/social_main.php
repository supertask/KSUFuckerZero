<!--<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='eng' lang='en'>-->
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>WAMP</title>
<meta name='Description' content='Website Under Construction' />
</head>
<body>

<?php

include("social_manager.php");
$firstname = "右";
$lastname = "高橋";
$keywords = array("テニス", "ソフトウェア");

$manager = new SocialManager();
$manager->search($firstname, $lastname, $keywords);

?>

</body>
</html>
