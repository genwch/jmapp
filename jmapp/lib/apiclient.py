import requests
from flask import abort

conf = {"host": "https://jmapi.geo.freeddns.org",
        "account": {"username": "system", "password": "system"}}


def get_token(username: str = None, password: str = None) -> str:
    from .auth import get_user
    _, usr, pwd = get_user()
    username = usr if username == None else username
    password = pwd if password == None else password
    username = conf.get("account").get(
        "username") if username == None else username
    password = conf.get("account").get(
        "password") if password == None else password
    headers = {"accept": "application/json",
               "Content-Type": "application/x-www-form-urlencoded"}
    data = {"username": username, "password": password}
    url = "{}/token".format(conf.get("host"))
    rtn = requests.post(url,
                        headers=headers, data=data)
    rtn = rtn.json()
    token = rtn.get("access_token", None)
    return token


def get_data(*args, **kwargs) -> list:
    for a in args:
        kwargs.update(a)
    usr = kwargs.get("username", None)
    pwd = kwargs.get("password", None)
    type = kwargs.get("type", None)
    code = kwargs.get("code", None)
    token = get_token(username=usr, password=pwd)
    if token == None:
        abort(401, description="Authentication failed")
    headers = {"accept": "application/json",
               "Authorization": f"Bearer {token}"}
    url = "{}/{}".format(conf.get("host"), type)
    if code != None:
        url = f"{url}/{code}"
    rtn = requests.get(url,
                       headers=headers)
    if rtn.status_code != 200:
        abort(403)
    rtn = rtn.json()
    return rtn.get("items", [])


def post_data(*args, **kwargs) -> list:
    rtn, data = post_data_with_rtn(*args, **kwargs)
    return rtn


def post_data_with_rtn(*args, **kwargs) -> list:
    for a in args:
        kwargs.update(a)
    type = kwargs.get("type", None)
    code = kwargs.get("code", None)
    data = kwargs.get("data", {})
    token = get_token()
    if token == None:
        return False
        # abort(401, description="Authentication failed")
    headers = {"accept": "application/json",
               "Authorization": f"Bearer {token}"}
    url = "{}/{}".format(conf.get("host"), type)
    if code != None:
        url = f"{url}/{code}"
    rtn = requests.post(url,
                        headers=headers, json=data)
    if rtn.status_code != 200:
        return False, None
    return True, rtn.json()
