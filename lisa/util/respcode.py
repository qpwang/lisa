from django.utils.translation import ugettext

OK = 0

UNKNOWN_ERROR = 1
HTTPS_REQUIRED = 2
PARAM_REQUIRED = 3
DATA_ERROR = 4

USER_AUTHENTICATION_ERROR = 9
USER_NOT_ACTIVATED = 10
USER_REGISTERED = 11
USER_NOT_EXIST = 12
USER_ALREADY_ACTIVE = 13
ACTIVATION_CODE_INVALID = 14
ACTIVATION_CODE_EXPIRED = 15
AUTH_ERROR = 16
TOKEN_INVALID = 17
TOKEN_VALIDATION_FAIL = 18

CONNECT_AUTH_ERROR = 20
USER_CANCEL_CONNECT = 21
USER_CANCEL_REGISTER = 22

API_AUTHENTICATION_ERROR  = 50
REMOVE_FAILED = 51
LOGOUT_FAILED = 52

ERROR_MESSAGE = {
    UNKNOWN_ERROR : ugettext("Unknown error."),
    HTTPS_REQUIRED : ugettext("HTTPS required."),
    PARAM_REQUIRED : ugettext("Parameter required."),
    DATA_ERROR : ugettext("Data error."),

    USER_AUTHENTICATION_ERROR :ugettext("Account or password is not correct."),
    USER_NOT_ACTIVATED : ugettext("User has not been activated."),
    USER_REGISTERED : ugettext("User is registered."),
    USER_NOT_EXIST : ugettext("User does not exist."),
    USER_ALREADY_ACTIVE : ugettext("User is already active."),
    ACTIVATION_CODE_INVALID : ugettext("Activation code invalid."),
    ACTIVATION_CODE_EXPIRED : ugettext("Activation code expired."),
    AUTH_ERROR : ugettext("Invalid email or password."),
    TOKEN_INVALID : ugettext("Token invalid."),
    TOKEN_VALIDATION_FAIL : ugettext("Token validation fails."),

    CONNECT_AUTH_ERROR : ugettext("Connection authentication error."),
    USER_CANCEL_CONNECT : ugettext("User cancel the connection."),
    USER_CANCEL_REGISTER : ugettext("User cancel the registration."),

    API_AUTHENTICATION_ERROR : ugettext("Authorization Failed."),
}
