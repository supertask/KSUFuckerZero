<?php

include ("fb_manager.php");
include ("gis_manager.php");


/*
 * A Facebook API and Google Image Search API Manager Class
 */
class SocialManager {
    private $fbManager;
    private $gisManager;

    private $firstnames;
    private $lastnames;
    private $keywords;

    private $google_searching_link;
    private $facebook_searching_link;

    public function __construct($firstnames, $lastnames, $keywords) {
        $this->fbManager = new FBManager();
        $this->gisManager = new GISManager();

        for($i = 0; $i < count($firstnames); $i++) {
            $firstnames[$i] = str_replace('?', '', $firstnames[$i]);
        }
        for($i = 0; $i < count($lastnames); $i++) {
            $lastnames[$i] = str_replace('?', '', $lastnames[$i]);
        }
        $this->firstnames = $firstnames;
        $this->lastnames = $lastnames;
        $this->keywords = $keywords;
        $this->check_arguments();

        if (empty($this->firstnames[0]) || empty($this->lastnames[0])) {
            $this->google_searching_link = '<a href="https://www.google.co.jp/search?q=' . $thsi->keywords[0] . '" target = "_blank">Google</a>';
            $this->facebook_searching_link ='FB'; 
        }
        else {
            $this->google_searching_link = '<a href="https://www.google.co.jp/search?q=' . $this->lastnames[0] . $this->firstnames[0] . '" target = "_blank">Google</a>';
            $this->facebook_searching_link = '<a href="https://www.facebook.com/search/top/?q=' . $this->lastnames[0] . $this->firstnames[0] . '" target = "_blank">FB</a>';
        }
    }

    public function check_arguments() {
        if (empty($this->keywords)) exit;
        foreach($this->keywords as $keyword) {
            if (empty($keyword)) exit;
        }
    }

    public function get_facebook_searching_link() { return $this->facebook_searching_link; }
    public function get_google_searching_link() { return $this->google_searching_link; }

    /*
     * Searches photos using Facebook API.
     */
    private function search_on_facebook($ids, $responses) {
        //echo 'FB search: <br />';
        foreach ($responses as $index => $response) {
            $picture = $response->getGraphUser();
            //echo 'id=' . $ids[$index] . ', url=' . $picture['url'] . '<br />';

            //良好until here
            $this->fbManager->plot_image($ids[$index], $picture['url']);
        }
    }

    /*
     * Searches photos using Google Image Search API.
     */
    public function search_on_google() {
        //echo 'Google search: <br />';
        $this->gisManager->plot_image($this->keywords[0]);
    }

    /*
     * Searches photos using Facebook API and Google Image Search API
     * on some situations. We use Facebook API if the name exists.
     * If it's not, we use Google Image Search API instead.
     */
    public function search() {
        $name = $this->lastnames[0] . $this->firstnames[0]; //because this is for only Japanese
        list($ids, $responses) = $this->fbManager->get_user_photos($name);

        if (is_null($responses)) {
            //No response
            //Put Google searching results
            $this->search_on_google(); 
        }
        else {
            $this->search_on_facebook($ids, $responses);
        }
    }
}

/*
function main() {
    SocialManager();
}
main();
*/
?>
