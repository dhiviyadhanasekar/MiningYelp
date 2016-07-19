<?php

if ($_GET['action'] == 'getResNames') {
    fetchRestaurantNames();
}

function fetchRestaurantNames(){
    $servername = "localhost";
    $username = "root";
    $password = "sjsu123";

    $link = mysqli_connect($servername, $username, $password) or die('Could not connect: ' . mysql_error());
    mysqli_select_db($link, 'yelp_db') or die('Could not select database');

    $query = "SELECT distinct name FROM business where business_id in (select distinct business_id from bus_popular_foods)";

    $result = mysqli_query($link, $query) or die('Query failed: ' . mysqli_error($link));
    while ($line = $result->fetch_assoc()) {
            echo $line['name'].'<br>';
    }
    mysqli_free_result($result);
    mysqli_close($link);
}
?>