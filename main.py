import sqlite3
from sqlalchemy import Column, ForeignKey, create_engine, Table, MetaData
from sqlalchemy import Integer, Date, String
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from datetime import date


class Database():
    def __init__(self):
        self.meta = MetaData()
        self.users = Table("Users", self.meta,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("username", String, nullable=False),
            Column("password", String, nullable=False)
        )
        self.regular_incomes = Table("regular_incomes", self.meta,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("user_id", String),
            Column("header", String),
            Column("description", String),
            Column("day_of_month", Integer),
            Column("sum", Integer, nullable=False)
        )
        self.regular_expenses = Table("regular_expenses", self.meta,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("user_id", String),
            Column("header", String),
            Column("description", String),
            Column("day_of_month", Integer),
            Column("sum", Integer, nullable=False)
        )
        self.unit_events = Table("unit_events", self.meta,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("user_id", String),
            Column("header", String),
            Column("description", String),
            Column("date", Date),
            Column("type", String),
            Column("sum", Integer, nullable=False)
        )
        self.engine = create_engine('sqlite:///my_database.db')
        self.meta.create_all(self.engine)
        self.connection = self.engine.connect()

        print(*(column.type for column in self.unit_events.columns))
        # print(self.unit_events.columns)

    def add_field(self, table):
        data = {}
        for column in table.columns:
            if column.name.lower() == "id":
                continue
            print(f"{column.name} {column.type}")
            value = input()
            data.update({column.name: value})

            req = table.insert().values(
                **data
            )

        with self.connection.begin():
            self.connection.execute(req)

    def create_request_add_field_income(self):
        req = self.regular_incomes.insert().values(
            user="Scoot",
            header="salary",
            description="typical salary",
            day_of_month=5,
            sum=31000
        )
        with self.connection.begin():
            self.connection.execute(req)

    def create_request_add_field_expense(self):
        req = self.regular_expenses.insert().values(
            user="Scoot",
            header="rent",
            description="typical rent",
            day_of_month=12,
            sum=14000
        )
        with self.connection.begin():
            self.connection.execute(req)

    def create_request_add_field_event(self):
        req = self.unit_events.insert().values(
            user="Scoot",
            header="shaverma",
            description="typical shaverma",
            date=date(2022, 10, 25),
            type="expence",
            sum=250
        )
        with self.connection.begin():
            self.connection.execute(req)

# class Expence(database):
#     __tablename__ = 'expences'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     descriptyon = Column(String)
#     date = Column(Date)
#     sum = Column(Integer, nullable=False)


# class UserInterface():
#     def __init__(self, dbObject):
#         self.main_menu = {
#             1: ("Regular expenses options...", dbObject.),
#             2: ("Regular incomes options...", ),
#             3: ("Unit events options...", )
#         }
#
#         self.table_menu = {
#             1: ("Add new row", ),
#             2: ("Delete row", ),
#             3: ("Show all rows", )
#         }
#
#
#
#     def menu_action(self, menu):
#         print("Pls select function:")
#         for key, text in menu.items():
#             print(f"{key}. {text[0]}")
#         try:
#             num = int(input())
#             menu.get(num)[1]()
#         except:
#             print("Incorrect input")
#
#     def start_ui(self):
#         self.menu_action(self.main_menu)



if __name__ == '__main__':
    # ui = UserInterface()
    database = Database()
    database.add_field(database.regular_expenses)
    # database.create_request_add_field_expense()

    # ui.start_ui()
    # ui.cre

    # ui = UserInterface()
    # ui.menu_action()
    # with Session(engine) as session:
    #     expence = Expence(descriptyon = 'Viduha', date = date(2022, 11, 30), sum = 25000)
    #     session.add(expence)
    #     session.commit()
