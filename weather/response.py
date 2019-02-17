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
    year = None
    month = None

    def __init__(self, value, year, month):
        self.value = value
        self.year = year
        self.month = month


class WeatherListResponse(object):
    def __init__(self, results=None, msg=SuccessConstants.SUCCESS_RESPONSE):
        if results is not None:
            self.results = results
        self.msg = msg
        self.success = True