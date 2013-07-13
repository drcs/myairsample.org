function validateChemicalName() {
    var elem = $(this)
    $.get('api/validate/' + elem.val() , function(data) {
	if (data == "NA") {
	    if (elem.next(".warning").length == 0) {
		elem.after($("<span class='warning'> \"" + elem.val() + "\" is either misspelled, or not in the database</span>"))
	    }
	} else {
	    elem.next(".warning").remove()
	}
    });
}

$( document ).ready(function () {
    var chem_n = 4;
    $( "#add_chemicals_button" ).click(function (event) {
	var newinput = $("<input />").attr("name","chem" + chem_n).attr("tabindex", chem_n*10)
	$("#chemical_name_input").append(newinput)
	newinput.focusout(validateChemicalName)
	newinput.focus()
	$("#chemical_level_input").append($("<input />").attr("name","report" + chem_n).attr("tabindex", chem_n*10 + 1))
	chem_n = chem_n + 1;
	event.preventDefault();
    });
    
    $("a.help").click(function (event) {
	$("#help_div > div").removeClass('selected');
	$($(this).attr('href')).addClass('selected');
	event.preventDefault();
    });

    $("#chemical_name_input input").focusout(validateChemicalName)
});