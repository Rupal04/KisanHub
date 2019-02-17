Metrics = (
    ('Rainfall','Rainfall'),
    ('Tmax', 'Tmax'),
    ('Tmin', 'Tmin')
)


class MetricsConstant(object):
    Rainfall = "Rainfall"
    Tmax = "Tmax"
    Tmin = "Tmin"


class SuccessConstants(object):
    SUCCESS_RESPONSE = "Successful"
    WEATHER_DATA_STORE_SUCCESS = "Successfully stored wether information to that database."


class ErrorConstants(object):
    ERROR_RESPONSE = "Error."
    EXCEPTIONAL_ERROR = "Some Unexpected Exception Occured. Error is "
    WEATHER_INFO_FETCHING_ERROR = "Error in fetching weather information."
    WEATHER_INFO_STORING_ERROR = "Error in storing weather information."