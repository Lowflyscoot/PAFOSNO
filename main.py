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

        # print(*(column.type for column in self.unit_events.columns))
        # print(self.unit_events.columns)

    def add_field(self, table):
        data = {}
        for column in table.columns:
            print(column.name)
            if column.name.lower() == "id":
                continue
            print(f"Write the field {column.name} with type {column.type}")
            value = input()
            data.update({column.name: value})

            req = table.insert().values(
                **data
            )

        with self.connection.begin():
            self.connection.execute(req)

    def get_numerable_tables_dict(self):
        return {1: self.users,
                2: self.regular_incomes,
                3: self.regular_expenses,
                4: self.unit_events}



# class Expence(database):
#     __tablename__ = 'expences'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     descriptyon = Column(String)
#     date = Column(Date)
#     sum = Column(Integer, nullable=False)


class UserInterface():
    # def __init__(self, dbObject):

    def menu_action(self, db, menu):
        print("Select table:")
        for _, tuple_data in menu.items():
            print(f"{tuple_data[0]}")
        # try:
        num = int(input())
        db.add_field(menu.get(num)[1])
        # except:
        #     print("Incorrect input")
        #     self.start_ui(db)

    def start_ui(self, db):
        tables_dict = db.get_numerable_tables_dict()
        menu = {}
        for num, table in tables_dict.items():
            menu.update({num: (f"{num}. Table {table.name}", table)})
        self.menu_action(db, menu)



if __name__ == '__main__':
    ui = UserInterface()
    database = Database()
    # database.add_field(database.regular_expenses)
    # database.create_request_add_field_expense()

    ui.start_ui(database)
    # ui.cre

    # ui = UserInterface()
    # ui.menu_action()
    # with Session(engine) as session:
    #     expence = Expence(descriptyon = 'Viduha', date = date(2022, 11, 30), sum = 25000)
    #     session.add(expence)
    #     session.commit()
