import time
from threading import Thread
from time import sleep

from flask import url_for, request
from flask_restful import Resource
import pyodbc
from werkzeug.utils import redirect

from src import app
from src.models import MODELS
from src.utils import to_html_resource


class Intro(Resource):
    SERVER = r"MSIPYMAK\SQLEXPRESS"
    DB_NAME = "factory_info"
    DATABASES_NAMES = [
        r"IT_BASE\IT_BASE/IT_BASE",
        r"MSIPYMAK\SQLEXPRESS/factory_info"
    ]

    DATABASE_TYPE = "mssql+pyodbc"
    SQLALCHEMY_DATABASE_URI = ""

    RULES = dict()

    def get(self):
        self.reset_db_uri()
        return to_html_resource("authentication.html")

    def post(self):
        user_json = request.form.to_dict()

        if user_json["login"] and user_json["password"]:
            rules = self.define_db_rules(user_json["login"], user_json["password"])
            if rules:
                self.set_db_uri(user_json["login"], user_json["password"])

                if rules['UchetCompOborud']["SELECT"]:
                    value = redirect(url_for("oborudlistapi"))



                else:
                    value = to_html_resource("error.html", er_msg="Нет доступа к ресурсу!")


            else:
                value = to_html_resource("error.html", er_msg="Нет доступа к ресурсу!")
        else:
            value = to_html_resource("error.html", er_msg="Введены пустые данные!")
        return value

    @classmethod
    def define_db_rules(cls, user, password,
                        db_tables=MODELS,
                        server=SERVER,
                        db_name=DB_NAME):
        rules = None

        try:
            with pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};' +
                                f'SERVER={server};DATABASE={db_name};' +
                                f'UID={user};PWD={password}') as conn:
                cursor = conn.cursor()

                rules = dict()
                for db_table in db_tables:
                    operations_rules = dict()
                    for item in ["INSERT", "SELECT", "DELETE", "UPDATE"]:
                        cursor.execute(f"SELECT "
                                       f"HAS_PERMS_BY_NAME"
                                       f"('{db_table}', 'OBJECT', '{item}'); ")
                        query_result = cursor.fetchone()
                        if query_result[0] is not None:
                            operations_rules[item] = query_result[0]

                    rules[db_table] = operations_rules
                    cls.RULES = rules
        except Exception:
            pass
        return rules

    @classmethod
    def reset_db_uri(cls):
        app.config["SQLALCHEMY_DATABASE_URI"] = ""

    def set_db_uri(self, login, password):
        if login and password:
            app.config["SQLALCHEMY_DATABASE_URI"] = \
                f"{self.DATABASE_TYPE}://{login}:{password}@" \
                f"{self.DATABASES_NAMES[1]}" \
                f"?driver=SQL Server Native Client 11.0"
