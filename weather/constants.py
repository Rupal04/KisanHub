Metrics = (
    (1,'RAINFALL'),
    (2, 'TMAX'),
    (3, 'TMIN')
)


class MetricsConstant(object):
    RAINFALL = 1
    TMAX = 2
    TMIN = 3


class SuccessConstants(object):
    SUCCESS_RESPONSE = "Successful"


class ErrorConstants(object):
    ERROR_RESPONSE = "Error."
    EXCEPTIONAL_ERROR = "Some Unexpected Exception Occured. Error is "