import os
from flask import Blueprint
from jmapp.lib.auth import jwt_required

from model import apply_mod, offer_mod, profile_mod, apply_pro_mod

fname = os.path.basename(__file__).split(".")[0]
profile = Blueprint(fname, __name__)

profile_m = profile_mod()
apply_m = apply_mod()
offer_m = offer_mod()
apply_pro_m = apply_pro_mod()


@profile.route("/", methods=["GET"])
@jwt_required
def profile_get():
    from flask import render_template, session, request
    from flask import render_template, request
    paralst = ("msg", "usr_cde")
    para = {p: request.args.get(p, None) for p in paralst}
    filt = {"usr_cde": para.get("usr_cde", None)} if para.get(
        "usr_cde", None) != None else {}
    owner = session["usr_cde"]
    usr_cde = para.get("usr_cde", None)
    form = profile_m.form(filt={"usr_cde": usr_cde})
    form.readonly = owner != usr_cde
    app_tbl = apply_m.table(filt={"cre_by": usr_cde}, owner=owner)
    dt = []
    rate = []
    rate_temp = []
    tmp_off_dt=[]
    for r in app_tbl.data:
        for a in r:
            if a.get("name") == "aid":
                aid = a.get("val")
                off_form = offer_m.form(filt={"aid": aid})
                rate_temp = [
                    c for c in off_form.cols if c.get("name") == "rate"]
                tmp_off_r={c.get("name"): c.get("val") for c in off_form.cols if c.get("name") in ("job_cde", "rate")}
                if tmp_off_r != {}:
                    tmp_off_dt.append(tmp_off_r)
                for t in [c.get("val") for c in off_form.cols if c.get("name") == "rate" if c.get("val", None) not in ("", None)]:
                    rate.append(t)
                    break
    if rate != []:
        trate = 0
        for r in rate:
            trate += int(r)
        for t in rate_temp:
            t.update({"val": trate/len(rate)})
            form.cols.append(t)
            break
    obj = [{"type": "form", "obj": form}]

    cols = ["job_cde", "rate"]
    off_col = [c for c in offer_m.cols if c.get("name") in cols]
    off_dt = [{k: v for k, v in d.items() if k in cols} for d in tmp_off_dt]

    join=[(off_col, off_dt)]
    app_p_tbl=apply_pro_m.table(filt={"cre_by": usr_cde}, owner=owner, join=join)
    obj.append({"type": "tbl", "obj": app_p_tbl})

    return render_template("profile.html.j2", obj=obj, msg=para.get("msg", None))


@profile.route("/", methods=["POST"])
def profile_post():
    from flask import redirect, request, session
    owner = session["usr_cde"]
    form = profile_m.form(filt={"usr_cde": owner})
    cols = [c.get("name") for c in form.cols]
    para = {k: v for k, v in request.form.items() if k in cols}
    rtn = profile_m.add(para)
    if rtn != []:
        return redirect("/")
    return redirect("?msg={}".format("Invalid input"))
