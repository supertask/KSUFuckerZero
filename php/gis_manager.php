<?php

require_once __DIR__ . '/vendor/autoload.php'; // change path as needed

use odannyc\GoogleImageSearch\ImageSearch;

/*
 * A Google Image Search Manager Class.
 */
class GISManager {

    public function __construct() {
    }

    public function get_photos($keyword) {
        ImageSearch::config()->apiKey(apache_getenv('GIS_KF_API_KEY'));
        ImageSearch::config()->cx(apache_getenv('GIS_KF_CX'));
        $photos = ImageSearch::search($keyword); // returns array of results
        
        return $photos['items'];
    }

    public function plot_image($keyword) {
        $items = $this->get_photos($keyword);

        foreach ($items as $key => $item) {
            $siteURL = $item['image']['contextLink'];
            $photoURL = $item['link'];
            echo "<a href='".$siteURL."' target='_blank'><img class='pic' src='".$photoURL."'/></a>";
        }
    }
}

/*
function main() {
    $manager = new GISManager();
    $manager->plot_image('テニス');
}
main();
*/
?>
