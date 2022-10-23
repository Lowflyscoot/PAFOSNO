import sqlite3
from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy import Integer, Date, String
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from datetime import date

database = declarative_base()
engine = create_engine('sqlite:///my_database.db')


class Expence(database):
    __tablename__ = 'expences'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descriptyon = Column(String)
    date = Column(Date)
    sum = Column(Integer, nullable=False)


class UserInterface():
    def __init__(self):
        self.menu_dict = {1: ("Add regular cost", self.add_regular), 2: ("Add unit cost", self.add_unit), 3: ("Get finance situation", self.get_situation)}

    def menu_action(self):
        print("For use this stuff please enter num of function:")
        for key, text in self.menu_dict.items():
            print(f"{key}. {text[0]}")
        try:
            num = int(input())
            self.menu_dict.get(num)[1]()
        except:
            print("Incorrect input")

    def add_regular(self):
        print("I added new regular cost!")

    def add_unit(self):
        print("I Added new unit cost!")

    def get_situation(self):
        print("You situation is very bad :(")


if __name__ == '__main__':
    ui = UserInterface()
    while True:
        ui.menu_action()
    # with Session(engine) as session:
    #     expence = Expence(descriptyon = 'Viduha', date = date(2022, 11, 30), sum = 25000)
    #     session.add(expence)
    #     session.commit()
