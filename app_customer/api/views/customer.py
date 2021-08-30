import logging

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.dto.customer_dto import CustomerDto
from api.exceptions.invalid_data import InvalidDataException
from api.exceptions.invalid_operation import InvalidOperationException
from api.service.customer_service import CustomerService


class CustomerView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Definição para autenticação
        self.authentication_classes = [SessionAuthentication, BasicAuthentication]
        self.permission_classes = [IsAuthenticated]

        # Classe de serviço para cliente
        self.service = CustomerService()

    @swagger_auto_schema(operation_description="Create a Customer",
                         request_body=Schema(
                                            type=TYPE_OBJECT,
                                            properties={
                                               "name": Schema(type=TYPE_STRING),
                                               "email": Schema(type=TYPE_STRING),
                                            },
                                            required=["name", "email"]),
                         responses={201: Schema(
                                            type=TYPE_OBJECT,
                                            properties={
                                               "id": Schema(type=TYPE_STRING),
                                               "name": Schema(type=TYPE_STRING),
                                               "email": Schema(type=TYPE_STRING),
                                            })
                                    }
                         )
    def post(self, request):
        logging.info(f"Create Customer API accessed by {request.user.username}")

        try:
            # Converte a entrada em DTO
            input_dto = CustomerDto().from_dict(JSONParser().parse(request)).validate()
            # Chama o serviço para cadastrar o cliente
            customer_dto = self.service.create(input_dto)

        except (InvalidDataException, ValidationError, InvalidOperationException) as e:
            # Responde com o status 400 no caso de existir dados inválidos no parâmetro
            logging.error(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Responde com status 400 e registra em log no caso de ocorrer um erro não especificado
            logging.exception("Invalid operation when creating customer.")
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(customer_dto.__dict__, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description="Update a Customer",
                         request_body=Schema(
                                            type=TYPE_OBJECT,
                                            properties={
                                               "id": Schema(type=TYPE_STRING),
                                               "name": Schema(type=TYPE_STRING),
                                               "email": Schema(type=TYPE_STRING),
                                            },
                                            required=["id", "name", "email"]),
                         responses={200: Schema(
                                            type=TYPE_OBJECT,
                                            properties={
                                               "id": Schema(type=TYPE_STRING),
                                               "name": Schema(type=TYPE_STRING),
                                               "email": Schema(type=TYPE_STRING),
                                            })
                                    }
                         )
    def put(self, request):
        logging.info(f"Update Customer API accessed by {request.user.username}")

        try:
            # Converte a entrada em DTO
            input_dto = CustomerDto().from_dict(JSONParser().parse(request)).validate()
            # Chama o serviço para atualizar o cliente
            customer_dto = self.service.update(input_dto)

        except (InvalidDataException, ValidationError, InvalidOperationException) as e:
            # Responde com o status 400 no caso de existir dados inválidos no parâmetro
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Responde com status 400 e registra em log no caso de ocorrer um erro não especificado
            logging.exception("Invalid operation when updating customer.")
            return Response(str(e), status=status.HTTP_200_OK)

        return JsonResponse(customer_dto.__dict__, status=status.HTTP_200_OK)
