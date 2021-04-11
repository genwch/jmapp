from ._template import *

# tbl = {"cols": [{"name": "txt", "control": "input", "sort": "true", "label": "text"}],
#        "data": [[{"type": "link", "url": "./", "val": "r1"}],
#                 [{"type": "button", "act": "location.href='{}';".format(
#                     "./"), "val": "r3"}],
#                 [{"type": "checkbox", "val": True}],
#                 [{"val": "r2"}]],
#        "id": "tbl_a"}


class job_mod(model_template):

    def set_type(self):
        self.type = "jobs"

    def set_cols(self):
        self.cols = [{"type": "hidden", "name": "jid", "label": "ID", "val": "", "uuid": True, "width": "0%"},
                     {"type": "link", "name": "job_cde", "label": "Code", "val": "", "width": "5%",
                         "url": "/job/view?jid={{jid}}", "genrun": "JD!!cnt-10!!", "key": True},
                     {"type": "text", "name": "company", "width": "5%",
                         "label": "Company", "val": "", "tbl_hide": True},
                     {"type": "text", "name": "title", "width": "50",
                         "label": "Title", "val": ""},
                     {"type": "textarea", "name": "scope", "width": "5%",
                         "label": "Scope", "val": "", "tbl_hide": True},
                     {"type": "textarea", "name": "requirement", "width": "5%",
                         "label": "Requirement", "val": "", "tbl_hide": True, "onchange": "get_job_cat(this, 'form-{}-{}');".format(self.id, "job_cat")},
                     {"type": "text", "name": "experience", "width": "5%",
                         "label": "Experience (Year)", "val": ""},
                     {"type": "text", "name": "amount", "width": "5%",
                         "label": "Amount", "val": ""},
                     {"type": "text", "name": "period", "width": "5%",
                         "label": "Period", "val": ""},
                     {"type": "moption", "name": "job_cat", "label": "Cat", "width": "5%",
                         "val": "", "opt": ["SW", "HW"]},
                     {"type": "button", "name": "edit", "label": "Edit", "val": "", "disable": "'{{appcnt}}'!='0'",
                         "visable": "'{{cre_by}}'=='{{owner}}'", "width": "5%", "url": "/job/view?edit=1&jid={{jid}}"},
                     {"type": "button", "name": "apply", "label": "Apply", "val": "", "disable": "'{{aid}}'!=''",
                      "visable": "'{{cre_by}}'!='{{owner}}' and '{{owner}}'!=''", "width": "5%", "url": "/job/apply?job_cde={{job_cde}}"},
                     {"type": "hidden", "name": "cre_by",
                         "label": "cre_by", "val": "", "width": "0%"}]
        return
