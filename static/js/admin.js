function Deleting_pic( pic_id ){
	var p = $('#'+pic_id);
	var link = p.attr('data-id');
	name = link.split('/')[1];
	id = link.split('/')[0];
	var url = '/restricted/admin_del_pic/';
	$.post( '/restricted/admin_del_pic/', {
		'csrfmiddlewaretoken': csrf_token,
		'id': id,
		'name': name 
	}).done(function( data ) {
		p.parent().remove();
	});
}

function admin_get_pic(){
	document.getElementById("images").innerHTML = "";
	$.getJSON("/restricted/admin_get_pic/", {
			"csrftoken": csrf_token,
			"id": global_id,
	}).done(function( data ) {
		var way = MEDIA_URL;
		var id = 0;
		$.each(data, function(i,item){
			id = id + 1;
			var images = document.getElementById("images");
			images.innerHTML = images.innerHTML + "<div class=\"img-wrap\">" +
				"<a href='javascript:Deleting_pic(" + id + ")'" +
				"<span class=\"close\">&times;</span></a>" +
				"<img id='" + id + "' src='" + way + item + "' data-id='" + item + "'>" + 
				"</div>";
				document.getElementById(id).onclick = function() { 
					
				}
		});
	}); 
}

function progressHandlingFunction(e){
	if(e.lengthComputable){
		$('progress').attr({value:e.loaded,max:e.total});
	}
}
            
$(document).ready(function(){
	$("#refresh").click(function(){
		admin_get_pic();
	})
	
	$("#preview").click(function(){
		var formData = new FormData($('form')[0]);
		formData.append('pic_url', document.getElementById("pic_url").value);
		formData.append('new_type', document.querySelector('input[name="new_type"]:checked').value);
		formData.append('name', document.getElementById("name").value);
		formData.append('info', CKEDITOR.instances.info.getData());
		formData.append('lid', CKEDITOR.instances.lid.getData());
		formData.append('html', CKEDITOR.instances.html.getData());
		formData.append('authors', $('#authors').val());
		formData.append('id', document.getElementById("id").value);
		$.ajax({
			url: '/restricted/preview/',
			type: 'POST',
			data: formData,
			success: function(responseData, textStatus, jqXHR) {
				var params = "menubar=no,location=no,resizable=yes,scrollbars=yes,status=yes";
				myWindow = window.open("");
				myWindow.document.write(responseData);
			},
			cache: false,
			contentType: false,
			processData: false
		});
	});
	
	$('#upload').click(function(){
		this.disabled=true; this.value='Please Wait...';
		var formData = new FormData($('form')[1]);
		formData.append("id", global_id);
		formData.append("csrftoken", csrf_token);
		$.ajax({
			url: '/restricted/admin_post_pic/',  //Server script to process data
			type: 'POST',
			xhr: function() {  // Custom XMLHttpRequest
				var myXhr = $.ajaxSettings.xhr();
				if(myXhr.upload){ // Check if upload property exists
					myXhr.upload.addEventListener('progress',progressHandlingFunction, false);
				}
				return myXhr;
			},
			data: formData,
			cache: false,
			contentType: false,
			processData: false
		});
		this.disabled=false; this.value='Загрузить';
		$('#file').disabled=false;
	});

	$('#date').change(function() {
		var date = this.value;
		var rfull = /^\d{2}[.]\d{2}[.]\d{4}$/;
		var rddmm = /^\d{2}[.]\d{2}$/;
		var rdd = /^\d{2}$/;
		if(!(rfull.test(date) || rddmm.test(date) || rdd.test(date)))
			$('#date_error_text').text("Дата должна быть в форматах: 'dd', 'dd.mm' или 'dd.mm.yyyy'");
		else
			$('#date_error_text').text("");
	});
		
	$(function() {
		$( "#tabs" ).tabs({
			collapsible: true
		});
	});

	CKEDITOR.replace( 'html' );
    CKEDITOR.replace( 'lid' );
    CKEDITOR.replace( 'info' );
    CKEDITOR.replace( 'authors' );
});
