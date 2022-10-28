import sqlite3
from sqlalchemy import Column, ForeignKey, create_engine, Table, MetaData
from sqlalchemy import Integer, Date, String
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Regular_transaction(Base):
    __tablename__ = "regular_transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    header = Column(String)
    description = Column(String)
    day_of_month = Column(Integer)
    sum = Column(Integer, nullable=False)

class Event(Base):
    __tablename__ = "unit_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    header = Column(String)
    description = Column(String)
    date = Column(Date)
    type = Column(String)
    sum = Column(Integer, nullable=False)

class Database:
    def __init__(self):
        self.classes = {m.persist_selectable.name: m.class_ for m in Base.registry.mappers}
        self.tables = list(Base.metadata.tables.values())
        Base.metadata.drop_all()
        Base.metadata.create_all()
        self.engine = create_engine('sqlite:///my_database.db', Base.metadata)
        self.session = sessionmaker(self.engine, expire_on_commit=False)
        self.connection = self.session()


    def get_tables(self):
        return enumerate(table.name for table in self.tables)

    def add_field(self, table_num, data):
        if table_num > len(self.tables):
            return
        table_name = self.tables[table_num].name
        cls = self.classes[table_name]
        obj = cls(**data)

        with self.connection.begin():
            self.connection.add(obj)
        return True

    def get_fields(self, table_num):
        if table_num > len(self.tables):
            return
        table = self.tables[table_num]
        return [(column.name, column.type) for column in table.columns if column.name.lower() != "id"]


class UserInterface:
    def __init__(self, dbObject):
        self.db = dbObject
        self.main_menu = {}
        for num, name in self.db.get_tables():
            self.main_menu.update({num: f"{num}. Table {name}"})

    def menu_action(self, menu):
        print("Select table:")
        for _, text in menu.items():
            print(text)
        try:
            num = int(input())
        except ValueError:
            print("Incorrect input")
            return
        data = self.input_action(num)
        if data is None:
            return
        return self.db.add_field(num, data)

    def input_action(self, table_num):
        fields = self.db.get_fields(table_num)
        if fields is None:
            print("Incorrect input")
            return
        data = {}
        for data_name, data_type in fields:
            print(f"Write the field {data_name} with type {data_type}")
            value = input()
            data.update({data_name: value})
        return data

    def start_ui(self):
        while self.menu_action(self.main_menu) is None:
            pass

if __name__ == '__main__':
    database = Database()
    ui = UserInterface(database)
    ui.start_ui()
