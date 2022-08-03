from datetime import datetime
from flask import request, url_for, render_template
from flask_restful import Resource
from sqlalchemy.exc import OperationalError, ArgumentError, ProgrammingError
from werkzeug.utils import redirect

from src import db
from src.utils import to_html_resource
from src.models import UchetCompOborud, search_uchet
from src.authentification import Intro

menu = [{"name": "Учёт оборудования", "url": "/oborud"},
        ]


class OborudListApi(Resource):
    title = "Учёт оборудования"
    table_titles = [
        "ID",
        "Отдел",
        "Рабочее место",
        "Системный блок",
        "Монитор",
        "Процессор",
        "ОЗУ",
        "ПЗУ",
        "GPU",
        "Принтер",
        "Материнская плата",
        "Блок питания",
        "UPS",
        "Дата zap",
        "Prim"
    ]

    add_option = 0
    up_option = 0
    del_option = 0

    def get(self):
        if request.is_json:
            return redirect(url_for("intro"))

        try:
            oborud = [f.to_dict() for f in db.session.query(UchetCompOborud).all()]

            self.add_option = Intro.RULES["UchetCompOborud"]["INSERT"]
            self.up_option = Intro.RULES["UchetCompOborud"]["UPDATE"]
            self.del_option = Intro.RULES["UchetCompOborud"]["DELETE"]
            return to_html_resource("oborud.html", menu=menu,
                                    oborud=oborud, title=self.title,
                                    table_titles=self.table_titles,
                                    add_option=self.add_option,
                                    up_option=self.up_option,
                                    del_option=self.del_option)
        except (ArgumentError, OperationalError, ProgrammingError):
            return to_html_resource("error.html", er_msg="Нет доступа к ресурсу!")

    def post(self):
        try:
            oborud_json = request.form.to_dict()

            if "search_info" in oborud_json.keys():
                oborud = search_uchet(oborud_json["search_info"], oborud_json["date_search"])


                return (to_html_resource("oborud.html", code=200,
                                         menu=menu,
                                         oborud=oborud,
                                         title=self.title,
                                         table_titles=self.table_titles,
                                         add_option=self.add_option,
                                         up_option=self.up_option,
                                         del_option=self.del_option)
                        if len(oborud)
                        else
                        to_html_resource("oborud.html", msg_title="Сообщение",
                                         msg=f" Ничего не найдено !",
                                         menu=menu,
                                         oborud=[f.to_dict() for f in
                                                 db.session.query(UchetCompOborud).all()],
                                         title=self.title,
                                         table_titles=self.table_titles,
                                         add_option=self.add_option,
                                         up_option=self.up_option,
                                         del_option=self.del_option))

            if not (oborud_json['Otdel'] and oborud_json['RabocheeMesto']
                    and oborud_json["Date_zap"]):
                return to_html_resource("oborud.html", code=400, msg_title="Ошибка",
                                        msg="Отправлены пустые данные!",
                                        menu=menu,
                                        oborud=[f.to_dict() for f in
                                                db.session.query(UchetCompOborud).all()],
                                        title=self.title,
                                        table_titles=self.table_titles,
                                        add_option=self.add_option,
                                        up_option=self.up_option,
                                        del_option=self.del_option)

            try:
                user = UchetCompOborud(
                    oborud_json["Otdel"],
                    oborud_json["RabocheeMesto"],
                    oborud_json["SistemnijBlok"],
                    oborud_json["Monitor"],
                    oborud_json["Processor"],
                    oborud_json["OperPamyat"],
                    oborud_json["PostPamyat"],
                    oborud_json["GPU"],
                    oborud_json["Printer"],
                    oborud_json["MatPlata"],
                    oborud_json["BlokPitaniya"],
                    oborud_json["UPS"],
                    datetime.strptime(oborud_json["Date_zap"], '%Y-%m-%d'),
                    oborud_json["Prim"]
                )
                db.session.add(user)
                db.session.commit()
            except (ValueError, KeyError):
                return to_html_resource("oborud.html", code=400, msg_title="Ошибка",
                                        msg="Отправлены неверные данные!",
                                        menu=menu,
                                        oborud=[f.to_dict() for f in
                                                db.session.query(UchetCompOborud).all()],
                                        title=self.title,
                                        table_titles=self.table_titles,
                                        add_option=self.add_option,
                                        up_option=self.up_option,
                                        del_option=self.del_option)

            return to_html_resource("oborud.html", msg_title="Сообщение",
                                    msg=f" Добавлено новое оборудование !",
                                    menu=menu,
                                    oborud=[f.to_dict() for f in
                                            db.session.query(UchetCompOborud).all()],
                                    title=self.title,
                                    table_titles=self.table_titles,
                                    add_option=self.add_option,
                                    up_option=self.up_option,
                                    del_option=self.del_option)
        except ProgrammingError:
            return "No access to add \'oborude\'!", 200

    def patch(self):
        try:
            Otdel, RabocheeMesto = request.json["Otdel"], request.json['RabocheeMesto']
            ob = db.session.query(UchetCompOborud). \
                filter_by(Otdel=Otdel).filter_by(RabocheeMesto=RabocheeMesto).first()

            if not ob:
                return {"msg_title": "Ошибка",
                        "msg": "Оборудование не найдено!"}, 404

            if not (request.json["newOtdel"] and request.json['newRabocheeMesto']):
                return {"msg_title": "Ошибка",
                        "msg": "Обновление не совершено, так вы не указали"
                               " обязательные данные: отдел и рабочее место!"}, 404

            if request.json['newOtdel']:
                ob.Otdel = request.json['newOtdel']
            if request.json['newRabocheeMesto']:
                ob.RabocheeMesto = request.json['newRabocheeMesto']

            if request.json['newSistemnijBlok']:
                ob.SistemnijBlok = request.json['newSistemnijBlok']

            if request.json['newMonitor']:
                ob.Monitor = request.json['newMonitor']

            if request.json['newProcessor']:
                ob.Processor = request.json['newProcessor']

            if request.json['newOperPamyat']:
                ob.OperPamyat = request.json['newOperPamyat']

            if request.json['newPostPamyat']:
                ob.PostPamyat = request.json['newPostPamyat']

            if request.json['newGPU']:
                ob.GPU = request.json['newGPU']

            if request.json['newPrinter']:
                ob.Printer = request.json['newPrinter']

            if request.json['newMatPlata']:
                ob.MatPlata = request.json['newMatPlata']

            if request.json['newBlokPitaniya']:
                ob.BlokPitaniya = request.json['newBlokPitaniya']

            if request.json['newUPS']:
                ob.UPS = request.json['newUPS']

            if request.json['newDate_zap']:
                ob.Date_zap = datetime.strptime(request.json['newDate_zap'], '%Y-%m-%d')

            if request.json['newPrim']:
                ob.Prim = request.json['newPrim']

            db.session.add(ob)
            db.session.commit()
            return {"msg_title": "Сообщение",
                    "msg": "Обновление совершено успешно!"}, 200
        except ProgrammingError:
            return {"msg_title": "Сообщение",
                    "msg": "Обновление не возможно!"}, 200

    def delete(self):
        try:
            Otdel, RabocheeMesto = request.json["Otdel"], request.json['RabocheeMesto']
            ob = db.session.query(UchetCompOborud). \
                filter_by(Otdel=Otdel).filter_by(RabocheeMesto=RabocheeMesto).first()

            if not ob:
                return {"msg_title": "Ошибка",
                        "msg": "Оборудование не найдено!"}, 404
            db.session.delete(ob)
            db.session.commit()
            return {"msg_title": "Сообщение",
                    "msg": "Удаление совершено успешно!"}, 200
        except ProgrammingError:
            return {"msg_title": "Сообщение",
                    "msg": "Удаление не возможно!"}, 200
