import Ajax from './Ajax.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());


const loginValidation = function () {

    $(".form-signin").submit(function (e) {
        // catch the form's submit event

        e.preventDefault();
        var login_data = {
            email: $("#inputEmail").val(),
            password: $("#inputPassword").val()
        };

        ajax.post(HomeRoutes.home.login, login_data).then((return_data) => {
            //edw na mpei loader
            if (return_data.success === true) {
              window.location.href = return_data.redirectUri;
            } else if (return_data.success === false) {
              $("#login-fail-message").html("<h4> *" + return_data.message + "</h4>");
            }
          }).catch((error) => {
           //edw na kryftei o loader
            const err = new AjaxError(error);
            $("#login-fail-message").html("<h4> *" + err.msg + "</h4>");
          });
    });//submit event END
}; //function END

export {loginValidation};