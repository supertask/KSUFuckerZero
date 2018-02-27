<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Required meta tags -->
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>京都産業大学 コンピュータ理工学部の学生データベース</title>
	<meta name = "description" content="コンピュータ理工学部の学生データベースです。コンピュータ理工学部内で作成したWEBサイトをトレースして、データベース化しています。各学年ごとの学生も検索が可能です。" />
	<meta name = "keyboard" content="コンピュータ理工学部,学生データベース,京都産業大学,WEBオーサリング,コンピュータ理工学実験,ソフトウェア工学,プロジェクト演習" />

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">
	<link href="css/student.css" type="text/css" rel="stylesheet" />


    <!-- jQuery first, then Tether, then Bootstrap JS. -->
    <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>

    <script type="text/javascript" src="js/masonry.pkgd.min.js"></script>
    <script type="text/javascript">
        function resizer(tag, start_width, end_width) {
            var min_margin = 9999;
            //var start_width = 300, end_width = 500;
            var fixed_width = 0;
            for(var i=0; i<(end_width-start_width); ++i) {
                var margin = $(window).width().toFixed(2) % (start_width + i);
                if (margin < min_margin) {
                    min_margin = margin;
                    fixed_width = start_width + i;
                }
            }
            $(tag).css("width",fixed_width);
        }
        $(window).resize(function(){ resizer("#pictures_flame #pictures img.pic",300,500); });
        //$(window).resize(function(){ resizer("#pages .page", 240,400); });

        $(window).on('load', function() {
            resizer("#pictures_flame #pictures img.pic",300,500);
            $('#pictures').masonry({
                itemSelector: '.pic',
                isFitWidth: true,
                isAnimated: true
            });
        });


        $(window).resize(function(){ resizer("#sns_pictures_flame #sns_pictures img.pic",150,250); });
        $(window).on('load', function() {
            resizer("#sns_pictures_flame #sns_pictures img.pic",150,250);
            $('#sns_pictures').masonry({
                itemSelector: '.pic',
                isFitWidth: true,
                isAnimated: true
            });
        });
    </script>

</head>
<body>


<?php
function is_correct_id() {
    if (isset($_GET["id"]) && preg_match("/([gi][0-9]+)/", $_GET["id"])) return true;
    return false;
}
function show_alert($error_name, $error_detail) {
    echo '<div class="alert alert-danger" role="alert"> <strong>' . $error_name . '</strong> ' . $error_detail . '</div>';
}

if (is_correct_id()) {
    include ("php/db_manager.php");
    $studentID = $_GET["id"];
    $table = NULL;
    $table_row = NULL;
    try {
        $table = get_student_table_in_detail(array($studentID));
        $table_row = $table->fetch();
    }
    Catch(PODException $e) { die("ReadError: ".$e->getMessage()."<br />"); }

    $cloudfront_link = "http://d3up5s9mj2aerv.cloudfront.net/";
    $face_width = 400;
    if(!empty($table_row)) {
        list($firstnames, $lastnames) = get_names();
        list($image_path, $css_line) = get_face_css($face_width);
        $top_keywords = array_slice(explode($SPLIT_CHAR, $table_row["page_keywords"]), 0, 50);
        $image_paths = explode($SPLIT_CHAR, $table_row["image_links"]);
        $page_titles = explode($SPLIT_CHAR, $table_row["page_titles"]);
        $page_paths = explode($SPLIT_CHAR, $table_row["page_paths"]);
?>

        <header class="clearfix">
            <div id="face-image" class="float-left">
                <?php
                if(empty($css_line)) {
                    echo "<img src='" . $image_path . "' style='width:" . $face_width . "px;' />";
                } else {
                    echo "<div style='background-image: url('".$image_path."); style='width:" . $face_width . "px; " . $css_line ."'></div>";
                }
                ?>
            </div>

            <div id="student-info" >
                <h1><?php echo $lastnames[0].' '.$firstnames[0]; ?> (<?php echo $studentID; ?>)</h1>
                <div id="tags">
                    <?php
                    foreach ($top_keywords as $keyword) {
                        echo "<span class='badge badge-pill badge-primary'>" . $keyword . "</span>\n";
                    }
                    ?>
                </div>
            </div>
        </header>

        <div id="pictures_flame">
            <div id="pictures">
            <?php
                $counter = 0;
                foreach ($image_paths as $image_path) {
                    if ($counter++ == 0) continue;
                    echo "<img class='pic' src='" . $cloudfront_link . $image_path . "' />"; //style='width: 320px;'
                }
            ?>
            </div>
        </div>

        <div id="pages">
        <?php
            $diff = sizeof($page_titles) - sizeof($page_paths);
            if ($diff > 0) {
                for ($i = 0; $i < $diff; ++$i) array_push($page_paths, "");
            }
            else {
                for ($i = 0; $i < -1 * $diff; ++$i) array_push($page_titles, "");
            }
            foreach(array_combine($page_titles, $page_paths) as $title => $path) {
                if (empty($title)) $title = "NON TITLE";
                echo "<button type='button' class='page btn btn-warning' formtarget='_blank' onclick=\"window.open('http://" . $path . "');\">" . $title . "</button>"; //style='width: 320px;'
            }
        ?>
        </div>

        <?php
            include("php/social_manager.php");
            $manager = new SocialManager($firstnames, $lastnames, $top_keywords);
        ?>
        <h2 style="margin-left:20px;">Related to.. (Also look at <?php echo $manager->get_facebook_searching_link(); ?>, <?php echo $manager->get_google_searching_link(); ?>)</h2>
        <div id="sns_pictures_flame">
            <div id="sns_pictures">
            <?php
                if (empty($firstnames[0]) || empty($lastnames[0])) {
                    $manager->search_on_google($top_keywords);
                }
                else {
                    //When firstname and lastname exist
                    $manager->search($firstnames[0], $lastnames[0], $top_keywords);
                }
            ?>
            </div>
        </div>
<?php
    }
    else {
        show_alert("Query error!", "No student you inputted in a database.");
    }
}
else {
    show_alert("Query error!", "You query has been invalid.");
}
?>

</body>
</html>
