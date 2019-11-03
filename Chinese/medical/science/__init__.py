  # -*- extra stuff goes here -*- 
from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
_ = MessageFactory('Chinese.medical.science')

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext import declarative
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
InputDb = "Chinese.medical.science:Input db"
ORMBase = declarative.declarative_base()
engine = create_engine('mysql://MSdba:dummypassword@127.0.0.1:3306/msdb?charset=utf8', pool_recycle=3600)
Scope_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine,expire_on_commit=False))
Session = Scope_session()

def maintain_session(session):
    "maintain sqlarchemy session"
    
#     import pdb
#     pdb.set_trace()
    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()    