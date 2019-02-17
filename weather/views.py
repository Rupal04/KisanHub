import logging

from weather.constants import ErrorConstants
from weather.response import ErrorResponse
from weather.utils import to_dict
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def fetch_weather_data(request):
    try:
        data = request.data()
        start_date = data.get("start_date", "")
        end_date = data.get("end_date", "")
        metric = data.get("metric", "")
        location = data.get("location", "")

        weather_resp = get_weather_information(start_date, end_date, metric, location)

        if not weather_resp:
            response = ErrorResponse(msg=ErrorConstants.WEATHER_INFO_FETCHING_ERROR)
            return Response(to_dict(response), status=status.HTTP_404_NOT_FOUND)

        elif weather_resp.success is False:
            response = ErrorResponse(msg=weather_resp.msg)
            return Response(to_dict(response), status=status.HTTP_202_ACCEPTED)

        return Response(to_dict(weather_resp), status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(ErrorConstants.EXCEPTIONAL_ERROR + str(e), exc_info=True)
        response = ErrorResponse()
        return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
