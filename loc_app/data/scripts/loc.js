$( document ).ready(function () {
    var chem_n = 4;
    $( "#add_chemicals_button" ).click(function (event) {
	$("#chemical_name_input").append($("<input />").attr("name","chem" + chem_n))
	$("#chemical_level_input").append($("<input />").attr("name","report" + chem_n))
	chem_n = chem_n + 1;
	event.preventDefault();
    });
    
    $("a.help").click(function (event) {
	$("#help_div > div").removeClass('selected');
	$($(this).attr('href')).addClass('selected');
	event.preventDefault();
    });
});