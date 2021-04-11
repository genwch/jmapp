from ._template import *


class login_mod(model_template):
    def set_type(self):
        self.type = "users"

    def set_cols(self):
        self.cols = [{"type": "hidden", "name": "uid", "label": "Login", "val": "", "uuid": True},
                     {"type": "text", "name": "usr_cde", "label": "Login",
                         "val": "", "placeholder": "Enter Login Name"},
                     {"type": "password", "name": "password", "label": "Password", "val": "", "placeholder": "Enter Password", "md5": True}]
        return

    def set_btns(self):
        self.btns = [{"type": "submit", "name": "submit", "label": "Login"},
                     {"type": "reset", "name": "reset", "label": "Reset"}]
        return
