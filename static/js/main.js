/**
 *   Welcome to Kyle's really really bulk Javascript file of fun!
 *   This file is loaded after Jquery and at the end of the DOM to guaranteed loading order.
 */

/**
 * Django doesn't like it when we don't include the crsf token in AJAX requests.
 * @param name of the cookie
 * @returns string
 */
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

/**
 * This insures that all headers are of same origin in our AJAX sending for csrftokens
 */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

/**
 * This is contained in the author.html, it edits the the profile fields when onclick is called.
 * Each field must always have a sibling input which makes it easy on the selector.
 *  -field_name: this is relative to the POST request to update the field being edited.
 */
function editProfileField(that, field_name) {
    var $button = $(that);
    var $confirmation_button = $(that).parent().siblings("span.input-group-btn");
    var $field = $(that).parent().siblings("input");
    $field.prop("disabled", false);
    $button.parent().hide();
    $confirmation_button.show();
}

/**
 * This is contained in the author.html, after a field is edited, it must be updated if it changed.
 *  -field_name: this is relative to the POST request to update the field being edited.
 */
function confirmEditProfileField(that, field_name) {
    var $button = $(that);
    var $field = $(that).parent().siblings("input");
    var $edit_button = $(that).parent().siblings("span.input-group-btn");
    var $progress = $(that).parent().parent().siblings(".progress");
    var sending_data = {};
    $button.prop("disabled", true);
    $field.prop("disabled", true);
    $progress.slideDown();
    sending_data[field_name] = $field.val();
    $.post("/profile/update/", sending_data, function (data) {
        //Callback from updating profile
        if (data.status) {
            //Our new field is valid
            $progress.slideUp();
            $button.parent().hide();
            $edit_button.show();
            $button.prop("disabled", false);
        }
        else {
            //TODO: Display some sort of error to the user
        }

    })
}

/**
 * Add all current page nav items
 */

var allNavItems = $(".nav-sidebar > li[id$='_nav']");

var navItemBlocks = [];

// Add all the classes into the buttons
for (var i = 0; i < allNavItems.length; i++) {
    var object = $(allNavItems[i]);
    var id = $(allNavItems[i]).attr('id').replace("_nav","");

    navItemBlocks.push("#" + id);
    var block = $("#" + id);
    if(i > 0) {
        block.hide();
    }
    block.find("h1").after('<div class="loading-main" style="display:none;"></div>');
}

function getNavItem(currentBlock,navItem) {
    $.get("http://" + location.host + navItem.attr('data-url'), function(data) {
            var content= currentBlock.find(".content");
    content.empty();
    currentBlock.find(".loading-main").hide();
    if(data.length <= 2) {
        content.append('<span>No results.</span>');
        } else {
        content.append(data);
        }
        }).fail(function(error) {
    alert( "error " + error);
  });
};

getNavItem($(navItemBlocks[0]),$(allNavItems[0]));

// When we click a nav item..
$(".nav-sidebar > li[id$='_nav']").click(function (item) {
    //Hide other streams
    // Make clicked item active
    // Make the others not
    var currentObject = $(this);
    var currentId = currentObject.attr('id');
    var currentBlock = null;
    for(var i = 0; i < allNavItems.length; i++) {
        console.log(currentId)
        // Get the object
        var object = $(allNavItems[i]);
        var objectId = object.attr('id');

        var blockId = navItemBlocks[i];

        // Check if it's the item we clicked
        if(objectId !== currentId) {
            // Set all others as inactive
            object.removeClass("active");
            // Hide their content
            $(blockId).hide();
        } else if(objectId === currentId) {

                // Show clicked content
                currentBlock = $(blockId);
                currentBlock.show();

                // Add active class to nav item
                currentObject.addClass("active");
        }
        $(blockId).find(".content").empty();
    }

    currentBlock.find(".loading-main").show();
    var content = currentBlock.find(".content");
    //loading.show(); 
    
    $.get("http://" + location.host + currentObject.attr('data-url'), function(data) {
    currentBlock.find(".loading-main").hide();
    if(data.length <= 2) {
        content.append('<span>No results.</span>');
        } else {
        content.append(data);
        }
        });

    });
