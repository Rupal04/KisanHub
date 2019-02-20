import logging

from rest_framework.decorators import api_view

from weather.constants import ErrorConstants
from weather.response import ErrorResponse
from weather.utils import to_dict, get_weather_information
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

@api_view(['GET'])
def fetch_weather_data(request):
    try:
        query_params = request.query_params

        start_date = query_params.get("start_date","")
        end_date = query_params.get("end_date", "")
        metric = query_params.get("metric","")
        location = query_params.get("location","")

        weather_resp = get_weather_information(start_date=start_date, end_date=end_date, metric=metric, location=location)

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
