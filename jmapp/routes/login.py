import os
from flask import Blueprint
from model import login_mod, register_mod

fname = os.path.basename(__file__).split(".")[0]
login = Blueprint(fname, __name__)
login_m = login_mod()
# login_m.add([{"usr_cde": "test", "password": "test"}])

reg_m = register_mod()

# def api_filter(data: list, filt: dict):
#     import copy
#     tmp = copy.deepcopy(data)
#     for k, v in filt.items():
#         tmp = [t for t in tmp if t.get(k) == v]
#     return tmp


# def api_data(*args, **kwargs):
#     for a in args:
#         kwargs.update(a)
#         break
#     data = [{"uid": "111", "usr_cde": "test", "password": "test"}]
#     rtn = api_filter(data, kwargs)
#     return rtn


@login.route("/login", methods=["GET"])
def get():
    from flask import render_template, request, session
    session.pop('usr_cde', None)
    session.pop('access_token', None)
    paralst = ("msg", "rurl")
    para = {p: request.args.get(p, None) for p in paralst}
    form = login_m.form()
    print(form.cols)
    return render_template("login.html.j2", obj=[{"type": "form", "obj": form}], msg=para.get("msg"), rurl=para.get("rurl", "/"))


@login.route("/login", methods=["POST"])
def post():
    from flask import redirect, request, session
    from flask_jwt_extended import create_access_token
    paralst = ("usr_cde", "password")
    para = {p: request.form.get(p, None) for p in paralst}
    rtn, _ = login_m.find(para, user={"username": para.get("usr_cde", None), "password": para.get("password", None)})
    if len(rtn) > 0:
        dt = rtn[0]
        getparalst = ("msg", "rurl")
        getpara = {p: request.args.get(p, None) for p in getparalst}
        rurl = getpara.get("rurl") if getpara.get("rurl") != None else "/"
        uid = dt.get("uid")
        usr_cde = para.get("usr_cde")
        pwd = para.get("password")
        access_token = create_access_token(identity=f"{uid};{usr_cde};{pwd}")
        session["usr_cde"] = para.get("usr_cde")
        session["access_token"] = access_token
        return redirect(rurl)
    session.pop('usr_cde', None)
    session.pop('access_token', None)
    return redirect("/login?msg={}".format("Invalid username or password"))


@login.route("/logout", methods=["GET"])
def logout_get():
    from flask import redirect, session
    session.pop('usr_cde', None)
    # session.pop('pwd', None)
    session.pop('access_token', None)
    return redirect("/")


@login.route("/reg", methods=["GET"])
def reg_get():
    from flask import render_template, request
    paralst = ("msg", "")
    para = {p: request.args.get(p, None) for p in paralst}
    form = reg_m.form()
    return render_template("register.html.j2", obj=[{"type": "form", "obj": form}], msg=para.get("msg"))


@login.route("/reg", methods=["POST"])
def reg_post():
    from flask import redirect, request, session
    from flask_jwt_extended import create_access_token
    paralst = ("usr_cde", "password")
    para = {p: request.form.get(p, None) for p in paralst}
    rtn, _ = login_m.find(para)
    if len(rtn) == 0:
        print("login add")
        rtn = login_m.add(para)
        if rtn != []:
            return redirect("/login")
        # if rtn != []:
        #     return redirect("/login")
    return redirect("/reg?msg={}".format("Invalid input"))
