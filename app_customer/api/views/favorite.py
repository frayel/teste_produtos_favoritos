import logging

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY, Items
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.dto.favorite_dto import FavoriteDto
from api.exceptions.invalid_data import InvalidDataException
from api.exceptions.invalid_operation import InvalidOperationException
from api.service.favorite_service import FavoriteService


class FavoriteView(APIView):
    """ url: /app/customer/<id>/favorite/ """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_classes = [SessionAuthentication, BasicAuthentication]
        self.permission_classes = [IsAuthenticated]
        self.service = FavoriteService()

    @swagger_auto_schema(operation_description="Add a Favorite product to a customer's list",
                         request_body=Schema(
                                            type=TYPE_OBJECT,
                                            properties={
                                               "product": Schema(type=TYPE_STRING),
                                            },
                                            required=["product"]),
                         responses={201: Schema(
                                            type=TYPE_OBJECT,
                                            properties={
                                               "id": Schema(type=TYPE_STRING),
                                               "customer": Schema(type=TYPE_STRING),
                                               "product": Schema(type=TYPE_STRING),
                                            })
                                    }
                         )
    def post(self, request, customer_id):
        logging.info(f"Add Favorite API accessed by {request.user.username}")

        try:
            input_dto = FavoriteDto().from_dict(JSONParser().parse(request)).validate()
            input_dto.customer = customer_id
            favorite_dto = self.service.create(input_dto)

        except (InvalidDataException, ValidationError, InvalidOperationException) as e:
            logging.error(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.exception("Invalid operation when creating favorite item.")
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(favorite_dto.__dict__, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description="View a customer's favorite list",
                         responses={200: Schema(
                             type=TYPE_ARRAY,
                             items=Items(type=TYPE_OBJECT, properties={
                                 "id": Schema(type=TYPE_STRING),
                                 "customer": Schema(type=TYPE_STRING),
                                 "product": Schema(type=TYPE_STRING),
                             }))
                         }
    )
    def get(self, request, customer_id):
        logging.info(f"View Favorite API accessed by {request.user.username}")

        try:
            page_num = request.GET.get("page", 1)
            favorite_result = self.service.list(customer_id, page_num)

        except (InvalidDataException, ValidationError, InvalidOperationException) as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.exception("Invalid operation when getting favorite item list.")
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(favorite_result, status=status.HTTP_200_OK, safe=False)
