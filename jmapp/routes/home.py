import os
from flask import Blueprint
from jmapp.lib.auth import jwt_required

from model import job_mod, apply_mod

fname = os.path.basename(__file__).split(".")[0]
home = Blueprint(fname, __name__)

# job_m = job_mod()
# apply_m = apply_mod()


@home.route("/", methods=["GET"])
def home_get():
    from flask import render_template
    return render_template("home.html.j2")
# def home_get():
#     from flask import render_template, session
#     owner = session.get("usr_cde", None)
#     obj=[]
#     if owner!=None:
#         app_tbl = apply_m.table(filt={"cre_by": owner}, owner=owner, title="Apply list")
#         app_dt, _ = apply_m.find({"cre_by": owner})
#         cols = ["aid", "job_cde"]
#         app_col = [c for c in apply_m.cols if c.get("name") in cols]
#         app_dt = [{k: v for k, v in d.items() if k in cols} for d in app_dt]
#         join = [(app_col, app_dt)]

#         tbl = job_m.table(owner=owner, join=join, title="Job list")
#         opts = job_m.get_opts()
#         obj.append({"type": "tbl", "obj": tbl, "opts": opts})
#         obj.append({"type": "tbl", "obj": app_tbl})
#     else:
#         tbl = job_m.table(title="Job list")
#         opts = job_m.get_opts()
#         obj.append({"type": "tbl", "obj": tbl, "opts": opts})

#     return render_template("index.html.j2", obj=obj)
#         # return render_template("index.html.j2")
