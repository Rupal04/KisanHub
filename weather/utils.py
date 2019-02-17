import logging
import requests
import json

from weather.constants import ErrorConstants, MetricsConstant, SuccessConstants
from weather.response import WeatherListResponse, SuccessResponse, ErrorResponse
from weather.models import Location, Measure

logger = logging.getLogger(__name__)

def to_dict(obj):
    """Represent instance of a class as dict.
        Arguments:
        obj -- any object
        Return:
        dict
        """

    def serialize(obj):
        """Recursively walk object's hierarchy."""
        if isinstance(obj, (bool, int, float)):
            return obj
        elif isinstance(obj, dict):
            obj = obj.copy()
            for key in obj:
                obj[key] = serialize(obj[key])
            return obj
        elif isinstance(obj, list):
            return [serialize(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(serialize([item for item in obj]))
        elif hasattr(obj, '__dict__'):
            return serialize(obj.__dict__)
        else:
            return repr(obj)

    return serialize(obj)


def store_metric_data_in_bulk(resp_content, metric, location):
    try:
        objs = [
            Measure(value=resp.value, year=resp.year, month=resp.month, metrics=metric, location=location)
            for resp in resp_content
        ]

        Measure.object.create(objs)

        response = SuccessResponse(msg=SuccessConstants.WEATHER_DATA_STORE_SUCCESS)


    except Exception as e:
        logger.error(ErrorConstants.WEATHER_INFO_STORING_ERROR + str(e))
        response = ErrorResponse(msg=ErrorConstants.WEATHER_INFO_STORING_ERROR)

    return response


def get_metrics_data_and_store(base_api_url, metric, location_name, location):
    api_url = base_api_url + metric + "-" + location_name + ".json"
    response = requests.get(api_url, stream=True)
    resp_content = json.loads(response.content)
    data_store_resp = store_metric_data_in_bulk(resp_content, metric, location)
    print(data_store_resp.msg)


def add_weather_information():
    try:
        base_api_url = "https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/"
        location_obj = Location.objects.all()
        for location in location_obj:
            location_name = location.name

            #for rainfall
            metric = MetricsConstant.Rainfall
            get_metrics_data_and_store(base_api_url, metric, location_name, location)

            #for Tmax
            metric = MetricsConstant.Tmax
            get_metrics_data_and_store(base_api_url, metric, location_name, location)

            #for Tmin
            metric = MetricsConstant.Tmin
            get_metrics_data_and_store(base_api_url, metric, location_name, location)


    except Exception as e:
        logger.error(ErrorConstants.WEATHER_INFO_STORING_ERROR + str(e), exc_info=True)
        return None

def get_weather_information(start_date, end_date, metric, location):
    try:
        weather_information_list =[]

        response = WeatherListResponse(weather_information_list)
        return response
    except Exception as e:
        logger.error(ErrorConstants.WEATHER_INFO_FETCHING_ERROR + str(e), exc_info=True)
        return None