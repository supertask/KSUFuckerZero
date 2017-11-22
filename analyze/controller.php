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

    $commands = array('download_all', 'analyze_HTMLs', 'create_index_DB');
    $disabled = ""; 
    foreach ($commands as $cmd) {
        if (isset($_POST[$cmd])) {
            $cmd_line .= $cmd;
            $disabled = "disabled"; 
        }
    }
?>

<body>
    <div class="card">
        <div class="card-block">
            <h1>Controller</h1>
            <form action="controller.php" method="post">
                <button class="btn btn-primary" name="download_all" type="submit" <?php echo $disabled ?>>
                1. 全CSE学生のページをS3へ保存 </button>
                <button class="btn btn-primary" name="analyze_HTMLs" type="submit" <?php echo $disabled ?>>
                2. HTMLを解析</button>
                <button class="btn btn-primary" name="create_index_DB" type="submit" <?php echo $disabled ?>>
                3. インデックス化</button>
                <div style="margin-top:20px">
                    <textarea class="form-control" rows="3" style="height:400px;"><?php
                        if( ($fp = popen($cmd_line, "r")) ) {
                            echo 'Running..\n';
                            while( !feof($fp) ){
                                #echo fread($fp, 1024);
                                echo fread($fp, 104);
                                flush(); // you have to flush buffer
                            }
                            echo "Ended\n";
                            fclose($fp);
                        }
                    ?></textarea>
                </div>
            </form>
        </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.1.1.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
</body>
</html>

