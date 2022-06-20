from os import environ
from urllib.parse import urlencode
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import requests
import threading

API_VERSION = "v10"

class Discord:
    def __init__(self):
        self.client_id = environ.get("DISCORD_CLIENT_ID")
        self.client_secret = environ.get("DISCORD_CLIENT_SECRET")
        self.token = environ.get("DISCORD_TOKEN")
        self.public_key = environ.get("DISCORD_PUBLIC_KEY")

    def api_request(self, endpoint):
        return f"https://discord.com/api/{API_VERSION}/{endpoint}"
    def headers(self, bearer):
        if bearer:
            return {"Authorization": f"Bearer {bearer}"}
        return {"Authorization": f"Bot {self.token}"}

    def get(self, endpoint, bearer=None) -> requests.Response:
        r = requests.get(self.api_request(endpoint), headers=self.headers(bearer))
        r.raise_for_status()
        return r
    def post(self, endpoint, json, bearer=None) -> requests.Response:
        r = requests.post(self.api_request(endpoint), headers=self.headers(bearer), json=json)
        r.raise_for_status()
        return r
    def put(self, endpoint, bearer=None) -> requests.Response:
        r = requests.put(self.api_request(endpoint), headers=self.headers(bearer))
        r.raise_for_status()
        return r
    def patch(self, endpoint, json, bearer=None) -> requests.Response:
        r = requests.patch(self.api_request(endpoint), headers=self.headers(bearer), json=json)
        r.raise_for_status()
        return r
    def delete(self, endpoint, bearer=None) -> requests.Response:
        r = requests.delete(self.api_request(endpoint), headers=self.headers(bearer))
        r.raise_for_status()
        return r

    def oauth_link(self, scopes, state, redirect_url):
        params = {
        "response_type": "code",
        "client_id": self.client_id,
        "redirect_uri": redirect_url,
        "scope": " ".join(scopes),
        "state": state
        }
        return f"https://discord.com/api/oauth2/authorize?{urlencode(params)}"

    def oauth_exchange(self, code, redirect_url) -> requests.Response:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_url
            }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        r = requests.post("https://discord.com/api/oauth2/token", headers=headers, data=data)
        r.raise_for_status()
        return r.json()
    
    def get_token_owner(self, bearer=None):
        r = self.get("users/@me", bearer=bearer)
        return r.json()

    def thread(self, function, request):
        print("starting thread")
        thread = threading.Thread(target=self.process_request, kwargs={
            "process": function,
            "request": request
        })
        thread.start()

    def process_request(self, **kwargs):
        process = kwargs.get("process")
        request = kwargs.get("request")

        process(request)
        print("thread done")

    def verify_signature(self, request):
        verify_key = VerifyKey(bytes.fromhex(self.public_key))

        signature = request.headers["X-Signature-Ed25519"]
        timestamp = request.headers["X-Signature-Timestamp"]
        body = request.data.decode("utf-8")

        try:
            verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
            return True
        except BadSignatureError:
            return False
