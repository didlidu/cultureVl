$(function() {
                
                // Note: make sure you call dropotron on the top level <ul>
                $('#main-nav').find('> ul').dropotron({
                    mode: 'instant',     // Menu mode ("instant", "fade", "slide", "zoom")
                    speed: '10',     // Menu speed ("fast", "slow", or ms)
                    hoverDelay: 20,        // Hover delay (in ms)
                    hideDelay: 50,        // Hide delay (in ms; 0 disables)
                    offsetY: 0 // Nudge up submenus by 10px to account for padding
                });
                $('#nav').find('> ul').dropotron({
                    mode: 'instant',     // Menu mode ("instant", "fade", "slide", "zoom")
                    speed: '10',     // Menu speed ("fast", "slow", or ms)
                    
                    hoverDelay: 20,        // Hover delay (in ms)
                    hideDelay: 100,        // Hide delay (in ms; 0 disables)
                    offsetY: 0 // Nudge up submenus by 10px to account for padding
                });
            
            });

// using jQuery
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
var p = $("#item_body > p").filter(function( index ){
    return regex.test($(this).text())
  });
var id = $('#article_id').text();
p.each(function(){
  text = $(this).text();
  text = text.match(/[0-9 ]+/);
  arpic = text[0].split(' ');
  var arrayLength = arpic.length;
  divbody = ""
  for (var i = 0; i < arrayLength; i++) {
      divbody += '<a href="/media/'+ id + '/' + arpic[i] +'.jpg"' +'></a>';
  }
  divbody = '<div class="fotorama" data-width="100%" data-ratio="800/600" data-minwidth="400" data-maxwidth="1000" data-minheight="300" data-maxheight="100%" data-loop="true">' + divbody + '</div>';
  $(this).replaceWith( divbody );
});

});

$( document ).ready(function() {
	//next = {{ next }};
	next = 0;
    $( "#more" ).click(function( event ) {
		alert(next);
		$.ajax({
		   type:"POST",
		   url:"/get_more/",
		   data: {
					'csrfmiddlewaretoken': '{{ csrf_token }}',
					"csrftoken": "{{ csrf_token }}",
				  'next': next,
				  'some-form-field': $("myform input:first").val(), // from form
				  'background-color': $("body").css("background-color")
				  // all of this data is submitted via POST to your view.
				  // in django, request.POST['background-color'] 
		   },
		   success: function(data){
			   alert(data);
			   $("#main_container").append(data);
		   }
		});
        event.preventDefault();
 
    });


 
});
