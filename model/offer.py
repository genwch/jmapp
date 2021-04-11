from ._template import *


class offer_mod(model_template):

    def set_type(self):
        self.type = "offers"

    def set_cols(self):
        self.cols = [{"type": "hidden", "name": "oid", "label": "ID", "val": "", "uuid": True},
                     {"type": "hidden", "name": "job_cde",
                         "label": "Job", "val": ""},
                     {"type": "hidden", "name": "aid",
                         "label": "Apply", "val": ""},
                     {"type": "star", "name": "rate",
                         "label": "Rate", "val": "", "maxval": "5"},
                     {"type": "hidden", "name": "cre_by",
                         "label": "", "val": "", "url": "/profile?usr_cde={{cre_by}}"}
                     #      ,
                     #  {"type": "button", "name": "offer", "label": "", "val": "", "disable": "{{oid}}",
                     #   "not_owner": True, "width": "80", "url": "./offer?job_cde={{job_cde}}"}
                     ]
        return
