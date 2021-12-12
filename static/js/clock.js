// Set the date we're counting down to
var countDownDate = new Date("Dec 25, 2021 00:00:00").getTime();

  // Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  var distance = countDownDate - now;

  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24) + 1);
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the result in the element with id="demo"
  document.getElementById("clock-inner").innerHTML = days + "d " + hours + "h "
  + minutes + "m " + seconds + "s ";

  // If the count down is finished, write Happy Christmas
  if (distance <= 0) {
    clearInterval(x);
    document.getElementById("flare").innerHTML = "";
    document.getElementById("clock-inner").innerHTML = "Happy Christmas!";
  }
}, 1000);


$.fn.clock = function() {
    $(this).each(function() {
      $(this).html($(this).text().split("").map(function(v, i) {
        return '<span class="clock-' + (i % 2 == 0 ? 'gold' : 'blue') + '">' + v + '</span>';
      }).join(""));
    });
  };
  
  $(function() { 
    $('span#flare').clock();
  });