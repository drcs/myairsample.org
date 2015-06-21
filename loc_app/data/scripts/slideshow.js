
var seconds_per_slide = 4;

/*
  Slideshow program:
  (1) Decrement first 'div' child "left" from 0 to -100%
  (2) Decrement second 'div' child "left" from 100% to 0% - simultaneous with (1)
  (3) Set first 'div' child "left" to +100%
  (4) rotate first 'div' child to last position
*/

$(function() {

    setInterval(function() {
	$('#slideshow > div.slides > div:first')
	    .animate({left: '-100%'}, 1000, 'swing', function() { $(this).css("left", "100%") })
	    .next()
	    .animate({left: '0%'}, 1000)
	    .end()
	    .appendTo('#slideshow > div.slides');
    }, seconds_per_slide * 1000);

    $('#slideshow-pager > div').click(function() {
	$('#slideshow-pager > div').removeClass("selected");
	$(this).addClass("selected");
	/* FIXME now actually select the slide */
    });

});

