from django.db import models

from decimal import Decimal
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    class Meta:
        db_table = "product"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=4, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VendingMachineSlot(models.Model):
    class Meta:
        db_table = "vending_machine_slot"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    row = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    column = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )


class User(models.Model):
    class Meta:
        db_table = "user"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=100)
    credit = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )


class Order(models.Model):
    class Meta:
        db_table = "order"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    slot = models.ForeignKey("VendingMachineSlot", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
