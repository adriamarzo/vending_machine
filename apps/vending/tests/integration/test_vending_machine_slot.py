from decimal import Decimal
import pytest
from apps.vending.models import VendingMachineSlot
from apps.vending.tests.factories import ProductFactory, VendingMachineSlotFactory
from uuid import uuid4
from rest_framework import status
from unittest.mock import ANY


# This annotation (see more in section 3) is required because factories
# inheriting from DjangoModelFactory will be stored in the db.
# You can prevent this by calling the .build() method instead of
# the constructor (ProductFactory.build(name="Heidi chocolate"))
@pytest.mark.django_db
def test_vending_slot_set_quantity():
    test_product = ProductFactory(name="Heidi chocolate", price=Decimal("5.32"))
    test_slot = VendingMachineSlotFactory(product=test_product, quantity=15)

    stored_slot = VendingMachineSlot.objects.get(id=test_slot.id)

    assert stored_slot == test_slot
    assert stored_slot.quantity == 15
    assert stored_slot.row == 0
    assert stored_slot.column == 0


def test_invalid_quantity_filter_returns_bad_request(client):
    response = client.get("/slots/?quantity=-1")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "quantity": ["Ensure this value is greater than or equal to 0."]
    }
