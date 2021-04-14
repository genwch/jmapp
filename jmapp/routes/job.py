import os
from flask import Blueprint
from jmapp.lib.auth import jwt_required

from model import job_mod, apply_mod, offer_mod

fname = os.path.basename(__file__).split(".")[0]
job = Blueprint(fname, __name__)

job_m = job_mod()
apply_m = apply_mod()
offer_m = offer_mod()


@job.route("/", methods=["GET"])
@jwt_required
def job_get():
    from flask import render_template, session
    owner = session.get("usr_cde", None)
    app_tbl = apply_m.table(owner=owner)
    app_dt, _ = apply_m.find({"cre_by": owner})
    cols = ["aid", "job_cde"]
    app_col = [c for c in apply_m.cols if c.get("name") in cols]
    app_dt = [{k: v for k, v in d.items() if k in cols} for d in app_dt]
    app_col.append({"type": "text", "name": "appcnt", "val": ""})
    join = [(app_col, app_dt)]

    tbl = job_m.table(owner=owner, join=join, title="Job list")
    opts = job_m.get_opts()
    return render_template("job.html.j2", obj=[{"type": "tbl", "obj": tbl, "opts": opts}], newbtn=True)


@job.route("/view", methods=["GET"])
def job_view_get():
    from flask import render_template, request, session
    owner = session.get("usr_cde", None)
    paralst = ("msg", "jid", "edit", "job_cde")
    para = {p: request.args.get(p, None) for p in paralst}
    if para.get("jid", None)==None and para.get("job_cde", None)!=None:
        filt = {"job_cde": para.get("job_cde", None)}
        print(filt)
        form = job_m.form(filt=filt)
        print(form)
    else:
        filt = {"jid": para.get("jid", None)} if para.get(
            "jid", None) != None else {}
    form = job_m.form(filt=filt)
    readonly = True if para.get("edit", "0") != "1" else False
    form.readonly = readonly
    obj = [{"type": "form", "obj": form}]
    jcde = None
    for j in [c.get("val") for c in form.cols if c.get("name") == "job_cde"]:
        jcde = j
        break
    creby = None
    for j in [c.get("val") for c in form.cols if c.get("name") == "cre_by"]:
        creby = j
        break
    if jcde != None:
        off_dt, _ = offer_m.find({"job_cde": jcde})
        if creby == owner:
            # if para.get("edit", "0") == "1":
            cols = ["oid", "aid", "rate"]
            off_col = [c for c in offer_m.cols if c.get("name") in cols]
            # print(off_dt)
            tdt = []
            for d in off_dt:
                dt = {k: v for k, v in d.items() if k in cols}
                dt.update({"offcnt": str(len(off_dt))})
                tdt.append(dt)
            off_dt = tdt
            print(off_dt)
            # off_dt = [{k: v for k, v in d.items() if k in cols}
            #           for d in off_dt]
            off_col.append(
                {"type": "text", "name": "offcnt", "val": str(len(off_dt))})
            join = [(off_col, off_dt)]
            app_tbl = apply_m.table(
                filt={"job_cde": jcde}, join=join, owner=owner)
            if app_tbl.data != []:
                obj.append({"type": "tbl", "obj": app_tbl})
        else:
            off_form = offer_m.form(filt={"job_cde": jcde})
            off_form.readonly = True
            if off_form.cols != []:
                aid = [c.get("val")
                       for c in off_form.cols if c.get("name") == "aid"]
                app_tbl = apply_m.table(filt={"aid": aid[0], "cre_by": owner})
                if app_tbl.data != []:
                    obj.append({"type": "form", "obj": off_form})

    return render_template("job.html.j2", obj=obj, msg=para.get("msg", None))


@job.route("/view", methods=["POST"])
def job_view_post():
    from flask import redirect, request, session
    owner = session["usr_cde"]
    args = request.args.get("jid", None)
    urlpara = "&jid={}".format(args) if args != None else ""
    filt = {"jid": args} if args != None else {}

    form = job_m.form()
    para = {k: v for k, v in request.form.items(
    ) if k in [c.get("name") for c in form.cols]}
    if filt != {}:
        para.update(filt)
    rtn = job_m.add(para)
    if rtn != []:
        return redirect("/job")

    return redirect("?msg={}{}".format("Invalid input", urlpara))


@job.route("/apply", methods=["GET"])
def job_apply_get():
    from flask import redirect, request, session
    args = request.args.get("job_cde", None)
    urlpara = "&job_cde={}".format(args) if args != None else ""
    filt = {"job_cde": args} if args != None else {}

    form = apply_m.form()
    para = {k: v for k, v in request.form.items(
    ) if k in [c.get("name") for c in form.cols]}
    if filt != {}:
        para.update(filt)
    rtn = apply_m.add(para)
    if rtn != []:
        return redirect("/job")
    return redirect("/job?msg={}".format("Apply fail"))



def byte2dict(data)->dict:
    import ast
    byte_str = data
    dict_str = byte_str.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    return mydata

@job.route("/jobcat", methods=["POST"])
def job_cat_post():
    from flask import request
    import jmapp.lib as lib
    paralst = ["job_desc"]
    rtn=byte2dict(request.data)
    para = {p: rtn.get(p, None) for p in paralst}
    rtn, data = lib.post_data_with_rtn(type="jobcat", data=para)
    if rtn:
        return data
    return {}


@job.route("/offer", methods=["GET"])
def job_offer_get():
    from flask import redirect, request, session
    paralst = ("job_cde", "aid", "rate")
    para = {p: request.args.get(p, None) for p in paralst}

    # filt = {"job_cde": para.get("job_cde"), "aid": para.get("aid")}

    # form = apply_m.form()
    # para = {k: v for k, v in request.form.items(
    # ) if k in [c.get("name") for c in form.cols]}
    # if filt != {}:
    #     para.update(filt)
    rtn = offer_m.add(para)
    return redirect("/job")
