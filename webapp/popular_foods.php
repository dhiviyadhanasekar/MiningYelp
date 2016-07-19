<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>Popular Foods</title>
  <script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.12.2.min.js"></script>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
  <link rel="stylesheet" href="https://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
  <script src="https://code.jquery.com/ui/1.11.4/jquery-ui.min.js"></script>
  <script src="https://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
  <!-- <link rel="stylesheet" href="/resources/demos/style.css"> -->

<script>
  var availableTags = [];
  var searchTableMinHeight = 0;
  $(function() {
    $('#searchResult').css({'min-height': $(window).height() - ($('.top_part').offset().top + $('.top_part').height() + 150)});
    $.ajax({
    type: "GET",
    url: "./onLoad.php",
    data: {action: 'getResNames'},
    success: function(result){
        console.log('result res names - done fetching');
        // $('#searchResult').empty();
        // $('#searchResult').append(result)
        availableTags = result.split('<br>');
        $( "#res_dropdown" ).autocomplete({
          source: availableTags
        });

    }, error: function(result){
        console.error('fetch restaurant names Error', result);
      }
    });
   
  });

var onSearch  = function(){

  $('#error_msg').text('');

  var resName = $.trim($('#res_dropdown').val());
  var found = $.inArray(resName, availableTags);

  if(found < 0 || resName.length == 0) {
    $('#error_msg').text('Error: Choose a restaurant from dropdown');
    return;
  }
  console.debug('resName', resName);
  $.ajax({
    type: "GET",
    url: "search.php",
    data: {action: 'search', restaurantName:resName},
    success: function(result){
        // console.log('result', result);
        $('#searchResult').empty();
        $('#searchResult').append(result);
    }, error: function(result){
        console.error('onSearch Error', result);
    }
  });
}
</script>
</head>
<body style='margin-left: 40px;margin-right: 40px;'>
<br/>
<div class="breadcrumb" style="font-size: 25px;">Popular food at...</div>
<div class="text-left container top_part">
  <div class="col-lg-6">
    <div class="input-group">
      <input type="text" class="form-control" placeholder="Search for restaurant..." id="res_dropdown">
      <span class="input-group-btn">
        <button class="btn btn-default" type="button" onClick="onSearch()">Go!</button>
      </span>
    </div><!-- /input-group -->
  </div><!-- /.col-lg-6 -->
  <br>
  <div id='error_msg' style="color:red; font-size: 12px"></div>
</div>
<br/>
<div id='searchResult' class='text-left container'></div>
</body>
<footer style="margin-bottom: 30px" class="text-center container">
  Build by Dhiviya Dhanasekar, XML & Web Intelligence (Teng Moh), SJSU 
</footer>
</html>


