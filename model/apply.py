from ._template import *


class apply_mod(model_template):

    def set_type(self):
        self.type = "applies"

    def set_cols(self):
        self.cols = [{"type": "hidden", "name": "aid", "label": "ID", "val": "", "uuid": True, "key": True},
                     {"type": "hidden", "name": "job_cde",
                         "label": "Job", "val": ""},
                     {"type": "link", "name": "cre_by",
                         "label": "Applier", "val": "", "url": "/profile?usr_cde={{cre_by}}"}]
        for i in range(5):
            self.cols.append({"type": "button", "name": f"rate{i+1}", "label": f"{i+1}", "val": "", "disable": "'{{rate}}'!=''",
                              "visable": "'{{cre_by}}'!='{{owner}}' and '{{oid}}'!=''", "width": "5", "url": "./offer?job_cde={{job_cde}}&aid={{aid}}&rate=%s" % (f"{i+1}")})
        self.cols.append({"type": "button", "name": "offer", "label": "Offer", "val": "", "disable": "'{{oid}}'!=''",
                          "visable": "'{{cre_by}}'!='{{owner}}' and '{{offcnt}}'!='1'", "width": "80", "url": "./offer?job_cde={{job_cde}}&aid={{aid}}"})
        return
