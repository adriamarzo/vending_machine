from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from apps.vending.expections import NotEnoughCreditException, ProductOutOfStockException

from apps.vending.models import Order, Product, User, VendingMachineSlot
from apps.vending.serializers import VendingMachineSlotSerializer, UserSerializer
from apps.vending.validators import (
    ListSlotsValidator,
    AuthValidator,
    OrderValidator,
    UserValidator,
)
from rest_framework import status


class AuthView(APIView):
    def post(self, request: Request) -> Response:
        validator = AuthValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        try:
            user = User.objects.get(username=validator.validated_data["username"])
            user_serializer = UserSerializer(user, many=False)
            return Response(data=user_serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class VendingMachineSlotView(APIView):
    def get(self, request: Request) -> Response:
        validator = ListSlotsValidator(data=request.query_params)
        validator.is_valid(raise_exception=True)
        filters = {}
        if quantity := validator.validated_data["quantity"]:
            filters["quantity__lte"] = quantity

        slots = VendingMachineSlot.objects.filter(**filters)
        slots_serializer = VendingMachineSlotSerializer(slots, many=True)
        return Response(data=slots_serializer.data)


class UserView(APIView):
    def patch(self, request: Request, user_id) -> Response:
        validator = UserValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        try:
            user = User.objects.get(id=user_id)
            user.credit = validator.validated_data["credit"]
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def hasUserEnoughCredit(user: User, product: Product):
    if user.credit >= product.price:
        return True
    return False


class OrderView(APIView):
    def post(self, request: Request) -> Response:
        validator = OrderValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        try:
            user = User.objects.get(id=validator.validated_data["user_id"])
            product = Product.objects.get(id=validator.validated_data["product_id"])

            if hasUserEnoughCredit(user, product) == False:
                raise NotEnoughCreditException()

            slot = VendingMachineSlot.objects.get(
                id=validator.validated_data["slot_id"]
            )

            if slot.quantity <= 0:
                raise ProductOutOfStockException(product)

            Order.objects.create(user=user, product=product, slot=slot)
            slot.quantity -= 1
            slot.save()

            user.credit -= product.price
            user.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotEnoughCreditException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": e})
        except ProductOutOfStockException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
