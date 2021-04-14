from ._template import *


class apply_pro_mod(model_template):

    def set_type(self):
        self.type = "applies"

    def set_cols(self):
        self.cols = [{"type": "hidden", "name": "aid", "label": "ID", "val": "", "uuid": True},
                     {"type": "link", "name": "job_cde",
                         "label": "Job", "val": "", "url": "/job/view?job_cde={{job_cde}}", "key": True},
                     {"type": "hidden", "name": "cre_by",
                         "label": "Applier", "val": "", "url": "/profile?usr_cde={{cre_by}}"},
                     {"type": "star", "name": "rate",
                         "label": "Rate", "val": "", "maxval": "5"}]
        # for i in range(5):
        #     self.cols.append({"type": "button", "name": f"rate{i+1}", "label": f"{i+1}", "val": "", "disable": "'{{rate}}'!=''",
        #                       "visable": "'{{cre_by}}'!='{{owner}}' and '{{oid}}'!=''", "width": "5", "url": "./offer?job_cde={{job_cde}}&aid={{aid}}&rate=%s" % (f"{i+1}")})
        # self.cols.append({"type": "button", "name": "offer", "label": "Offer", "val": "", "disable": "'{{oid}}'!=''",
        #                   "visable": "'{{cre_by}}'!='{{owner}}' and '{{offcnt}}'!='1'", "width": "80", "url": "./offer?job_cde={{job_cde}}&aid={{aid}}"})
        return
