from src.models import UchetCompOborud


class BaseService:
    @staticmethod
    def fetch_all(session, model):
        return session.query(model)


class EquipmentService(BaseService):
    @classmethod
    def fetch_equipment_by_otdel_and_rabmesto(cls, session, model, otdel, rabmesto):
        return cls.fetch_all(session, model). \
            filter_by(Otdel=otdel, RabocheeMesto=rabmesto).first()
