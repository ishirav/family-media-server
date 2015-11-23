
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
    return jQuery.map($('.selected'), function(item) { 
        var url = decodeURI($(item).data('url'));
        return url.split('?')[0];
    });
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
    var target_path = window.location.pathname.replace('/home/', '/paste/');
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


function new_folder_prompt() {
    BootstrapDialog.show({
        title: 'New Folder',
        message: '<input class="form-control" placeholder="Enter folder name" id="folder_name">',
        buttons: [
            {
                label: 'Cancel',
                action: function(dialogRef) {
                    dialogRef.close();
                }
            },
            {
                label: 'Create',
                cssClass: 'btn-success',
                action: function(dialogRef) {
                    new_folder($('#folder_name').val());
                    dialogRef.close();                    
                }
            }            
        ],       
        onshown: function(dialogRef) {
            $('#folder_name').focus();
        }
    });
}


function new_folder(name) {
    var target_path = window.location.pathname.replace('/home/', '/new_folder/');
    $.post(target_path, JSON.stringify({name: name}))
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
        
    var gesture_handler = new Hammer($('#directory').get(0), {domEvents: true});

    gesture_handler.on('press', function(ev) {
        var item = $(ev.target).closest('.item');
        select_item(item);
        ev.gesture.preventDefault();
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
        ev.gesture.preventDefault();
    });

    $('.cut-btn').on('click', cut);
    $('.copy-btn').on('click', copy);
    $('.paste-btn').on('click', paste);
    $('.delete-btn').on('click', confirm_del);
    $('.new-btn').on('click', new_folder_prompt);
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
