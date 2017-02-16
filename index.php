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
	<link href="css/index.css" type="text/css" rel="stylesheet" />


    <!-- jQuery first, then Tether, then Bootstrap JS. -->
    <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>

    <script type="text/javascript" src="js/masonry.pkgd.min.js"></script>
    <script type="text/javascript">
        $(function(){
            $('#ksu_result').masonry({
                itemSelector: '.card',
                isFitWidth: true,
                isAnimated: true
            });
        });
    </script>
</head>
<body>

<div id="ksu_result">
<?php
$SPLIT_CHAR = ",";
$table_row = NULL;
function get_names() {
    global $SPLIT_CHAR;
    global $table_row;
    $firstnames = explode($SPLIT_CHAR, $table_row["firstnames"]);
    $lastnames = explode($SPLIT_CHAR, $table_row["lastnames"]);
    if ($firstnames[0] === "" && $lastnames[0] === "") {
        $firstnames = array("???");
        $lastnames = array("");
    }
    else if ($firstnames[0] === "") { $firstnames = array("??"); }
    else if ($lastnames[0] === "") { $lastnames = array("??"); }
    return array($firstnames, $lastnames);
}
function get_face() {
    global $SPLIT_CHAR;
    global $table_row;
    $face_paths = explode($SPLIT_CHAR, $table_row["image_links"]);
    $face_rects = explode($SPLIT_CHAR, $table_row["faceimage_position"]); #A bug
    if ($face_rects[0] === 'None' || $face_rects[0] === '') {
        return array($face_paths[0], NULL);
    }
    else {
        $face_rect = $face_rects[0];
        $face_rect = substr($face_rect, 1, strlen($face_rect)-2);
        echo "<script>console.log('". $face_rect . "');</script>";
        $face_rect = array_map('intval', explode($SPLIT_CHAR, $face_rect));
        #echo "<script>console.log('". $face_rect[0] . "');</script>";
        return array($face_paths[0], $face_rect);
    }
}
function get_face_css() {
    list($face_path, $face_rect) = get_face();
    $css_line = "";
    if (empty($face_path)) { return array("./images/no-user.gif", $css_line); }
    if ($face_rect) {
        $width = 300; /* 固定 */
        $image_size = getimagesize($face_path);
        $face_position = array($face_rect[0], $face_rect[1]);
        $face_size = array($face_rect[2], $face_rect[3]);

        $ratio = $width / (float) $face_size[0];
        $height = $face_size[1] * $ratio;
        $bg_position = array(-1 * $face_position[0] * $ratio, -1 * $face_position[1] * $ratio);
        $bg_size = array($image_size[0] * $ratio, $image_size[1] * $ratio);
        $css_line = sprintf("background-position: %dpx %dpx; background-size:%dpx %dpx; height: %dpx;", (int)$bg_position[0], (int)$bg_position[1], (int)$bg_size[0], (int)$bg_size[1], (int)$height);
    }
    return array("http://".$face_path, $css_line);
}

try {
    $dbh = new PDO("sqlite:analyze/DB/cse_student_DB.db");
    $table = $dbh->prepare("select firstnames,lastnames,studentID,page_keywords,image_links,faceimage_position from cse_students");
    $table->execute();

    while($table_row = $table->fetch())
    {
        list($firstnames, $lastnames) = get_names();
        list($image_path, $css_line) = get_face_css();
        $top_keywords = array_slice(explode($SPLIT_CHAR, $table_row["page_keywords"]), 0, 15);
        $studentID = $table_row["studentID"];
        $cse_url = "http://www.cse.kyoto-su.ac.jp/~" . $studentID . "/";
        $cc_url = "http://www.cc.kyoto-su.ac.jp/~" . $studentID . "/";
        #echo "<script>console.log('". $face_rect . "');</script>";
?>
        <div class="card">
            <?php
            if(empty($css_line)) {
                echo "<img class='picture' src='" . $image_path . "' style='width:300px;' />";
            } else {
                echo "<div class='face' style='background-image: url('".$image_path.");" . $css_line ."'></div>";
            }
            ?>
            <div class="card-block">
                <h4 class="card-title"><?php echo $lastnames[0].' '.$firstnames[0]; ?> (<?php echo $studentID; ?>)</h4>
                <div class="card-text">
                <?php
                    foreach ($top_keywords as $keyword) {
                        echo "<span class='badge badge-pill badge-primary'>" . $keyword . "</span>\n";
                    }
                ?>
                </div>
            </div>
            <div class="card-block">
                <a href="#" class="card-link">詳細</a>
                <a href="<?php echo $cse_url?>" class="card-link" target="_blank">CSEページ</a>
                <a href="<?php echo $cc_url?>" class="card-link" target="_blank">CCページ</a>
            </div>
        <!-- .card --></div>
<?php
    }
}
Catch(PODException $e) {
    print "Error: ".$e->getMessage()."<br />";
    die();
}
?>
</body>
</html>

