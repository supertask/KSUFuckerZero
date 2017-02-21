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
        $(window).on('load', function() {
            $('#pictures').masonry({
                itemSelector: '.pic',
                isFitWidth: true,
                isAnimated: true
            });
            $('#pages').masonry({
                itemSelector: '.page',
                isFitWidth: true,
                isAnimated: true
            });
        });
        $(window).resize(function() {
            //for
            //Here
            console.log($(window).width().toFixed(2) % );
            console.log();
        });
    </script>

</head>
<body>

<?php
function is_correct_id() {
    if (isset($_GET["id"]) && preg_match("/([gi][0-9]+)/", $_GET["id"])) return true;
    return false;
}

if (is_correct_id()) {
    $studentID = $_GET["id"];
    include ("db_manager.php");
    try {
        $face_width = 400;
        $table = get_table_from($studentID);
        $table->execute(array($studentID));
        $table_row = $table->fetch();
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
            <h1><?php echo $lastnames[0].' '.$firstnames[0]; ?> (<?php echo $studentID; ?>)</h4>
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
                echo "<img class='pic' src='http://" . $image_path . "' />"; //style='width: 320px;'
            }
        ?>
        </div>
    </div>

    <h2>Pages</h2>
    <div id="pages">
    <?php
        foreach(array_combine($page_titles, $page_paths) as $title => $path) {
            if (empty($title)) $title = "NON TITLE";
            echo "<a class='page' href='http://" . $path . "' >" . $title . "</a>"; //style='width: 320px;'
        }
    ?>
    </div>
<?php
        }
        else {
            echo '<div class="alert alert-danger" role="alert"> <strong>Query error!</strong> No student you input in a database.</div>';
        }
    }
    Catch(PODException $e) {
        print "Error: ".$e->getMessage()."<br />";
        die();
    }
}
else {
    echo '<div class="alert alert-danger" role="alert"> <strong>Query error!</strong> Your input of student id is wrong.</div>';
}
?>



</body>
</html>
