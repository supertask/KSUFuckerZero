<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Required meta tags always come first -->
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
                itemSelector: '.ksu_student',
                isFitWidth: true,
                isAnimated: true
            });
        });
    </script>
</head>
<body>


<div id="ksu_result">

<?php
try {
    $SPLIT_CHAR = ",";
    $dbh = new PDO("sqlite:analyze/DB/cse_student_DB.db");
    $table = $dbh->prepare("select firstnames,lastnames,studentID,page_keywords from cse_students");
    $table->execute();
    $cnt=0;

    while($table_row = $table->fetch())
    {
        $firstnames = explode($SPLIT_CHAR, $table_row["firstnames"]);
        $lastnames = explode($SPLIT_CHAR, $table_row["lastnames"]);
        if ($firstnames[0] === "" && $lastnames[0] === "") {
            $firstnames = array("???");
            $lastnames = array("");
        }
        else if ($firstnames[0] === "") { $firstnames = array("??"); }
        else if ($lastnames[0] === "") { $lastnames = array("??"); }
        $top_keywords = array_slice(explode($SPLIT_CHAR, $table_row["page_keywords"]), 0, 15);
        $studentID = $table_row["studentID"];
        $cse_url = "http://www.cse.kyoto-su.ac.jp/~" . $studentID . "/";
        $cc_url = "http://www.cc.kyoto-su.ac.jp/~" . $studentID . "/";
?>


        <div class="ksu_student">
        <div class="card">
            <!--<img class="card-img-top" src="https://u.o0bc.com/avatars/stock/_no-user-image.gif" alt="A student face">-->
            <!--<img src="images/neko.jpg" alt="A student face" />-->
            <div class="image_flame" style="background-image: url('images/b.jpg');"></div>
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
        <!-- .ksu_student --></div>


<?php
        //if (($cnt+1) % 3 == 0) { echo "<div style=\"content: '.'; display:block; visibility:hidden; clear:both; height:0; font-size:0\"></div>"; }
        $cnt++;
    }
}
Catch(PODException $e) {
    print "Error: ".$e->getMessage()."<br />";
    die();
}
?>




</body>
</html>

