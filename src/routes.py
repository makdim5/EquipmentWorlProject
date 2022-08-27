from src import api
from src.resources import AuthenticationResource, EquipmentResource, EternalNumbersResource

api.add_resource(AuthenticationResource, AuthenticationResource.URI, "/")
api.add_resource(EquipmentResource, EquipmentResource.URI)
api.add_resource(EternalNumbersResource, EternalNumbersResource.URI)


