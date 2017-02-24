<?php
function get_db() {
    return new PDO("sqlite:analyze/DB/cse_student_DB.db");
}

function get_table() {
    $dbh = get_db();
    return $dbh->prepare("select firstnames,lastnames,studentID,page_keywords,image_links,faceimage_position from cse_students");
}

function get_table_from() {
    $dbh = get_db();
    return $dbh->prepare("select firstnames,lastnames,page_keywords,image_links,faceimage_position,page_titles,page_paths from cse_students where studentID = ?");
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
        $image_size = getimagesize($face_path); #Call a local image
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

?>
