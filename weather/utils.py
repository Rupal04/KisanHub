import logging
import json
import requests

from rest_framework.decorators import api_view

from weather.constants import ErrorConstants, MetricsConstant
from weather.response import SuccessResponse, ErrorResponse, WeatherResponse
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
        for resp in resp_content:
            if not Measure.objects.filter(value=resp["value"], year=resp["year"],
                                          month=resp["month"], metrics=metric, location=location).exists():
                Measure.objects.create(value=resp["value"], year=resp["year"],
                                       month=resp["month"], metrics=metric, location=location)

            else:
                logger.error(ErrorConstants.WEATHER_INFO_ALREADY_EXISTS)

        response = SuccessResponse(msg = "Successfully stored " + metric + " information for " + location.name + " location." )
    except Exception as e:
        logger.error(ErrorConstants.WEATHER_INFO_STORING_ERROR + str(e))
        response = ErrorResponse(msg=ErrorConstants.WEATHER_INFO_STORING_ERROR)

    return response


def get_metrics_data_and_store(base_api_url, metric, location_name, location):
    api_url = base_api_url + metric + "-" + location_name + ".json"
    response = requests.get(api_url, stream=True)
    resp_content = json.loads(response.content)
    data_store_resp = store_metric_data_in_bulk(resp_content, metric, location)
    return data_store_resp


def add_weather_information():
    """
    This method fetches the weather information for all the locations and metrices and then store that data to the models.
    :return:
    """
    try:
        base_api_url = "https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/"
        location_obj = Location.objects.all()
        for location in location_obj:
            location_name = location.name

            #for rainfall
            metric = MetricsConstant.Rainfall
            rainfall_metric= get_metrics_data_and_store(base_api_url, metric, location_name, location)
            print(rainfall_metric.msg)

            #for Tmax
            metric = MetricsConstant.Tmax
            tmax_metric = get_metrics_data_and_store(base_api_url, metric, location_name, location)
            print(tmax_metric.msg)

            #for Tmin
            metric = MetricsConstant.Tmin
            tmin_metric = get_metrics_data_and_store(base_api_url, metric, location_name, location)
            print(tmin_metric.msg)

    except Exception as e:
        logger.error(ErrorConstants.WEATHER_INFO_STORING_ERROR + str(e), exc_info=True)


def get_weather_information(**kwargs):
    """
    This method fetches the weather information from the model as per the parameters are given in the API call.
    :param kwargs: arguments that are in the API call as query parameters.
    :return: list of weather information in a particular format and error response if it happens.
    """
    try:
        weather_info_obj = Measure.objects.filter()
        if kwargs["start_date"] and kwargs["end_date"]:
            start_year, start_month = kwargs["start_date"].split("-", 1)
            end_year, end_month = kwargs["end_date"].split("-", 1)
            weather_info_obj = weather_info_obj.filter(year__range=(start_year, end_year),
                                                      month__range=(start_month, end_month))

        if kwargs["metric"]:
            metric_val = kwargs["metric"]
            weather_info_obj = weather_info_obj.filter(metrics = metric_val)

        if kwargs["location"]:
            location_name = kwargs["location"]
            location_obj = Location.objects.get(name=location_name)
            weather_info_obj = weather_info_obj.filter(location=location_obj)

        response_list =[]
        for obj in weather_info_obj:
            year_val = obj.year
            month_val = obj.month
            complete_date = str(year_val) + "-" + str(month_val)
            measure_val = obj.value
            response_list.append(complete_date + ":" + str(measure_val))

        response = WeatherResponse(response_list)
        return response
    except Exception as e:
        logger.error(ErrorConstants.WEATHER_INFO_FETCHING_ERROR + str(e), exc_info=True)
        return None