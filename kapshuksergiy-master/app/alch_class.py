from sqlalchemy import create_engine , Column , Integer , String , DateTime , MetaData , ForeignKey , ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import datetime

from .const import db_url

Base = declarative_base()
Session = sessionmaker()
metadata = MetaData()

engine = create_engine(db_url)
Session.configure(bind=engine)

session = Session()


class Inf_Train (Base):
    __tablename__ = 'inf_train'
 
    id_train = Column(Integer, primary_key = True)
    station_departure = Column(String)
    station_arrival = Column(String)
    date_departure = Column (DateTime)
    date_arrival = Column(DateTime)

    def __init__(self , station_departure , station_arrival , date_departure , date_arrival):
        self.station_departure = station_departure 
        self.station_arrival = station_arrival 
        self.date_departure = date_departure 
        self.date_arrival = date_arrival
    def __repr__(self):
        return "<Inf_Train({}, {}, {}, {}, {})>".format(self.id_train, self.station_departure, self.station_arrival,
         self.date_departure, self.date_arrival)


class Wagons (Base):
    __tablename__ = 'wagons'

    id_wagons = Column(Integer, primary_key = True)
    train = Column('train',ForeignKey('inf_train.id_train'),primary_key=True)
    type_wagon = Column(String)
    free_places = Column(ARRAY(Integer))

    def __init__(self , train , id_wagons , type_wagon , free_places ):
        self.train = train
        self.id_wagons = id_wagons
        self.type_wagon = type_wagon 
        self.free_places = free_places 
    def __repr__(self):
         return "<({}, {}, {})>" .format (self.id_wagons,
         self.type_wagon, self.free_places)


class Users(Base):
    __tablename__ = 'users'

    id_u = Column(String,primary_key = True)
    id_t = Column(Integer,primary_key = True)
    id_w = Column(Integer,primary_key = True)
    station_d = Column(String)
    station_a = Column(String)
    date_d = Column (DateTime)
    date_a = Column(DateTime)
    type_w = Column(String)
    places = Column(Integer,primary_key = True)

    def __init__(self,id_u,id_t,id_w,station_d,station_a,date_d,date_a,type_w,places):
        self.id_u = id_u
        self.id_t = id_t
        self.id_w = id_w
        self.station_d = station_d
        self.station_a = station_a
        self.date_d = date_d
        self.date_a = date_a
        self.type_w = type_w
        self.places = places
    def __repr__(self):
        return "\n\nВи замовили білет на потяг № {} {} - {},\nДата відправлення  {}  Дата прибуття {} \nТип Вагону '{}' Вагон № {} Місце № {}" .format(self.id_t,self.station_d,self.station_a,self.date_d,self.date_a,self.type_w,self.id_w,self.places)
    
# Base.metadata.create_all(bind=engine)
# Session.configure(bind=engine)

# session = Session()

def select_train_wagon_by_id(idd_train):
    if type(idd_train) == int:
        print(session.query(Inf_Train).filter(Inf_Train.id_train == idd_train).all())
        print(session.query(Wagons).filter(Wagons.train == idd_train).all())
    else: return 'Нет такого поезда'

def select_wagon_places_by_id(idd_train):
    return session.query(Wagons.free_places,Wagons.type_wagon).filter(Wagons.train == idd_train).all()

def add_wagons(idd_train, idd_wagons, type_wagons, array1):
    for i in session.query(Wagons.id_wagons).filter( Wagons.train ==  int(idd_train)).all():
        if i == int(idd_wagons):
            print('Такой вагон уже существует')
            return
    if array1 == []:
        print('Вагон не может быть пустым')
        return
    # for i in array1:
    #     if i >= 40 or i <= 0 :
    #         print('Хреновые места ')
    #         return    
    add_wagon = Wagons(idd_train , idd_wagons , type_wagons , array1)
    session.add(add_wagon)
    session.commit()

def delete_wagone(idd_train , idd_wagons):

    engine.execute("Delete From Wagons "
                   " Where Wagons.train = {} AND Wagons.id_wagons = {}".format(idd_train , idd_wagons))

   


def ticket_purchase (idd_train, idd_wagons,number):
    # select_train_wagon_by_id(idd_train)
    array1 = session.query(Wagons.free_places,Wagons.type_wagon).filter( Wagons.train == idd_train , Wagons.id_wagons == idd_wagons).one()
    array2 = [] 

    for num in array1.free_places:  
        if num != number:
            array2.append(num)

        else: 
              pass

    delete_wagone(idd_train, idd_wagons)
    add_wagons(idd_train, idd_wagons,array1.type_wagon,array2)
    session.commit()

def ticket_add (idd_train, idd_wagons,number):
    # select_train_wagon_by_id(idd_train)
    array1 = session.query(Wagons.free_places,Wagons.type_wagon).filter( Wagons.train == idd_train , Wagons.id_wagons == idd_wagons).one()
     
    array1.free_places.append(number)

    delete_wagone(idd_train, idd_wagons)
    # print(array1)
    add_wagons(idd_train, idd_wagons,array1.type_wagon,array1.free_places)
    session.commit()

def add_train(station_departure,station_arrival,date_departure,date_arrival):
    
    ad_train = Inf_Train(station_departure , station_arrival , date_departure , date_arrival)
    session.add(ad_train)
    session.commit()
    select_train_wagon_by_id(ad_train.id_train)
    

def delete_train(idd_train):

    for i in session.query(Wagons.id_wagons).filter(Wagons.train == idd_train).all():
        
        delete_wagone(idd_train,i[0])

    engine.execute("Delete From Inf_Train "
                   " Where Inf_Train.id_train = {} ".format(idd_train ))

def select_station_deprt():
    return session.query(Inf_Train.station_departure).all()

def select_station_arrival():
    return session.query(Inf_Train.station_arrival).all()

def select_date(station_d , station_a):
    return session.query(Inf_Train.date_departure, Inf_Train.date_arrival).filter(Inf_Train.station_departure == station_d,Inf_Train.station_arrival == station_a).all()

def select_id_by_station(station_d , station_a):
    return session.query(Inf_Train.id_train).filter(Inf_Train.station_departure == station_d, Inf_Train.station_arrival == station_a).all()

def select_train_by_date(date_d,station_d,station_a):
    return session.query(Inf_Train.id_train,Inf_Train.date_departure,Inf_Train.date_arrival).filter(func.date(Inf_Train.date_departure) == date_d, Inf_Train.station_departure == station_d, Inf_Train.station_arrival == station_a ).all()

def select_date_by_id_statio(idd_train,station_d,station_a):
    return session.query(Inf_Train.date_departure,Inf_Train.date_arrival).filter(Inf_Train.id_train == idd_train , Inf_Train.station_departure == station_d , Inf_Train.station_arrival == station_a).all()

def select_free_places(idd_train,idd_wagon):
    return session.query(Wagons.free_places).filter(Wagons.train == idd_train, Wagons.id_wagons == idd_wagon).one()

def select_wagon_by_id_type(idd_train,type_wagons):
    return session.query(Wagons.id_wagons).filter(Wagons.train == idd_train, Wagons.type_wagon == type_wagons ).all()


def add_users(id_us,id_tr,id_wa,station_de,station_ar,date_de,date_ar,type_wa,placess):
    add_user = Users(id_us,id_tr,id_wa,station_de,station_ar,date_de,date_ar,type_wa,placess)
    session.add(add_user)
    session.commit()

def select_users_ticket(users_idd):
    array_user_t = session.query(Users).filter(Users.id_u == users_idd).all()
    return array_user_t

# print(select_wagon_by_id_type(11,'Плацкарт'))

# print(select_free_places(11,1)[0])

# print(select_train_by_date(datetime.date(2500,3,5),'Львів','Днепр'))

# print(select_users_ticket('1136622274'))

# print(select_date('Київ','Хмельницьк'))
# print([i[0].date() for i in select_date('Львів','Днепр')])
# print(select_id_by_station('Київ', 'Хмельницьк'))
# print(select_date_by_id_statio(10 ,'Львів','Днепр' ))
# select_station_deprt()
# print(select_date_by_id_statio(11,'Днепр','Київ'))
# print(session.query(Wagons.id_wagons).filter(Wagons.train == 4).all())
# delete_train(1)
# array1 = session.query(Wagons.free_places,Wagons.type_wagon).filter( Wagons.train == 4 , Wagons.id_wagons == 3).one()
# print(array1)
# print(array1.type_wagon)

# ticket_purchase(4,3,4)
# ticket_purchase(11,1,1)
# print(select_wagon_places_by_id(11))
# add_wagons(14,7,'Плацкарт',[1,2,3,4,5,6,10,11])
# add_wagons(1,8,'Плацкарт',[1,3,6,9,17,18])
# add_wagons(3,7,'Купе',[1,3,6,9,11,15,18])
# add_train("Днепр","Львів",datetime.datetime(2020,6,24,8,10),datetime.datetime(2020,6,24,14,50))
# add_train("Київ","Хмельницьк",datetime.datetime(2020,6,15,23,50),datetime.datetime(2020,6,17,7,0))
# engine = create_engine("postgresql://postgres:qwer@localhost:5432/Teleg")
# Base.metadata.create_all(bind=engine)
# Session.configure(bind=engine)

# session = Session()


# add_wagons(4,2,'Пласкард',[ 1 , 2 , 4 , 5 , 6 , 7])
# add_wagons(4, 3, "dgf", [1,3,4,5,6,7])
# one_wagon = Wagons( 5 , 1, 'Пласкард', [ 1 , 2 , 3 ])
# session.add(one_wagon)
# delete_wagone(3,7)

# print(session.query(Inf_Train).filter_by(station_departure = 'wew').first())
# select_station_deprt()
# select_id(4)
# session.commit()

# print(Base.metadata.tables)
