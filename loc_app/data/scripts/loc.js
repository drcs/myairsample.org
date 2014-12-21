function validateChemicalName() {
    var elem = $(this)
    elem.next().next(".warning").remove()
    $.get('api/validate/' + elem.val() , function(data) {
	if (data == "NA") {
	    elem.next().after($("<span class='warning'> \"" + elem.val() + "\" is either misspelled, or not in the database</span>"))
	}
	if (data == "NS") {
	    elem.next().after($("<span class='warning'> \"" + elem.val() + "\" is a valid chemical name, but there are no standards available for it in the database</span>"))
	}
    });
}

$( document ).ready(function () {
    var chem_n = 4;
    $( "#add_chemicals_button" ).click(function (event) {
	var newinput = $("<input />").attr("name","chem" + chem_n).attr("tabindex", chem_n*10)
	$("#chemical_input div.inputs").append(newinput)
	newinput.focusout(validateChemicalName)
	newinput.focus()
	$("#chemical_input div.inputs").append($("<input />").attr("name","report" + chem_n).attr("tabindex", chem_n*10 + 1))
	chem_n = chem_n + 1;
	event.preventDefault();
    });
    
    $("a.help").click(function (event) {
	$("#help_div > div").removeClass('selected');
	$($(this).attr('href')).addClass('selected');
	event.preventDefault();
    });

    $("#chemical_input input[name*=chem]").focusout(validateChemicalName)
});

// Display a navigation bar at the top of the page when it is scrolled down
var show_middle_nav = false;

$(window).on('scroll', function() {
    var old_show_middle_nav = show_middle_nav;
    var scroll_pos_test = 50;
    show_middle_nav = (window.pageYOffset > scroll_pos_test);
    if (show_middle_nav != old_show_middle_nav) {
	if (show_middle_nav) {
	    $("#middle-nav").show();
	} else {
	    $("#middle-nav").hide();
	}
    }
});
