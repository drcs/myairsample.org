
// var seconds_per_slide = 30;
var seconds_per_slide = 30000;

/*
  Slideshow program:
  (1) Decrement first 'div' child "left" from 0 to -100%
  (2) Decrement second 'div' child "left" from 100% to 0% - simultaneous with (1)
  (3) Set first 'div' child "left" to +100%
  (4) rotate first 'div' child to last position
*/

$(function() {

    setInterval(function() {
	var slide = $('#slideshow > div.slides > div:first');
	var next_slide = slide.next();

	slide.animate({left: '-100%'}, 1000, 'swing', function() { $(this).css("left", "100%") })
	    .next()
	    .animate({left: '0%'}, 1000)
	    .end()
	    .appendTo('#slideshow > div.slides');

	$('#slideshow-pager > div').removeClass("selected");
	$('#slideshow-pager > div[_slide_no=' + next_slide.attr('_slide_no') + ']').addClass("selected");
    }, seconds_per_slide * 1000);

    var slide_no = 1;

    $('#slideshow > div.slides > div').each(function() {
	var pager_element = $('<div />').addClass('synthetic').attr('_slide_no', slide_no);
	$(this).attr('_slide_no', slide_no);
	$('#slideshow-pager').append(pager_element);
	slide_no++;
    });

    $('#slideshow-pager > div:first').addClass("selected");

    $('#slideshow-pager > div').click(function() {
	$('#slideshow-pager > div').removeClass("selected");
	$(this).addClass("selected");
	var slide_no = $(this).attr('_slide_no');

	$('#slideshow > div.slides > div').each(function() {
	    if ($(this).attr('_slide_no') == slide_no) {
		return false;
	    }

	    $('#slideshow > div.slides > div:first')
		.next()
		.css({left: '0%'})
		.end()
		.css({left: '100%'})
		.appendTo('#slideshow > div.slides');

	});


    });


});

