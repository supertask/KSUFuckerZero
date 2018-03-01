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

ini_set('display_errors', 1);

include("social_manager.php");
$firstnames = array("右", "真輝", "健悟");
$lastnames = array("高橋","小谷",  "今江");
$keywords = array("テニス", "ソフトウェア");

$manager = new SocialManager($firstnames, $lastnames, $keywords);
$manager->search();

?>

</body>
</html>
