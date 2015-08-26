'user strict';


// This is an attempt to dynamically load more ingredient fields.
// it isn't fully functional yet, it does increment the page's form count
// but it doesn't add more forms to the screen
$('#create-recipe-form').on('click', '#add-ingredient', function(e){
	e.preventDefault();
	var forms = parseInt($('#id_form-TOTAL_FORMS').val(), 10);
	forms += 1
	$('#id_form-TOTAL_FORMS').val(forms);
});