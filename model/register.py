from ._template import *


class register_mod(model_template):
    def set_type(self):
        self.type = "users"

    def set_cols(self):
        self.cols = [{"type": "text", "name": "usr_cde", "label": "Login", "val": "", "placeholder": "Enter Login Name"},
                     {"type": "password", "name": "password", "label": "Password",
                         "val": "", "placeholder": "Enter Password"},
                     {"type": "password", "name": "c_password", "label": "Confirm Password", "val": "", "placeholder": "Confirm Password"}]
        return

    def set_btns(self):
        self.btns = [{"type": "submit", "name": "submit", "label": "Register"},
                     {"type": "reset", "name": "reset", "label": "Reset"}]
        return
