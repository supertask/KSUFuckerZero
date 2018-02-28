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
$firstnames = array("真輝", "右", "健悟");
$lastnames = array("小谷", "高橋", "今江");
//$firstnames = array("健悟");
//$lastnames = array("今江");
$keywords = array("テニス", "ソフトウェア");

$manager = new SocialManager($firstnames, $lastnames, $keywords);
$manager->search();

?>

</body>
</html>
