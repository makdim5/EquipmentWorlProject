from src import db

MODELS = ['UchetCompOborud', "EternalNumbers"]


class UchetCompOborud(db.Model):
    __tablename__ = 'UchetCompOborud'

    ID = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    Otdel = db.Column(db.String(150, 'Cyrillic_General_CI_AS'), primary_key=True, nullable=False)
    RabocheeMesto = db.Column(db.String(150, 'Cyrillic_General_CI_AS'), primary_key=True, nullable=False)
    SistemnijBlok = db.Column(db.String(150, 'Cyrillic_General_CI_AS'))
    Monitor = db.Column(db.String(150, 'Cyrillic_General_CI_AS'))
    Processor = db.Column(db.String(150, 'Cyrillic_General_CI_AS'))
    OperPamyat = db.Column(db.String(150, 'Cyrillic_General_CI_AS'))
    PostPamyat = db.Column(db.String(150, 'Cyrillic_General_CI_AS'))
    GPU = db.Column(db.String(150, 'Cyrillic_General_CI_AS'))
    Printer = db.Column(db.String(150, 'Cyrillic_General_CI_AS'))
    MatPlata = db.Column(db.String(150, 'Cyrillic_General_CI_AS'))
    BlokPitaniya = db.Column(db.String(150, 'Cyrillic_General_CI_AS'))
    UPS = db.Column(db.String(150, 'Cyrillic_General_CI_AS'))

    def __init__(self, Otdel, RabocheeMesto, SistemnijBlok, Monitor, Processor, OperPamyat, PostPamyat,
                 GPU, Printer, MatPlata, BlokPitaniya, UPS):
        if Otdel and RabocheeMesto:
            (self.Otdel, self.RabocheeMesto, self.SistemnijBlok,
             self.Monitor, self.Processor, self.OperPamyat, self.PostPamyat,
             self.GPU, self.Printer, self.MatPlata, self.BlokPitaniya, self.UPS) \
                = (Otdel, RabocheeMesto, SistemnijBlok, Monitor,
                   Processor, OperPamyat, PostPamyat,
                   GPU, Printer, MatPlata, BlokPitaniya, UPS)

    def __repr__(self):
        return f'Oborud: id = {self.ID} otdel={self.Otdel}'

    @staticmethod
    def search(session, search_info: str):
        ls = [
            session.query(UchetCompOborud).filter(UchetCompOborud.Otdel.like(f"%{search_info}%")),
            session.query(UchetCompOborud).filter(UchetCompOborud.RabocheeMesto.like(f"%{search_info}%")),
            session.query(UchetCompOborud).filter(UchetCompOborud.SistemnijBlok.like(f"%{search_info}%")),
            session.query(UchetCompOborud).filter(UchetCompOborud.Monitor.like(f"%{search_info}%")),
            session.query(UchetCompOborud).filter(UchetCompOborud.Processor.like(f"%{search_info}%")),
            session.query(UchetCompOborud).filter(UchetCompOborud.OperPamyat.like(f"%{search_info}%")),
            session.query(UchetCompOborud).filter(UchetCompOborud.PostPamyat.like(f"%{search_info}%")),
            session.query(UchetCompOborud).filter(UchetCompOborud.GPU.like(f"%{search_info}%")),
            session.query(UchetCompOborud).filter(UchetCompOborud.Printer.like(f"%{search_info}%")),
            session.query(UchetCompOborud).filter(UchetCompOborud.MatPlata.like(f"%{search_info}%")),
            session.query(UchetCompOborud).filter(UchetCompOborud.BlokPitaniya.like(f"%{search_info}%")),
            session.query(UchetCompOborud).filter(UchetCompOborud.UPS.like(f"%{search_info}%")),
        ]

        return {item for query in ls for item in query}


class EternalNumbers(db.Model):
    __tablename__ = 'EternalNumbers'

    ID = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    Number = db.Column(db.String(150, 'Cyrillic_General_CI_AS'), nullable=False)
    Name = db.Column(db.String(150, 'Cyrillic_General_CI_AS'))

    def __init__(self, Number, Name):
        self.Number, self.Name = Number, Name

    def __repr__(self):
        return f'EternalNumber: {self.Number} Name={self.Name}'

    @staticmethod
    def search(session, search_info: str):
        ls = [
            session.query(EternalNumbers).filter(EternalNumbers.Name.like(f"%{search_info}%")),
            session.query(EternalNumbers).filter(EternalNumbers.Number.like(f"%{search_info}%")),

        ]

        return {item for query in ls for item in query}
