<?php

/**
 * Estimates a grade from an entrance year using a date.
 *
 * Example:
 *     if today -> 2016
 *     2016,2015,2014,2013 -> 1,2,3,4
*/
function get_grade_name($num) {
    if($num <= 4) { return $num . "回生"; }
    else { return "OB" . ($num - 4) . "年目"; }
}


function get_freshman_year() {
    $freshman_year = 0;
    date_default_timezone_set('Asia/Tokyo');
    $today_year = intval(date("Y"));
    $today_month = intval(date("m"));
    if ($today_month < 4) { $freshman_year = $today_year - 1; }
    else { $freshman_year = $today_year; }

    return $freshman_year;
}
function get_grade($year) { return get_freshman_year() - $year + 1; }
function get_entrance_year($grade) { return get_freshman_year() - $grade + 1; }

function get_db() {
    return new PDO("sqlite:analyze/DB/cse_student_DB.db");
}

function get_table($grade_from, $grade_to, $sort_option, $search) {
    $dbh = get_db();
    $entrance_year_range = array(get_entrance_year($grade_to), get_entrance_year($grade_from));
    $sql_statement = "SELECT entrance_year,firstnames,lastnames,studentID,page_keywords,image_links,faceimage_position FROM cse_students WHERE ?<=entrance_year AND entrance_year<=?";
    #if (!empty($search)) { } //TODO(Tasuku): search function
    if ($sort_option === 0) { $sql_statement .= "ORDER BY coding_size DESC"; }
    else { $sql_statement .= ""; }
    $table = $dbh->prepare($sql_statement);
    $table->execute($entrance_year_range);

    return $table;
}

function get_table_from($exec_array) {
    $dbh = get_db();
    $table = $dbh->prepare("SELECT entrance_year,firstnames,lastnames,page_keywords,image_links,faceimage_position,page_titles,page_paths FROM cse_students WHERE studentID = ?");
    $table->execute($exec_array);
    return $table;
}

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
    $face_rects = explode($SPLIT_CHAR.$SPLIT_CHAR, $table_row["faceimage_position"]); #A bug
    if ($face_rects[0] === 'None' || $face_rects[0] === '') {
        return array($face_paths[0], NULL);
    }
    else {
        $face_rect = $face_rects[0];
        $face_rect = substr($face_rect, 1, strlen($face_rect)-2);
        $face_rect = array_map('intval', explode($SPLIT_CHAR, $face_rect));
        #echo "<script>console.log('". $face_rect . "');</script>";
        #echo "<script>console.log('". $face_rect[0] . "');</script>";
        return array($face_paths[0], $face_rect);
    }
}
function get_face_css($width) {
    list($face_path, $face_rect) = get_face();
    $css_line = "";
    if (empty($face_path)) { return array("./images/no-user.gif", $css_line); }
    if ($face_rect) {
        //$width = 300; // 固定
        //$face_path = "http://" . $face_path;
        $image_size = getimagesize($face_path); #Call a local image(SOS!!!!!!!!!!!!!!!)
        #echo "<script>console.log('". $face_path . " " . $image_size[0] . " " . $image_size[1] . " ". $image_size[2] . " " . $image_size[3] . "');</script>";
        $face_position = array($face_rect[0], $face_rect[1]);
        $face_size = array($face_rect[2], $face_rect[3]);

        $ratio = $width / (float) $face_size[0];
        $height = $face_size[1] * $ratio;
        $bg_position = array(-1 * $face_position[0] * $ratio, -1 * $face_position[1] * $ratio);
        echo "<script>console.log('". $face_path . " " . $image_size[0] . " " . $image_size[1] . " ". $image_size[2] . " " . $image_size[3] . "');</script>";

        $bg_size = array($image_size[0] * $ratio, $image_size[1] * $ratio);
        #echo "<script>console.log('". $face_path . $bg_size[0] . " " . $bg_size[1] . $bg_size[2] . $bg_size[3] . "');</script>";
        $css_line = sprintf("background-position: %dpx %dpx; background-size:%dpx %dpx; height: %dpx;", (int)$bg_position[0], (int)$bg_position[1], (int)$bg_size[0], (int)$bg_size[1], (int)$height);
        #echo "<script>console.log('". $css_line . "');</script>";
    }
    return array("http://".$face_path, $css_line);
}

function test() {
    $start_year=2000;
    for($i=0; $i<100; $i++) {
        assert(get_entrance_year(get_grade($start_year+$i)) == $start_year+$i);
    }
}
?>
