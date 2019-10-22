# test_bumbo.py
import pytest

from api import API


def test_basic_route(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(req, resp):
            resp.text = "YOLO2"


def test_client_can_send_request(api, client):
    RESPONSE_TEXT = "This is cool"

    @api.route("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get("http://testserver/hey").text == RESPONSE_TEXT


def test_parameterised_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matt").status_code == 200
    assert client.get("http://testserver/matt").text == "hey matt"
    assert client.get("http://testserver/tom").text == "hey tom"


def test_default_404_response(client):
    response = client.get("http://testserver/doestnotexists")

    assert response.status_code == 404
    assert response.text == "Not found"


def test_alternative_route(api, client):
    response_text = "Alternative way to add route"

    def home(req, resp):
        resp.text = response_text

    api.add_route("/alternative", home)

    assert client.get("http://testserver/alternative").text == response_text
