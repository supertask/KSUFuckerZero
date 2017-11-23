<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>学生データベース コントロールパネル</title>
    <meta name = "description" content="コンピュータ理工学部の学生データベースです。コンピュータ理工学部内で作成したWEBサイトをトレースして、データベース化しています。各学年ごとの学生も検索が可能です。" />
    <meta name = "keyboard" content="コンピュータ理工学部,学生データベース,京都産業大学,WEBオーサリング,コンピュータ理工学実験,ソフトウェア工学,プロジェクト演習" />

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">
</head>

<?php
    set_time_limit(100000);
    $pypath = apache_getenv('PY_PATH');
    $cmd_line = $pypath . ' main.py ';

    if (isset($_POST['run_option'])) {
        $cmd = $_POST['run_option'];
        $cmd_line .= $cmd;
    }
?>

<body>
<div style="padding: 30px;">
    <form action="controller.php" method="post">
        <div class="row">
            <h1>Web Crawling Fucker</h1>
        </div>
        <div class="row">
            <select class="form-control col col-lg-4 mr-sm-2" name="run_option">
                <option selected value="download_all">1. 全CSE学生のページをダウンロード</option>
                <option value="upload_to_s3">2. 全CSE学生のページをS3へ保存</option>
                <option value="analyze_HTMLs">3. HTMLを解析</option>
                <option value="create_index_DB">4. インデックス化</option>
            </select>
            <button class="btn btn-primary" type="submit">実行</button>
        </div>

        <div class="row" style="margin-top:20px">
            <textarea class="form-control" rows="3" style="height:400px;"><?php
            if (isset($_POST['run_option'])) {
                if( ($fp = popen($cmd_line, "r")) ) {
                echo "Running..\n";
                while( !feof($fp) ){
                    echo fread($fp, 1024);
                    flush(); // you have to flush buffer
                }
                fclose($fp);
                $disabled = "";
                echo "Ended\n";
                }
            } ?></textarea>
         </div>
    </form>
</div>
    <script src="https://code.jquery.com/jquery-3.1.1.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
</body>
</html>

