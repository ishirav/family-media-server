
var select_mode = false;


function update_select_mode() {
    select_mode = !!$('#directory .selected').length;
    $('.select-' + select_mode).show();
    $('.select-' + !select_mode).hide();
}


function select_item(item) {
    item.toggleClass('selected');
    update_select_mode();
}


function get_selection() {
    return jQuery.map($('.selected'), function(item) { return decodeURI($(item).data('url')) });
}

function cut_or_copy(mode) {
    var data = {mode: mode, paths: get_selection()};
    $.post('/cut_or_copy/', JSON.stringify(data))
        .done(function(msg) {
            if (msg) {
                BootstrapDialog.show({title: 'Error', message: msg});
            }
            else {
                $('.selected').removeClass('selected');
                update_select_mode();
            }
        });
}


function cut() {
    cut_or_copy('cut');
}


function copy() {
    cut_or_copy('copy');
}


function paste() {
    var target_path = window.location.pathname.replace('/root/', '/paste/');
    $.post(target_path, function(msg) {
        if (msg) {
            BootstrapDialog.show({title: 'Error', message: msg});
        }
        else {
            window.location = window.location;
        }
    });
}


function confirm_del() {
    BootstrapDialog.confirm({
        title: 'Delete',
        message: 'Are you sure you want to delete the selected files?',
        type: BootstrapDialog.TYPE_DANGER,
        btnOKLabel: 'Delete',
        callback: function(result) {
            if (result) del();
        }
    });
}


function del() {
    var data = {paths: get_selection()};
    $.post('/delete/', JSON.stringify(data))
        .done(function(msg) {
            if (msg) {
                BootstrapDialog.show({title: 'Error', message: msg});
            }
            else {
                window.location = window.location;
            }
        });
}


function init_event_handlers() {
        
    var gesture_handler = new Hammer($('#directory').get(0));

    gesture_handler.on('press', function(ev) {
        var item = $(ev.target).closest('.item');
        select_item(item);
    });

    gesture_handler.on('tap', function(ev) {
        var item = $(ev.target).closest('.item');
        if (item.length) {
            if (select_mode) {
                select_item(item);
            }
            else {
                window.location.href = item.data('url');
            }
        }
    });

    $('.cut-btn').on('click', cut);
    $('.copy-btn').on('click', copy);
    $('.paste-btn').on('click', paste);
    $('.delete-btn').on('click', confirm_del);
}


// Send CSRF token with AJAX requests
$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
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
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});
