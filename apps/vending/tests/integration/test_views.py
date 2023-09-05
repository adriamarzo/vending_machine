from decimal import Decimal
from unittest.mock import ANY

import factory
import pytest
from rest_framework import status

from apps.vending.models import Product, User, VendingMachineSlot
from apps.vending.tests.factories import (
    ProductFactory,
    UserFactory,
    VendingMachineSlotFactory,
)
from django.urls import reverse
from uuid import uuid4


@pytest.fixture
def products_list() -> list[Product]:
    return [ProductFactory(name=f"Product {i}") for i in range(1, 11)]


@pytest.fixture
def slots_grid(products_list) -> list[VendingMachineSlot]:
    """returns a grid of slots of 5x2"""
    slots = []
    for row in range(1, 3):
        for column in range(1, 6):
            slot = VendingMachineSlotFactory(
                product=products_list.pop(), row=row, column=column, quantity=column - 1
            )
            slots.append(slot)
    return slots


@pytest.mark.django_db
class TestListVendingMachineSlots:
    def test_list_slots_returns_expected_response(self, client, slots_grid):
        response = client.get("/slots/")

        expected_response = [
            {
                "id": ANY,
                "quantity": 0,
                "coordinates": [1, 1],
                "product": {"id": ANY, "name": "Product 10", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 1,
                "coordinates": [2, 1],
                "product": {"id": ANY, "name": "Product 9", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 2,
                "coordinates": [3, 1],
                "product": {"id": ANY, "name": "Product 8", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 3,
                "coordinates": [4, 1],
                "product": {"id": ANY, "name": "Product 7", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 4,
                "coordinates": [5, 1],
                "product": {"id": ANY, "name": "Product 6", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 0,
                "coordinates": [1, 2],
                "product": {"id": ANY, "name": "Product 5", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 1,
                "coordinates": [2, 2],
                "product": {"id": ANY, "name": "Product 4", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 2,
                "coordinates": [3, 2],
                "product": {"id": ANY, "name": "Product 3", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 3,
                "coordinates": [4, 2],
                "product": {"id": ANY, "name": "Product 2", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 4,
                "coordinates": [5, 2],
                "product": {"id": ANY, "name": "Product 1", "price": "10.40"},
            },
        ]

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_list_slots_returns_filtered_response(self, client, slots_grid):
        response = client.get("/slots/?quantity=1")

        expected_response = [
            {
                "id": ANY,
                "quantity": 0,
                "coordinates": [1, 1],
                "product": {"id": ANY, "name": "Product 10", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 1,
                "coordinates": [2, 1],
                "product": {"id": ANY, "name": "Product 9", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 0,
                "coordinates": [1, 2],
                "product": {"id": ANY, "name": "Product 5", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 1,
                "coordinates": [2, 2],
                "product": {"id": ANY, "name": "Product 4", "price": "10.40"},
            },
        ]

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response


@pytest.fixture
def user() -> User:
    return UserFactory(username="user1")


@pytest.mark.django_db
class TestLogin:
    def test_login_returns_expected_response(self, client, user):
        response = client.post("/login/", data={"username": "user1"})

        expected_response = {
            "id": ANY,
            "username": "user1",
            "credit": "100.00",
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_login_fails_expected_response(self, client, user):
        response = client.post("/login/", data={"username": "user2"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUser:
    def test_user_credit_update_success(self, client, user):
        url = reverse("credit_view", kwargs={"user_id": user.id})
        response = client.patch(
            url, data={"credit": Decimal("200.00")}, content_type="application/json"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_user_credit_validate_error(self, client, user):
        url = reverse("credit_view", kwargs={"user_id": user.id})
        response = client.patch(
            url,
            data={"credit": Decimal("-200.00")},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_credit_update_error(self, client, user):
        url = reverse("credit_view", kwargs={"user_id": uuid4()})
        response = client.patch(
            url,
            data={"credit": Decimal("200.00")},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
class TestOrder:
    def test_create_order_expected_response(self, client, user, slots_grid):
        assert slots_grid[3].quantity == 3

        response = client.post(
            "/order/",
            data={
                "user_id": user.id,
                "product_id": slots_grid[3].product.id,
                "slot_id": slots_grid[3].id,
            },
        )

        slots_grid[3].quantity == 2

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_order_expected_out_of_stock_response(
        self, client, user, slots_grid
    ):
        response = client.post(
            "/order/",
            data={
                "user_id": user.id,
                "product_id": slots_grid[0].product.id,
                "slot_id": slots_grid[0].id,
            },
        )

        expected_response = {"error": "Product 10 is out of stock. "}

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_response

    def test_create_order_expected_not_enough_credit_response(
        self, client, user, slots_grid
    ):
        response = client.post(
            "/order/",
            data={
                "user_id": user.id,
                "product_id": slots_grid[0].product.id,
                "slot_id": slots_grid[0].id,
            },
        )

        expected_response = {"error": "Product 10 is out of stock. "}

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_response

    def test_create_order_validation_error_expected_response(
        self, client, user, slots_grid
    ):
        response = client.post(
            "/order/",
            data={
                "user_id": user.id,
                "product_id": "test",
                "slot_id": slots_grid[0].id,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_order_error_expected_response(self, client, user, slots_grid):
        response = client.post(
            "/order/",
            data={
                "user_id": user.id,
                "product_id": uuid4(),
                "slot_id": slots_grid[0].id,
            },
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
