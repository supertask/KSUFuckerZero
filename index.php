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
    <!--
    <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>
    -->
    <script src="https://code.jquery.com/jquery-3.1.1.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>

    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
	<link href="css/searcher.css" type="text/css" rel="stylesheet" />
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <script type="text/javascript" src="js/slider_setting.js"></script>

    <script type="text/javascript" src="js/masonry.pkgd.min.js"></script>
    <script type="text/javascript" src="js/grid_setting.js"></script>
</head>

<?php
    $query_search = isset($_GET['search']) ? $_GET['search'] : ""; //search query
    $query_sort_option = isset($_GET['sort-option']) ? intval($_GET['sort-option']) : 0; //HTML size sorting
    $query_grade_from = isset($_GET['grade-from']) ? intval($_GET['grade-from']) : 3; //sophomore
    $query_grade_to = isset($_GET['grade-to']) ? intval($_GET['grade-to']) : 6; //senior
    /*
    echo $query_search . "\n";
    echo $query_sort_option . "\n";
    echo $query_grade_from . "\n";
    echo $query_grade_to . "\n";
    */
?>

<body style="background-color: #F8F8F8;">
<header>
    <form method="GET">
        <h1 id="brand">KSU Fucker</h1>
        <div class="row">
            <input class="form-control col col-lg-5 mr-sm-2" type="text" name="search" placeholder="（顔、g1XXXXXXなど）" value="<?php echo $query_search; ?>">
            <select class="form-control col col-lg-2 mr-sm-2" name="sort-option">
                <?php
                    $sorts = array("HTMLサイズ順","名簿順");
                    for ($i=0; $i < sizeof($sorts); $i++)
                    {
                        if($i === $query_sort_option) {
                            echo "<option selected value=\"" . strval($i) . "\">" . $sorts[$i] . "</option>";
                        }
                        else {
                            echo "<option value=\"" . strval($i) . "\">" . $sorts[$i] . "</option>";
                        }
                    }
                ?>
            </select>
            <button class="btn btn-warning" type="submit">検索</button>
        </div>
        <div id="slider-range">
            <div id="custom-handle-left" class="ui-slider-handle"> </div>
            <div id="custom-handle-right" class="ui-slider-handle"></div>
            <input type="hidden" id="grade-from" name="grade-from" value="<?php echo $query_grade_from; ?>" />
            <input type="hidden" id="grade-to" name="grade-to" value="<?php echo $query_grade_to; ?>" />
        </div>
   </form>
</header>


<div id="ksu_result">
<?php
include ("lib/db_manager.php");
$table = NULL;
$table_row = NULL;

try { $table = get_students_table($query_grade_from, $query_grade_to, $query_sort_option, $query_search); }
Catch(PODException $e) { die("ReadError: ".$e->getMessage()."<br />"); }

try { $table_row = $table->fetch(); }
Catch(PODException $e) { die("FetchError: ".$e->getMessage()."<br />"); }


while($table_row)
{
    $face_width = 300;
    list($firstnames, $lastnames) = get_names();
    list($image_path, $css_line) = get_face_css($face_width);
    $top_keywords = array_slice(explode($SPLIT_CHAR, $table_row["page_keywords"]), 0, 15);
    $entrance_year = $table_row["entrance_year"];
    $studentID = $table_row["studentID"];
    $cse_url = "http://www.cse.kyoto-su.ac.jp/~" . $studentID . "/";
    $cc_url = "http://www.cc.kyoto-su.ac.jp/~" . $studentID . "/";
    #echo "<script>console.log('". $face_rect . "');</script>";
?>
    <div class="card" style="width: <?php echo $face_width; ?>px; ">
        <?php
        if(empty($css_line)) {
            echo "<img src='" . $image_path . "' style='width:" . $face_width . "px;' />";
        } else {
            echo "<div style='background-image: url(\"".$image_path."\"); width:" . $face_width . "px; " . $css_line ."'></div>";
        }
        ?>
        <div class="card-block">
            <h3 class="card-title" style="font-size: 22px;"><?php echo $lastnames[0].' '.$firstnames[0]; ?>（<?php echo get_grade_name(get_grade(intval($entrance_year))); ?>）</h3>
            <div class="card-text">
            <?php
                foreach ($top_keywords as $keyword) {
                    echo "<span class='badge badge-pill badge-primary'>" . $keyword . "</span>\n";
                }
            ?>
            </div>
        </div>
        <div class="card-block">
            <a href="student.php?id=<?php echo $studentID; ?>" class="card-link">詳細</a>
            <!--
            <a href="<?php echo $cse_url; ?>" class="card-link" target="_blank">CSEページ</a>
            <a href="<?php echo $cc_url; ?>" class="card-link" target="_blank">CCページ</a>
            -->
        </div>
    <!-- .card --></div>
<?php
    try { $table_row = $table->fetch(); }
    Catch(PODException $e) { die("FetchError: ".$e->getMessage()."<br />"); }
}
?>
</body>
</html>

