from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase): pass

class TestBase(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer)
    game_status = Column(Integer)
    game_data = Column(String)
    maximum = Column(Integer)

def open(database):
    engine = create_engine(database, echo=False)
    Base.metadata.create_all(bind=engine)
    session=Session(autoflush=False, bind=engine)
    return session

def add(session, user_id, game_status, game_data, maximum):
    element = TestBase(user_id = user_id, game_status = game_status, game_data = game_data, maximum = maximum)
    session.add(element)
    session.commit()

def remove(session, user_id):
    try:
        element = session.query(TestBase).filter(TestBase.user_id==user_id).first()
        session.delete(element)
        session.commit()
    except:
        pass

def set(session, user_id, game_status, game_data, maximum):
    element = session.query(TestBase).filter(TestBase.user_id==user_id).first()
    element.game_status = game_status
    element.game_data = game_data
    element.maximum = maximum
    session.commit()

def get(session, user_id):
    return session.query(TestBase).filter(TestBase.user_id==user_id).first()

def getbest(session):
    return session.query(func.max(TestBase.maximum)).scalar()