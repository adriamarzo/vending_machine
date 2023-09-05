from _decimal import Decimal
from uuid import uuid4
from datetime import datetime
import factory
from factory.django import DjangoModelFactory

from apps.vending.models import Order, Product, User, VendingMachineSlot


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: "Product %d" % n)
    price = Decimal("10.40")
    created_at = datetime(2023, 5, 30, 12)
    updated_at = datetime(2023, 5, 30, 23)


class VendingMachineSlotFactory(DjangoModelFactory):
    class Meta:
        model = VendingMachineSlot

    product = factory.SubFactory(ProductFactory)
    quantity = 10
    row = 0
    column = 0


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "User%d" % n)
    credit = Decimal("100.00")


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    slot = factory.SubFactory(VendingMachineSlotFactory)
