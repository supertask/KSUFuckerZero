<?php

/**
 * Estimates a grade from an entrance year using a date.
 *
 * Example:
 *     if today -> 2016
 *     2016,2015,2014,2013 -> 1,2,3,4
*/
function get_freshman_year() {
    $freshman_year = 0;
    $today_year = intval(date("Y"));
    $today_month = intval(date("m"));
    if ($today_month < 4) { $freshman_year = $today_year - 1; }
    else { $freshman_year = $today_year; }

    return $freshman_year;
}
function get_grade($year) {
    return get_freshman_year() - $year + 1;
}
function get_year($grade) {
    return get_freshman_year() - $grade + 1;
}

for($i=0; $i<20; $i++) {
    echo $i . " " . get_year($i). "\n";
    assert(get_year(get_grade(2005+$i)) == 2005+$i);
}
echo "end\n";

?>
