function validateChemicalName() {
    var elem = $(this)
    $.get('api/validate/' + elem.val() , function(data) {
	if (data == "NA") {
	    if (elem.next().next(".warning").length == 0) {
		elem.next().after($("<span class='warning'> \"" + elem.val() + "\" is either misspelled, or not in the database</span>"))
	    }
	} else if (data == "NS") {
	    if (elem.next().next(".warning").length == 0) {
		elem.next().after($("<span class='warning'> \"" + elem.val() + "\" is a valid chemical name, but there are no standards available for it in the database</span>"))
	    }
	} else {
	    elem.next().next(".warning").remove()
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