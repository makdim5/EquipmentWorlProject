from src.models import UchetCompOborud


class EquipmentService:
    @staticmethod
    def fetch_all_equipment(session):
        return session.query(UchetCompOborud)

    @classmethod
    def fetch_equipment_by_otdel_and_rabmesto(cls, session, otdel, rabmesto):
        return cls.fetch_all_equipment(session). \
                filter_by(Otdel=otdel, RabocheeMesto=rabmesto).first()

