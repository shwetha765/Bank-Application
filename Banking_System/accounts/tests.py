from django.test import TestCase
from rest_framework.test import APIClient
from unittest import mock
from rest_framework.response import Response
import json

data = {
    "account_holder_name": "Test User",
    "account_type": "Savings",
    "fathers_name": "My Father",
    "address": "My address",
    "identity_proof": 204764692414,
    "contact": "1234567890",
    "has_debit_card": "True"
}


# Create your tests here.
class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Test Case for Endpoint my-bank/account/new/
    @mock.patch("accounts.views.Response")
    @mock.patch("accounts.views.CreateAccountSerializer")
    @mock.patch("accounts.views.generate_account_data")
    def test_register_new_account(self, mock_data_create, mock_serializer, mock_response):
        # Mocking generate_account_data function and setting return value
        mock_data_create.return_value = mock.MagicMock({"name": "test", "desc": "Testing"})

        # Creating instance of Mocked Serializer and setting its functions return value
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.save.return_value = lambda: "Saved"

        # Mocking Response which will return from the view
        mock_response.return_value = Response({"message": "Account Created"})

        # Defined an API Call to the endpoint and fetched the Data
        response = self.client.post("/my-bank/account/new/", data=data, format="json")
        result = response.data

        # Writing logic for testing of the view
        mock_data_create.assert_called_once_with(data)
        mock_serializer_instance.is_valid.assert_called_once()
        mock_serializer_instance.save.assert_called_once()
        mock_response.assert_called_once()
        self.assertEqual(mock_response.return_value.data, result)

    # Testing the Login Function
    # def test_login(self):
    #     login_data = {
    #         'username': "testUser",
    #         'password': "testPassword"
    #     }
    #
    #     self.client.credentials()
    #     response = self.client.post("/my-bank/account/login/", data=login_data, format="json")
    #     self.assertTrue("token" in response.data)
    #

    # Testing for account details view
    def test_get_account_details(self):
        response = self.client.get("/my-bank/account/" + self.username)
        result = response.data
        keys = {"account_no", "account_holder_name", "account_type", 'balance'}
        self.assertEqual(result.keys(), keys)
        self.assertTrue(str(result['account_no']).isdigit())

    # def test_deposit_amount(self):
    #     deposit_data = {"balance": float(1000)}
    #     response = self.client.put("/my-bank/account/deposit/" + self.username, data=deposit_data, format="json")
    #     result = response.data
    #     keys = {"message", "balance"}
    #     self.assertEqual(result.keys(), keys)
    #     self.assertEqual(result['message'], "Amount Deposited Successfully")
    #
    # def test_transfer_amount(self):
    #     transfer_data = {
    #         "to_acc": self.account_number,
    #         "balance": float(1000)
    #     }
    #
    #     response = self.client.put("/my-bank/account/transfer/" + self.username, data=transfer_data, format="json")
    #     result = response.data
    #     keys = {"message", "avail_balance"}
    #     self.assertEqual(result.keys(), keys)
    #     self.assertEqual(result["message"], "Transaction Successful")
