from decimal import Decimal
import pytest
from apps.vending.models import Product
from apps.vending.tests.factories import ProductFactory


# This annotation (see more in section 3) is required because factories
# inheriting from DjangoModelFactory will be stored in the db.
# You can prevent this by calling the .build() method instead of
# the constructor (ProductFactory.build(name="Heidi chocolate"))
@pytest.mark.django_db
def test_product_creation():
    test_product = ProductFactory(name="Heidi chocolate", price=Decimal("5.32"))

    stored_product = Product.objects.get(id=test_product.id)

    assert stored_product == test_product
    assert stored_product.price == Decimal("5.32")
    assert stored_product.name == "Heidi chocolate"
