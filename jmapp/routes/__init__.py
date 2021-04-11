from .home import *
from .login import *
from .job import *
from .profile import *

__route__ = [{"route": home, "prefix": "/"}, {"route": login, "prefix": "/"},
             {"route": job, "prefix": "/job"}, {"route": profile, "prefix": "/profile"}]
