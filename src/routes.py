from src import api
from src.authentification import Intro
from src.resources import OborudListApi

api.add_resource(Intro, "/")
api.add_resource(OborudListApi, "/oborud")
