/**
 * Created by joseph on 12/6/15.
 */

$(function() {
    $('#event-list').find('.register-btn').on('click', function () {
        var root_url = window.location.origin ? window.location.origin+'/' : window.location.protocol+'/'+window.location.host+'/';
        var event_id = $(this).attr('data-id');
        var register_url = root_url + "events/" + event_id + "/register";
        var signin_url = root_url + "signin";
        $.ajax({
            url: register_url,
            type: 'GET',
            dataType: 'JSON',
            success: function (data) {
                var return_code = data.return_code;
                if (return_code == 0) {
                    window.location.reload();
                }
                else if(return_code == 100){
                    window.location.replace(signin_url)
                }
                else {
                    alert(data.return_desc);
                }
            },
            error: function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});

$(function() {
    $('#event-list').find('.cancel-register-btn').on('click', function () {
        $('#cancel-register-modal').modal({
            relatedTarget: this,
            onConfirm: function() {
                var root_url = window.location.origin ? window.location.origin+'/' : window.location.protocol+'/'+window.location.host+'/';
                var event_id = $(this.relatedTarget).data('id');
                var cancel_register_url = root_url + "events/" + event_id + "/cancel-register";
                $.ajax({
                    url: cancel_register_url,
                    type: 'GET',
                    dataType: 'JSON',
                    success: function (data) {
                        var return_code = data.return_code;
                        if (return_code == 0) {
                            window.location.reload();
                        }
                        else {
                            alert(data.return_desc);
                        }
                    },
                    error: function(xhr,errmsg,err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                })
            },
            // closeOnConfirm: false,
            onCancel: function() {
            }
        });
    })
});
