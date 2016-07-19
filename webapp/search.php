<?php

if ($_GET['action'] == 'search') {
  fetchFoodNames($_GET['restaurantName']);
}


function fetchFoodNames($restaurantName){
$servername = "localhost";
$username = "root";
$password = "sjsu123";

if($restaurantName == '') {
  $restaurantName = "Mr Hoagie";
}
// MySQLdb.connect("localhost","root","sjsu123", "yelp_db")
// Connecting, selecting database
$link = mysqli_connect($servername, $username, $password)
    or die('Could not connect: ' . mysql_error());
// echo 'Connected successfully';
mysqli_select_db($link, 'yelp_db') or die('Could not select database');

// Performing SQL query
// $query = "SELECT food_name, score FROM bus_popular_foods where business_id in (select business_id from business where name='" . mysqli_real_escape_string($link, $restaurantName) ."') and no_display <> 1 order by score desc, CHAR_LENGTH(food_name) desc limit 10";
$query = "SELECT food_name, score FROM bus_popular_foods where business_id in (select business_id from business where name='" . mysqli_real_escape_string($link, $restaurantName) ."') and no_display <> 1 order by CHAR_LENGTH(food_name) desc, score desc limit 10";
// echo $query;
$result = mysqli_query($link, $query) or die('Query failed: ' . mysqli_error($link));

// Printing results in HTML
echo "<table class='table table-hover ' style='width:auto;margin-left: 20px;'>\n";
echo "\t<tr class='row'>\n<th style='width:auto;'>Food</th>\n\t\t<th style='width:auto;'>Score</th>\n\t</tr>\n";
while ($line = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
    echo "\t<tr class='row'>\n";
    foreach ($line as $col_value) {
        echo "\t\t<td class='text-capitalize' style='width:auto;'>$col_value</td>\n";
    }
    echo "\t</tr>\n";
}
echo "</table>\n";

// Free resultset
mysqli_free_result($result);

// Closing connection
mysqli_close($link);
}
?>