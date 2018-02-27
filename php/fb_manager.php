<?php
require_once __DIR__ . '/vendor/autoload.php'; // change path as needed

/*
 * A Facebook API Manager Class
 */
class FBManager {
    private $fb;
    const MAX_NUM_OF_PICTURE = 5;

    public function __construct() {
        $this->fb = new Facebook\Facebook([
            'app_id' => apache_getenv('FB_KF_ID'),
            'app_secret' => apache_getenv('FB_KF_SECRET'),
            'default_graph_version' => 'v2.12',
            'default_access_token' =>  apache_getenv('FB_KF_ACCESS_TOKEN') //Expired on 04/01/2018
        ]);
    }

    private function get_users_from($name) {
        try {
            // Get the \Facebook\GraphNodes\GraphUser object for the current user.
            // If you provided a 'default_access_token', the '{access-token}' is optional.
            $response = $this->fb->get('/search?locale=ja_JP&q=' . $name . '&type=user');
            $userList = $response->getGraphEdge()->asArray();
        }
        catch(\Facebook\Exceptions\FacebookResponseException $e) {
            // When Graph returns an error
            echo 'Graph returned an error: ' . $e->getMessage();
            exit;
        }
        catch(\Facebook\Exceptions\FacebookSDKException $e) {
            // When validation fails or other local issues
            echo 'Facebook SDK returned an error: ' . $e->getMessage();
            exit;
        }
        return $userList; 
    }

    public function get_user_photos($name) {
        $userList = $this->get_users_from($name);

        $batch = array();
        $ids = array();
        foreach ($userList as $index => $user) {
            if ($index >= FBManager::MAX_NUM_OF_PICTURE)
                break;
            $request = $this->fb->request('GET', '/'.$user['id'].'/picture?redirect=false&height=150&width=150');
            array_push($batch, $request);
            array_push($ids, $user['id']);
        }

        try {
            $responses = $this->fb->sendBatchRequest($batch);
        }
        catch(\Facebook\Exceptions\FacebookResponseException $e) {
            echo 'Graph returned an error: ' . $e->getMessage();
            exit;
        } catch(\Facebook\Exceptions\FacebookSDKException $e) {
            echo 'Facebook SDK returned an error: ' . $e->getMessage();
            exit;
        }

        foreach($responses as $index => $response) {
            $picture = $response->getGraphUser();
            //echo $index . '<br />';
            //echo $picture['url'] . '<br />';
            //echo $response->isError() . '<br />';
            if ($response->isError()) {
                return array(null, null);
            }
            else {
                //echo $picture['url'] . '<br />';
                //echo $response->isError() . '<br />';
            }
        }

        return array($ids, $responses);
    }

    public function plot_image($id, $pictureURL) {
        echo "<a href='http://facebook.com/".$id."' target='_blank'><img class='pic' src='".$pictureURL."'/></a>";
    }
}

/*
function main() {
    $manager = new FBManager();
    $manager->showCandidates("高橋右");

    $firstname = "右";
    $lastname = "高橋";
    $keywords = array("テニス", "ソフトウェア");


    plotSNSPhotos($lastname, $lastname, $keywords);
}
main();
*/
?>
