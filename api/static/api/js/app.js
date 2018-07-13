import {loginValidation} from "./login-validation.js";
import {signupValidation} from "./signup-validation.js";
import {ActivateUser} from "./activate-user.js";



$(document).ready(function() {
    loginValidation();
    signupValidation();
    ActivateUser();    
});