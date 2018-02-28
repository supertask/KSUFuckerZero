<?php
echo apache_getenv('FB_KF_ID');
echo '<br />';
echo apache_getenv('FB_KF_SECRET');
echo '<br />';
echo apache_getenv('FB_KF_ACCESS_TOKEN'); //Expired on 04/01/2018
echo '<br />';
$app = array(
    'app_id' => apache_getenv('FB_KF_ID'),
    'app_secret' => apache_getenv('FB_KF_SECRET'),
    'default_graph_version' => 'v2.12',
    'default_access_token' =>  apache_getenv('FB_KF_ACCESS_TOKEN') //Expired on 04/01/2018
);
var_dump($app);
?>
