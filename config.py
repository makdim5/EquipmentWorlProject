class Config:
    # SQLALCHEMY_DATABASE_URI = r"mssql+pyodbc://MSIPYMAK\SQLEXPRESS/factory_info?driver=SQL Server Native Client 11.0"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://PIS:852*258@IT_BASE\IT_BASE/IT_BASE?driver=SQL Server Native Client 11.0"
    DATABASES_NAMES = [
        r"IT_BASE\IT_BASE/IT_BASE",
        r"MSIPYMAK\SQLEXPRESS/factory_info"
    ]

    DATABASE_TYPE = "mssql+pyodbc"
    SQLALCHEMY_DATABASE_URI = ""

    @classmethod
    def set_uri(cls, login, password):
        # cls.SQLALCHEMY_DATABASE_URI = f"{cls.DATABASE_TYPE}://{login}:{password}@" \
        #                               f"{cls.DATABASES_NAMES[0]}" \
        #                               f"?driver=SQL Server Native Client 11.0"

        cls.SQLALCHEMY_DATABASE_URI = r"mssql+pyodbc://PIS:852*258@IT_BASE\IT_BASE/IT_BASE?driver=SQL Server Native Client 11.0"


"""
in Windows 11 cmd write 

python -m sqlacodegen.main --flask --outfile models.py "mssql+pyodbc://sa:Oreo2021@MSIPYMAK\SQLEXPRESS/factory_info?driver=SQL Server Native Client 11.0"

to get all ORMs from db "factory_info" in MS SQL Server

"""
