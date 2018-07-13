import Ajax from './Ajax.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());

function showerror(id,error_message) {
    $(id).html("<h4>*" + error_message + "</h4>");
}

function hideerror() {
    $('#activate-fail-message').html("");
    $('#delete-fail-message').html("");

}

const ActivateUser = function () {

    $("[data-toggle=tooltip]").tooltip();

    $('.modal').on('show.bs.modal', function (e) {
        hideerror();
        const $trigger = $(e.relatedTarget);
        const email = $trigger.val();
        var data = {
            email : email,
            reason: $('#delete-reason').val()
        };
        console.log(data);
        $('.modal-title').html($trigger.val());
        $(".btn-delete").on('click', function () {
            data['reason']=$('#delete-reason').val();
            ajax.post(HomeRoutes.home.delete, data).then((return_data) => {
                if (return_data.success === true) {
                    $($trigger).closest('tr').remove();
                    $(".modal .close").click()
                }else{
                    showerror('#delete-fail-message',return_data.message);
                }
            }).catch((error) => {
                const err = new AjaxError(error);
                console.log(err);
                showerror('#delete-fail-message',err.msg);
            });
        });

        $(".btn-activate").on('click', function () {
            ajax.post(HomeRoutes.home.activate, data).then((return_data) => {
                if (return_data.success === true) {
                    $($trigger).closest('tr').remove();
                    $(".modal .close").click()
                }else{
                    showerror('#activate-fail-message',return_data.message);
                }
            }).catch((error) => {
                const err = new AjaxError(error);
                console.log(err);
                showerror('#activate-fail-message',err.msg);
            });
        });
        
    });
}

export {ActivateUser};
