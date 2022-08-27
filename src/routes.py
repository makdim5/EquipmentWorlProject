from src import api
from src.resources import AuthenticationResource, EquipmentResource

api.add_resource(AuthenticationResource, AuthenticationResource.URI, "/")
api.add_resource(EquipmentResource, EquipmentResource.URI)
