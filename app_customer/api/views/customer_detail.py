import logging

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions.invalid_data import InvalidDataException
from api.exceptions.invalid_operation import InvalidOperationException
from api.service.customer_service import CustomerService


class CustomerDetailView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Definição para autenticação
        self.authentication_classes = [SessionAuthentication, BasicAuthentication]
        self.permission_classes = [IsAuthenticated]

        # Classe de serviço para cliente
        self.service = CustomerService()

    @swagger_auto_schema(operation_description="View a Customer",
                         responses={200: Schema(
                             type=TYPE_OBJECT,
                             properties={
                                 "id": Schema(type=TYPE_STRING),
                                 "name": Schema(type=TYPE_STRING),
                                 "email": Schema(type=TYPE_STRING),
                             })
                         }
                         )
    def get(self, request, customer_id):
        logging.info(f"View Customer API accessed by {request.user.username}")

        try:
            # Chama o serviço para obter os dados do cliente
            customer_dto = self.service.view(customer_id)

        except (InvalidDataException, ValidationError, InvalidOperationException) as e:
            # Responde com o status 400 no caso de existir dados inválidos no parametro
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Responde com status 400 e registra em log no caso de ocorrer um erro não especificado
            logging.exception("Invalid operation when getting customer.")
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(customer_dto.__dict__, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False)
    @swagger_auto_schema(operation_description="Remove a Customer")
    def delete(self, request, customer_id):
        logging.info(f"Remove Customer API accessed by {request.user.username}")

        try:
            # Chama o serviço para remover o cliente
            self.service.delete(customer_id)

        except (InvalidDataException, ValidationError, InvalidOperationException) as e:
            # Responde com o status 400 no caso de existir dados inválidos no parametro
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Responde com status 400 e registra em log no caso de ocorrer um erro não especificado
            logging.exception("Invalid operation when removing customer.")
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
