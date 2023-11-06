import pytest
import requests


class TestLanguageToolAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = "https://api.languagetoolplus.com/v2/check"
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.data = {
            "text": "Helo darknes my old frend",
            "language": "en-US",
            "enabledOnly": "false",
        }

    def test_smoke_check(self):
        response = requests.post(
            self.url, headers=self.headers, data=self.data
        )
        assert response.status_code == 200

    def test_errors(self):
        response = requests.post(
            self.url, headers=self.headers, data=self.data
        )
        matches = [i for i in response.json()["matches"]]
        assert matches[0]["shortMessage"] == "Spelling mistake"
