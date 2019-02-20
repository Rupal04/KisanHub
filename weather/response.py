from weather.constants import SuccessConstants, ErrorConstants


class SuccessResponse(object):
    def __init__(self, msg=SuccessConstants.SUCCESS_RESPONSE):
        self.msg = msg
        self.success = True


class ErrorResponse(object):
    def __init__(self, msg=ErrorConstants.ERROR_RESPONSE):
        self.msg = msg
        self.success = False


class WeatherResponse(object):
    value = None
    date = None

    def __init__(self, results, msg=SuccessConstants.SUCCESS_RESPONSE):
        self.results = results
        self.msg = msg
        self.success = True
