/* jshint esversion: 8 */

// Updates
let twelve = "The sleigh gets polished and cleaned, the runway shovelled from snow. Its almost Christmas - not much time to go!!";
let eleven = "Mr and Mrs Clause tour the factory and give the elves a hearty applause.";
let ten = "The reindeer practice flying formations under brightly lit Christmas decorations.";
let nine = "The Elves work hard in 12 hour shifts, testing and wrapping all Christmas gifts.";
let eight = "The Elves work and sing songs with Christmas cheer. Santa holds an important planning meeting with the Reindeer.";
let seven = "Santa checks the workshop and downloads a Christmas playlist for the big trip.";
let six = "Santa, the Elves, and Reindeer have a feast to celebrate their hard work, Candy Cane and Eggnog for everyone!";
let five = "Mrs. Clause locks away all the milk and cookies so Santa can make space for your milk and cookies.";
let four = "Santa checks the Naughty or Nice List and plans his route with Google Maps.";
let three = "The Elves wrap up the last gifts and put it in Santa’s Bag.";
let two = "Santa checks the oats and water level of the Reindeer, before the Big Delivery.";
let one = "The Elves pack up the Sleigh, and with a “HO! HO! HO!”, Santa is on his way to deliver the gifts.";
let zero = "Merry Christmas"
let checkBack = "Check back here 12 days before Christmas for updates on how Santa is preparing for Christmas";

// Set the date we're counting down to
var countDownDate = new Date("Dec 25, 2021");

  // Update the count down every 1 day
var x = setInterval(function() {

// Get today's date
var now = new Date();

// Find the distance between now and the count down date
var distance = countDownDate - now;

// Time calculations for days
var days = Math.floor(distance / (1000 * 60 * 60 * 24));

// Get the ids for displaying the number images and updates
let update = document.getElementById('update');
let digit1 = document.getElementById('digit-1');
let digit2 = document.getElementById('digit-2');
let number = document.getElementById('number');

// Display the number images 1 - 12 and updates corresponding to the days left till Christmas
switch (days) {
  case 12:
    digit1.innerHTML = `<img class="number" src="/static/images/one.png">`;
    digit2.innerHTML = `<img class="number" src="/static/images/two.png">`;
    update.innerHTML = twelve;
    break;
  case 11:
    digit1.innerHTML = `<img class="number" src="/static/images/one.png">`;
    digit2.innerHTML = `<img class="number" src="/static/images/one.png">`;
    update.innerHTML = eleven;
    break;
  case 10:
    digit1.innerHTML = `<img class="number" src="/static/images/one.png">`;
    digit2.innerHTML = `<img class="number" src="/static/images/zero.png">`;
    update.innerHTML = ten;
    break;
  case 9:
    number.innerHTML = `<img class="number" src="/static/images/nine.png">`;
    update.innerHTML = nine;
    break;
  case 8:
    number.innerHTML = `<img class="number" src="/static/images/eight.png">`;
    update.innerHTML = eight;
    break;
  case 7:
    number.innerHTML = `<img class="number" src="/static/images/seven.png">`;
    update.innerHTML = seven;
    break;
  case 6:
    number.innerHTML = `<img class="number" src="/static/images/six.png">`;
    update.innerHTML = six;
    break;
  case 5:
    number.innerHTML = `<img class="number" src="/static/images/five.png">`;
    update.innerHTML = five;
    break;
  case 4:
    number.innerHTML = `<img class="number" src="/static/images/four.png">`;
    update.innerHTML = four;
    break;
  case 3:
    number.innerHTML = `<img class="number" src="/static/images/three.png">`;
    update.innerHTML = three;
    break;
    case 2:
      number.innerHTML = `<img class="number" src="/static/images/two.png">`;
      update.innerHTML = two;
      break;
    case 1:
    number.innerHTML = `<img class="number" src="/static/images/one.png">`;
    update.innerHTML = one;
    break;
  default:
    update.innerHTML = checkBack;
    break;
}

// If the count down is finished, write Happy Christmas
if (distance <= 0) {
  clearInterval(x);
  number.innerHTML = `<img class="number" src="/static/images/zero.png">`;
  update.innerHTML = zero;
}
}, 1000);