

//Dropotron section
$(function() {
    // Note: make sure you call dropotron on the top level <ul>
    $('#main-nav > ul').dropotron({ 
        offsetY: -10 // Nudge up submenus by 10px to account for padding
    });
    $('#nav > ul').dropotron({ 
            offsetY: -10 // Nudge up submenus by 10px to account for padding
    });
});