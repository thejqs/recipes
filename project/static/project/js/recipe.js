'user strict';

$('#create-recipe-form').on('click', '#add-ingredient', function(e){
	e.preventDefault();
	var forms = parseInt($('#id_form-TOTAL_FORMS').val(), 10);
	forms += 1
	$('#id_form-TOTAL_FORMS').val(forms);
});