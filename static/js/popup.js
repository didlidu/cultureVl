


function popup(message) {
	var block = "<div id='popup' style='display: none; position: fixed; z-index:100; \
	top: 20px; left: 20px; background-color: #B8B8B8; height: 100px; width: 300px; \
	text-align: center; vertical-align: text-middle; line-height: 100px; border-style:solid; border-width:5px;'>\
	<span style='display: inline-block; \
	vertical-align: middle; line-height: normal;'>"  + message + "</span></div>";
	$('BODY').append(block);
	$('#popup').fadeIn(500);
	setTimeout(function(){
		$('#popup').fadeOut(500).wait().remove();
	}, 2000);
	
}
