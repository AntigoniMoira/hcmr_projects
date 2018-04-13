import Ajax from './Ajax.js';
import HomeRoutes from './routes.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());


const loginValidation = function () {

    $(".form-signin").submit(function (e) {
        // catch the form's submit event

        //Έστω ότι έχουν γίνει έλεγχοι και μας έχει δώσει email και password
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
              $("#login-fail-message").html("<h4> *" + return_data.errorMessage + "</h4>");
            }
          }).catch((error) => {
            $(".givmed-loader").hide();
            const err = new AjaxError(error);
            $("#login-fail-message").html("<h4> *" + err.msg + "</h4>");
          });
    });//submit event END
}; //function END

export {loginValidation};