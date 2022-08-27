from marshmallow import ValidationError
from sqlalchemy.exc import OperationalError, ArgumentError, ProgrammingError
from src import db
from src.models import UchetCompOborud, EternalNumbers
from flask import url_for, request
from flask_restful import Resource
from werkzeug.utils import redirect

from src.schemas import EquipmentSchema, EternalNumbersSchema
from src.services.db_manager import DBManager
from src.services.db_services import EquipmentService, EternalNumbersService
from src.services.render_utils import render_html


class AuthenticationResource(Resource):
    URI = "/authentication"

    def get(self):
        DBManager.reset_db_uri()
        return render_html("authentication.html")

    def post(self):
        user_json = request.form.to_dict()
        value = render_html("error.html", er_msg="Введены пустые данные!")
        if user_json["login"] and user_json["password"]:
            value = render_html("error.html", er_msg="Нет доступа к ресурсу!")
            rules = DBManager.define_db_rules(user_json["login"], user_json["password"])
            if rules:
                DBManager.set_db_uri(user_json["login"], user_json["password"])
                if rules['UchetCompOborud']["SELECT"]:
                    value = redirect(url_for("equipmentresource"))
        return value


class EquipmentResource(Resource):
    URI = "/equipment"
    TEMPLATE = "oborud.html"
    model = UchetCompOborud
    schema = EquipmentSchema()
    title = "Учёт оборудования"
    table_titles = [
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
    ]

    def get(self):
        try:
            equipment = EquipmentService.fetch_all(db.session, self.model)
            self.schema.dump(equipment, many=True)
            return_value = render_html(
                self.TEMPLATE, menu=menu,
                oborud=equipment,
                uri=self.URI,
                title=self.title,
                table_titles=self.table_titles,
                add_option=DBManager.RULES[self.model.__name__]["INSERT"],
                up_option=DBManager.RULES[self.model.__name__]["UPDATE"],
                del_option=DBManager.RULES[self.model.__name__]["DELETE"])
        except (ArgumentError, OperationalError, ProgrammingError):
            return_value = redirect(url_for("authenticationresource"))
        return return_value

    def post(self):
        try:
            db.session.add(self.schema.load(request.json, session=db.session))
            db.session.commit()
            return_value = {"msg_title": "Сообщение",
                            "msg": "Добавлено новое оборудование!"}, 200
        except Exception as ex:
            return_value = {"msg_title": "Ошибка",
                            "msg": str(ex)}, 400
        return return_value

    def patch(self):
        try:
            ob = EquipmentService.fetch_equipment_by_otdel_and_rabmesto(
                db.session, self.model,
                request.args["Otdel"],
                request.args['RabocheeMesto'])
            db.session.add(self.schema.load(request.json,
                                            instance=ob, session=db.session))
            db.session.commit()
            return_value = {"msg_title": "Сообщение",
                            "msg": "Обновление совершено!"}, 200
        except Exception as e:
            return_value = {"msg_title": "Ошибка",
                            "msg": str(e)}, 400
        return return_value

    def delete(self):
        return_value = {"msg_title": "Ошибка",
                        "msg": "Удаление не совершено!"}, 404
        try:
            ob = EquipmentService.fetch_equipment_by_otdel_and_rabmesto(
                db.session, self.model,
                request.json["Otdel"],
                request.json['RabocheeMesto'])

            if ob:
                db.session.delete(ob)
                db.session.commit()
                return_value = {"msg_title": "Сообщение",
                                "msg": "Удаление совершено успешно!"}, 200
        except ProgrammingError:
            pass
        return return_value


class EternalNumbersResource(Resource):
    URI = "/numbers"
    TEMPLATE = "EternalNumbers.html"
    model = EternalNumbers
    schema = EternalNumbersSchema()
    title = "Внутренние номера"
    table_titles = [
        "Абонент",
        "Номер телефона",
    ]

    def get(self):
        try:
            numbers = EternalNumbersService.fetch_all(db.session, self.model)
            self.schema.dump(numbers, many=True)
            return_value = render_html(
                self.TEMPLATE, menu=menu,
                numbers=numbers,
                uri=self.URI,
                title=self.title,
                table_titles=self.table_titles,
                add_option=DBManager.RULES[self.model.__name__]["INSERT"],
                up_option=DBManager.RULES[self.model.__name__]["UPDATE"],
                del_option=DBManager.RULES[self.model.__name__]["DELETE"])
        except (ArgumentError, OperationalError, ProgrammingError):
            return_value = redirect(url_for("authenticationresource"))
        return return_value

    def post(self):
        try:
            db.session.add(self.schema.load(request.json, session=db.session))
            db.session.commit()
            return_value = {"msg_title": "Сообщение",
                            "msg": "Добавлен новый номер!"}, 200
        except Exception as ex:
            return_value = {"msg_title": "Ошибка",
                            "msg": str(ex)}, 400
        return return_value

    def patch(self):
        try:
            ob = EternalNumbersService.fetch_number(db.session, self.model,
                                                    request.args["oldNumber"])
            db.session.add(self.schema.load(request.json,
                                            instance=ob, session=db.session))
            db.session.commit()
            return_value = {"msg_title": "Сообщение",
                            "msg": "Обновление совершено!"}, 200
        except Exception as e:
            return_value = {"msg_title": "Ошибка",
                            "msg": str(e)}, 400
        return return_value

    def delete(self):
        return_value = {"msg_title": "Ошибка",
                        "msg": "Удаление не совершено!"}, 404
        try:
            ob = EternalNumbersService.fetch_number(db.session, self.model,
                                                    request.json["Number"])

            if ob:
                db.session.delete(ob)
                db.session.commit()
                return_value = {"msg_title": "Сообщение",
                                "msg": "Удаление совершено успешно!"}, 200
        except ProgrammingError:
            pass
        return return_value


menu = [
    {"name": EquipmentResource.title, "url": EquipmentResource.URI},
    {"name": EternalNumbersResource.title, "url": EternalNumbersResource.URI},
]
