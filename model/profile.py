from ._template import *


class profile_mod(model_template):

    def set_type(self):
        self.type = "profiles"

    def set_cols(self):
        self.cols = [{"type": "hidden", "name": "pid", "label": "ID", "val": "", "uuid": True},
                     {"type": "hidden", "name": "usr_cde", "label": "Code", "val": "",
                         "key": True},
                     {"type": "text", "name": "usr_name",
                         "label": "Name", "val": "", "placeholder": "Name"},
                     {"type": "email", "name": "email",
                         "label": "Email", "val": "", "placeholder": "Email"},
                     {"type": "textarea", "name": "usr_desc",
                         "label": "Description", "val": "", "placeholder": "Description"},
                     {"type": "text", "name": "education",
                         "label": "Education Level", "val": "", "placeholder": "Education Level"},
                     {"type": "text", "name": "qualification",
                         "label": "Qualification", "val": "", "placeholder": "Qualification"},
                     {"type": "text", "name": "work_exp",
                         "label": "Working Experience (Year)", "val": "", "placeholder": "Working Experience"},
                     {"type": "text", "name": "programing",
                         "label": "Programing", "val": "", "placeholder": "Programing"},
                     {"type": "moption", "name": "job_cat",
                         "label": "Job Cat", "val": "", "opt": ["SW", "HW"]},
                     {"type": "hidden", "name": "cre_by",
                         "label": "cre_by", "val": ""}]
        return
