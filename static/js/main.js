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



$("#myposts_nav").click(function () {
    //Hide other streams
    $("#stream").hide();
    $("#allposts").hide();
    $.get('/post/my', function (data) {
        $("#myposts").html(data);
        //Show the My Posts stream
        $("#myposts").show();
        //Update Sidebar
        $("#myposts_nav").addClass("active");
        $("#stream_nav").removeClass("active");
        $("#allposts_nav").removeClass("active");
    });
});

$("#allposts_nav").click(function () {
    //Hide other streams
    $("#stream").hide();
    $("#myposts").hide();
    $.get('/post/all', function (data) {
        $("#allposts").html(data);
        //Show the My Posts stream
        $("#allposts").show();
        //Update Sidebar
        $("#allposts_nav").addClass("active");
        $("#stream_nav").removeClass("active");
        $("#myposts_nav").removeClass("active");
    });

});

$("#stream_nav").click(function () {
    //Hide other streams
    $("#myposts").hide();
    $("#allposts").hide();
    //Show the My Posts stream
    $("#stream").show();
    //Update Sidebar
    $("#stream_nav").addClass("active");
    $("#myposts_nav").removeClass("active");
    $("#allposts_nav").removeClass("active");
});
