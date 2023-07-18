DIRECTOR_BUSINESS = "director_business"    #variables are values
DIRECTOR_SALES = "director_sales"

EMAIL_NOT_REGISTERED = "Email is not registered"
MISSING_PARAMS = "Missing parameters"
NOT_AUTHORISED = "Not authorised"
INVALID_CREDENTIALS = "Invalid credentials"
DEFAULT_FAILURE_MESSAGE = "Data doesn't exists"


JWT_EXP_TIME = 60 #MINs


PATH_TO_SKIP_MIDDLEWARE = [
    '/api/register/',
    '/api/login/',
]