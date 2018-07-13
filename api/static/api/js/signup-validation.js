import Ajax from './Ajax.js';
import Utils from './Utils.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());
const utils = new Utils();

const signupValidation = function () {

    function showerror(error_message) {
		  $('#signup-fail-message').html("<h4>*" + error_message + "</h4>");
    }
    
    function hideerror() {
		  $('#signup-fail-message').html("");
    }

    //Phone validation
    $('#inputPhone').keypress(function (e) {
      utils.allowOnlyNumbers(e);
      //utils.allowCertainLength(e, $(this).val().length, 10);
    });
    
    $(".form-signup").submit(function (e) {
        // catch the form's submit event
        e.preventDefault();
        hideerror();
        $('#signup-success-message').html("");

        if (!(utils.validate_email($('#inputEmail').val()))) {
          showerror("This is not a valid email address.");
        }
        else {
          if ($("#inputPassword").val().length < 6){
            showerror("Password must be more than 5 characters.");
          }
          else{
            var signup_data = {
                firstname: $("#inputFirstName").val(),
                lastname: $("#inputLastName").val(),
                country: $("#inputCountry").val(),
                institution: $("#inputInstitution").val(),
                phone: $("#inputPhone").val(),
                email: $("#inputEmail").val(),
                password: $("#inputPassword").val(),
                password2: $("#inputConfirmPassword").val(),
                description: $("#inputDescription").val()
            };

            ajax.post(HomeRoutes.home.signup, signup_data).then((return_data) => {
                //edw na mpei loader
              if (return_data.success === true) {
                hideerror();
                $('#signup-success-message').html("<h4>*You have successfully registered. An account activation email will be sent to you shortly.</h4>");
              }else{
                showerror(return_data.message);
              }
            }).catch((error) => {
              //edw na kryftei o loader
                const err = new AjaxError(error);
                console.log(err);
                showerror(err.msg);
              });
          }//second else end
        }//first else end
    });//submit event end
}; //function END

export {signupValidation};