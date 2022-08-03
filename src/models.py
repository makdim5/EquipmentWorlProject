from datetime import datetime

from src import db

MODELS = ['UchetCompOborud']

t_LOG_Oborud = db.Table(
    'LOG_Oborud',
    db.Column('ID', db.Integer, nullable=False, server_default=db.FetchedValue()),
    db.Column('Login', db.String(150, 'Cyrillic_General_CI_AS')),
    db.Column('Otdel', db.String(150, 'Cyrillic_General_CI_AS')),
    db.Column('RabocheeMesto', db.String(150, 'Cyrillic_General_CI_AS')),
    db.Column('Date', db.DateTime),
    db.Column('Do', db.String(150, 'Cyrillic_General_CI_AS'))
)


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
    Date_zap = db.Column(db.DateTime, nullable=False)
    Prim = db.Column(db.Text(2147483647, 'Cyrillic_General_CI_AS'))

    def __init__(self, otdel, rab_mesto, sist_block, monitor, processor, ozu, pzu,
                 gpu, printer, matplata, blokpit, ups, date_zap, prim):
        self.Otdel = otdel
        self.RabocheeMesto = rab_mesto
        self.SistemnijBlok = sist_block
        self.Monitor = monitor
        self.Processor = processor
        self.OperPamyat = ozu
        self.PostPamyat = pzu
        self.GPU = gpu
        self.Printer = printer
        self.MatPlata = matplata
        self.BlokPitaniya = blokpit
        self.UPS = ups
        self.Date_zap = date_zap
        self.Prim = prim

    def __repr__(self):
        return f'Oborud: id = {self.ID} otdel={self.Otdel}'

    def to_dict(self):
        return {
            "ID": self.ID if self.ID else "",
            "Otdel": self.Otdel if self.Otdel else "",
            "RabocheeMesto": self.RabocheeMesto if self.RabocheeMesto else "",
            "SistemnijBlok": self.SistemnijBlok if self.SistemnijBlok else "",
            "Monitor": self.Monitor if self.Monitor else "",
            "Processor": self.Processor if self.Processor else "",
            "OperPamyat": self.OperPamyat if self.OperPamyat else "",
            "PostPamyat": self.PostPamyat if self.PostPamyat else "",
            "GPU": self.GPU if self.GPU else "",
            "Printer": self.Printer if self.Printer else "",
            "MatPlata": self.MatPlata if self.MatPlata else "",
            "BlokPitaniya": self.BlokPitaniya if self.BlokPitaniya else "",
            "UPS": self.UPS if self.UPS else "",
            "Date_zap": self.Date_zap if self.Date_zap else "",
            "Prim": self.Prim if self.Prim else ""
        }


def search_uchet(search_info: str, date_search: str):
    if date_search:
        date_search = datetime.strptime(date_search, '%Y-%m-%d')
    ls = [
        db.session.query(UchetCompOborud).filter(UchetCompOborud.Otdel.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.RabocheeMesto.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.SistemnijBlok.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.Monitor.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.Processor.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.OperPamyat.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.PostPamyat.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.GPU.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.Printer.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.MatPlata.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.BlokPitaniya.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.UPS.like(f"%{search_info}%")),
        db.session.query(UchetCompOborud).filter(UchetCompOborud.Prim.like(f"%{search_info}%"))

    ]

    return {item for query in ls for item in query}
