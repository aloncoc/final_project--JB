from sqlalchemy import asc, text, desc
from logger import Logger
from Customers import Customer
from Users import User
from Tickets import Ticket
from Administrators import Administrator
from Airline_Companies import Airline_Company
from Flights import Flight
from Country import Country
from User_Roles import User_Role
from db_config import *
import datetime



class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session


    def reset_auto_inc(self, table_class):
        self.local_session.query(text(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE'))
        self.local_session.commit()

    def get_all(self, table_class):
        return self.local_session.query(table_class).all()

    def get_all_limit(self, table_class, limit_num):
        return self.local_session.query(table_class).limit(limit_num).all()

    def get_all_order_by(self, table_class, column_name, direction=asc):
        return self.local_session.query(table_class).order_by(direction(column_name)).all()

    def add(self, one_row):
        self.local_session.add(one_row)
        self.local_session.commit()

    def add_all(self, rows_list):
        self.local_session.add_all(rows_list)
        self.local_session.commit()

    def get_by_id(self, table_class, id):
        return self.local_session.get(table_class,id)

    def delete_by_id(self, table_class, id_column_name, id):
        self.local_session.query(table_class).filter(id_column_name == id).delete(synchronize_session=False)
        self.local_session.commit()


    def update_by_id(self, table_class, id_column_name, id_,data):
        self.local_session.query(table_class).filter(id_column_name == id_).update(data)
        self.local_session.commit()

    def get_by_column_value(self, table_class, column_name, value):
        return self.local_session.query(table_class).filter(column_name == value).all()

    def get_by_condition(self, table_class, cond):
        query_result = self.local_session.query(table_class)
        result = cond(query_result)
        return result


    def drop_all_tables(self):
        self.local_session.execute('DROP TABLE users CASCADE')
        self.local_session.execute('DROP TABLE user_roles CASCADE')
        self.local_session.execute('DROP TABLE tickets CASCADE')
        self.local_session.execute('DROP TABLE flights CASCADE')
        self.local_session.execute('DROP TABLE customers CASCADE')
        self.local_session.execute('DROP TABLE countries CASCADE')
        self.local_session.execute('DROP TABLE airline_companies CASCADE')
        self.local_session.execute('DROP TABLE administrators CASCADE')
        self.local_session.commit()



    def reset_autoinc_for_all_tables(self):
        #reset auto inc for all tables
        self.reset_auto_inc(Country)
        self.reset_auto_inc(User_Role)
        self.reset_auto_inc(User)
        self.reset_auto_inc(Administrator)
        self.reset_auto_inc(Airline_Company)
        self.reset_auto_inc(Customer)
        self.reset_auto_inc(Flight)
        self.reset_auto_inc(Ticket)
        self.local_session.commit()





    def init_db(self):
        self.drop_all_tables()
        create_all_entities()

        self.add_all([Country(id=1, name='Israel'),Country(id=2, name='Mexico'),Country(id=3, name= 'USA')])

        self.add_all([User_Role(id=1, name='Administrator'),User_Role(id=2, name= 'Customer'),User_Role(id=3, name= 'Airline_Company')])

        self.add_all([User(username='alonc', password='053212', email='alonc@gmail.com', user_role=1),
                      User(username='Liav', password='053213', email='liav@gmail.com', user_role=1),
                      User(username='Yosi', password='053214', email='Yosi@gmail.com', user_role=2),
                      User(username='Tomer', password='053215', email='Tomer@gmail.com', user_role=2),
                      User(username='Elad', password='053216', email='Elad@gmail.com', user_role=3),
                      User(username='Dan', password='053217', email='Dan@gmail.com', user_role=3),
                      User(username='rohi', password='rohi123', email= 'rohi@gmail.com',user_role= 1),
                      User(username= 'tal',password='tal1234',email= 'tal@gmail.com',user_role=3)])

        self.add_all([Administrator(first_name='Alon', last_name='Cohen', user_id=1),
                      Administrator(first_name='Liav', last_name='Michaeli', user_id=2)])

        self.add_all([Airline_Company(name='elal', country_id=1, user_id=5),
                     Airline_Company(name='klasa_airline', country_id=2, user_id=6)])

        self.add_all([Customer(first_name='Yosi', last_name='Shmaryau', address='Givatayim', phone_no='054456453', \
                             credit_card_no='52321231', user_id=3),
                      Customer(first_name='Tomer', last_name='Gil', address='Givatayim', phone_no='0544564221', \
                               credit_card_no='52321333', user_id=4)])

        self.add_all([Flight(airline_company_id=1, origin_country_id=1,
                         destination_country_id=3, departure_time=datetime.datetime(2022, 1, 30, 16, 0, 0),
                         landing_time=datetime.datetime(2022, 1, 31, 12, 0, 0),
                         remaining_tickets=150),
                      Flight(airline_company_id=2, origin_country_id=2,
                             destination_country_id=1,
                             departure_time=datetime.datetime(2022, 1, 31, 11, 0, 0),
                             landing_time=datetime.datetime(2022, 1, 31, 23, 0, 0),
                             remaining_tickets=90),
                      Flight(airline_company_id=1, origin_country_id=1,
                             destination_country_id=3, departure_time=datetime.datetime(2022, 1, 30, 16, 0, 0),
                             landing_time=datetime.datetime(2022, 1, 31, 12, 0, 0),
                             remaining_tickets=0)])



        self.add_all([Ticket(flight_id=1, customer_id=1),
                      Ticket(flight_id=2, customer_id=2)])
