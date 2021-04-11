from abc import ABC, abstractmethod

from jmapp import lib


class form_mod(ABC):
    data = []

    def __init__(self, id, action, method, cols, btns):
        self.id = f"form-{id}"
        self.action = action
        self.method = method
        self.cols = cols
        self.btns = btns

    def __str__(self):
        return str(self.data)


class table_mod(ABC):
    data = []

    def __init__(self, id, cols):
        self.id = f"tbl-{id}"
        self.cols = cols

    def __str__(self):
        return str(self.data)


class model_template(ABC):

    def __init__(self, data: list = None):
        self.data = []
        self.form_cols_attr = ["type", "name", "label",
                               "val", "placeholder", "readonly", "opt", "maxval", "onchange"]
        self.table_cols_attr = ["type", "name",
                                "label", "val", "url", "act", "isown", "disable", "width", "maxval", "visable"]

        self.set_id()
        self.set_action()
        self.set_method()
        self.set_owner_col()
        self.set_type()
        self.set_cols()
        self.set_btns()
        self.check_owner = [c.get("name")
                            for c in self.cols if c.get("check_owner", False)]
        self.not_owner = [c.get("name")
                          for c in self.cols if c.get("not_owner", False)]
        if isinstance(data, type(None)):
            data = []
        self.add(data)
        self.table_temp = table_mod(id=self.id, cols=self.cols)
        self.init_form()
        self.init_table()

    def init_form(self):
        self.form_temp = None
        self.form_temp = form_mod(
            id=self.id, action=self.action, method=self.method, cols=self.cols, btns=self.btns)

    def init_table(self):
        self.table_temp = None
        self.table_temp = table_mod(id=self.id, cols=self.cols)

    def set_id(self):
        self.id = self.__class__.__name__
        pass

    def set_type(self):
        self.type = self.__class__.__name__
        pass

    def set_action(self):
        self.action = "#"
        pass

    def set_owner_col(self):
        self.owner_col = "upd_by"
        pass

    def set_method(self):
        self.method = "POST"
        pass

    def set_cols(self):
        self.cols = []
        pass

    def get_opts(self):
        import copy
        rtn = []
        cols = copy.deepcopy(self.cols)
        for c in cols:
            if c.get("type") in ["moption"]:
                opt = c.get("opt", [])
                for d in self.data:
                    for k, v in d.items():
                        if k == c.get("name"):
                            topts = v.split(";")
                            opt += topts
                opt = list(set(opt))
                rtn.append({"name": c.get("name"), "opts": opt})
        return rtn

    def set_btns(self):
        self.btns = [{"type": "submit", "name": "submit", "label": "Submit", "readonly": False},
                     {"type": "reset", "name": "reset",
                         "label": "Reset", "readonly": False},
                     {"type": "button", "name": "back", "label": "Back", "act": "window.history.back();", "always": True}]
        pass

    def __str__(self):
        return str(self.data)

    def table(self, filt: dict = {}, owner: str = None, join: list = [], title: str = None):
        def nest_repl(data, val):
            import re
            for k, v in data.items():
                if isinstance(val, int):
                    val = str(val)
                if isinstance(v, int):
                    v = str(v)
                # print(k, v, val, type(v), type(val))
                if isinstance(v, str) and isinstance(val, str):
                    val = val.replace("{{%s}}" % (k), v)
            if isinstance(val, str):
                val = re.sub("{{(.*)}}", "", val)
            return val

        def join_dt(cols, data, join):
            if join == ():
                return (cols, data)
            key = [c.get("name") for c in cols if c.get("key", False)]
            tmp = []
            for d in data:
                for k in key:
                    for j in join[1]:
                        jcols = [{"type": "hidden", "name": k}
                                 for k, v in j.items()]
                        if d.get(k) == j.get(k):
                            d.update(j)
                            break
                tmp.append(d)
            return (join[0], tmp)

        import copy
        self.init_table()
        data, _ = self.find(filt=filt)
        dcols = self.cols

        jcols = []
        for j in join:
            tcols, data = join_dt(dcols, data, j)
            jcols += tcols
        cols = dcols + jcols
        ndata = []
        jcolval = {j.get("name"): j.get("val") for j in jcols if j.get(
            "val", None) not in ("", None)}
        cnt = 0
        for d in data:
            ntbl_dt = []
            for cseq in cols:
                if cseq.get("tbl_hide", False):
                    continue
                ndt = copy.deepcopy(cseq)
                v = d.get(cseq.get("name"), cseq.get("val", None))
                if v != None:
                    ndt.update({"val": v})
                # print(cseq.get("name"), v)
                if cseq.get("name") in self.check_owner:
                    isown = d.get(self.owner_col, None) == owner
                    ndt.update({"isown": isown})
                if cseq.get("name") in self.not_owner:
                    notown = d.get(self.owner_col, None) != owner
                    ndt.update({"notown": notown})
                if cseq.get("visable", None) != None:
                    nd = {"owner": owner}
                    nd.update(d)
                    nd.update(jcolval)
                    nv = nest_repl(nd, cseq.get("visable"))
                    # print(cseq.get("name"), nv)
                    nv = eval(nv)
                    ndt.update({"visable": nv})
                if cseq.get("disable", None) != None:
                    nd = {"owner": owner}
                    nd.update(d)
                    nv = nest_repl(nd, cseq.get("disable"))
                    nv = eval(nv)
                    ndt.update({"disable": nv})
                if cseq.get("name") in [d.get("name") for d in dcols]:
                    ndt = {nk: nest_repl(d, nv) for nk, nv in ndt.items()}
                    if ndt.get("name") not in [d.get("name") for d in ntbl_dt]:
                        ntbl_dt.append(ndt)
            ndata.append(ntbl_dt)
            cnt += 1
        self.table_temp.data = ndata
        cols = []
        for c in dcols:
            if c.get("tbl_hide", False):
                continue
            cols.append({k: v for k, v in c.items()
                         if k in self.table_cols_attr})
        self.table_temp.cols = cols
        if title != None:
            self.table_temp.title = title
        return self.table_temp

    def form(self, filt: dict = {}):
        self.init_form()
        dt, _ = self.find(filt=filt)
        data = {}
        for d in dt:
            data = d
            break
        if filt == {}:
            data = {}
        if data == {} and filt != {}:
            data.update(filt)
        cols = []
        tcol = self.cols.copy()
        for c in tcol:
            c.update({"val": ""})
            if data != {}:
                c.update({"val": v for k, v in data.items()
                          if k == c.get("name")})
            if c.get("uuid", False):
                c.update({"readonly": True})
            elif c.get("genrun", None) != None:
                c.update({"readonly": True})
            opt = c.get("opt", [])
            if opt != []:
                c.update({"opt": list(set(opt))})
            cols.append({k: v for k, v in c.items()
                         if k in self.form_cols_attr})
        self.form_temp.cols = cols
        return self.form_temp

    def add(self, record):
        if not(isinstance(record, list)):
            record = [record]
        for r in record:
            rtn = lib.post_data(type=self.type, data=r)
            if not(rtn):
                return []
        return record

    def refresh(self, username: str = None, password: str = None):
        if username != None and password != None:
            self.data = lib.get_data(
                type=self.type, username=username, password=password)
        else:
            self.data = lib.get_data(type=self.type)

    def set_md5(self, val):
        import hashlib
        return hashlib.md5(val.encode()).hexdigest()

    def find(self, filt, user: dict = {}):
        import copy
        if dict == {}:
            self.refresh()
        else:
            self.refresh(username=user.get("username"),
                         password=user.get("password"))
        if not(isinstance(filt, list)):
            filt = [filt]
        rtn_data = []
        for f in filt:
            data = copy.deepcopy(self.data)
            for k, v in f.items():
                col = [c for c in self.cols if c.get("name") == k]
                if col != []:
                    if col[0].get("md5", False):
                        v = self.set_md5(v)
                data = [d for d in data if d.get(k, None) == v]
            rtn_data += [d for d in data if d not in rtn_data]
        idx = [self.data.index(d) for d in rtn_data]
        return data, idx

    def rm(self, record):
        if not(isinstance(record, list)):
            record = [record]
        for r in record:
            _, idx = self.find(r)
            data = [d for i, d in enumerate(self.data) if i not in idx]
            self.data = data
        return self.data

    def cnt(self):
        return len(self.data)

    def autogen(self, data):
        if not(isinstance(data, list)):
            data = [data]
        rtn = []
        for d in data:
            for c in self.cols:
                if d.get(c.get("name"), None) == None or d.get(c.get("name"), "") == "":
                    if c.get("uuid", False):
                        d[c.get("name")] = self.uuid()
                    elif c.get("genrun", None) != None:
                        d[c.get("name")] = self.genrun(mask=c.get("genrun"))
            rtn.append(d)
        return rtn

    def uuid(self):
        from uuid import uuid4
        return str(uuid4())

    def genrun(self, mask):
        try:
            cnt = self.cnt()+1
            nmask = mask.split("!!")
            genpat = nmask[1].split("-")
            if genpat[0] == "cnt":
                runnum = str(cnt).zfill(int(genpat[1]))
                rtn = "{}{}{}".format(nmask[0], runnum, nmask[2])
            else:
                rtn = mask
        except:
            rtn = mask
        return rtn
