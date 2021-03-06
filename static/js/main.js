function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
$( document ).ready(function() {


var regex = new RegExp('\\*{3}\\[([0-9 ]+)\\]\\*{3}');
var P = $("img" , $("#item_body")).parent();
for(var i=0; i<P.length;i++){
	var imgs = $('img', P[i]);
	divbody = ""	
	for(var j=0;j<imgs.length;j++){
		divbody += '<a href="'+ imgs[j].getAttribute("src") + '"></a>';
	}
	divbody = '<div class="fotorama" data-width="100%" data-ratio="800/600" data-minwidth="400" data-maxwidth="800" data-minheight="300" data-maxheight="500" data-loop="true">' + divbody + '</div>';
	$(P[i]).replaceWith( divbody );
	
}
});

$( document ).ready(function() {

    var nav = $(" #main-nav ");
    nav.hover(
    function(){
      $( "div:not(:last)", nav).css("display", "inherit");
    },
    function(){
      $( "div:not(:last)", nav).css("display", "none");
    }

    );

		$( "#more" ).click(function( event ) {
			$('#more').text("");

            $('#more').append("<span><img style='width:15px; height: auto;' src='" + $('#loader_pic').attr('src') + "'/></span>");
			$.ajax({
			   type:"POST",
			   url:"/get_more/",
			   data: {
				   'next': getCookie('next'),
				   'type_of_page': $('#type_of_page').text(),
			   },
			   success: function(data){
				   if(data.length == 0) popup("Больше записей нет :(");
				   $("#main_container").append(data);
				   $('#more').text("");
				   $('#more').append("<span><a>Ещё записи</a></span>");
			   },
			   error: function() {
				   $('#more').text("");
				   $('#more').append("<span><a>Ещё записи</a></span>");
				   popup("Ошибка соединения с сервером.");
			   }
			});
			event.preventDefault();
			
    });


 
});
