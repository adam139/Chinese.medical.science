#-*- coding: UTF-8 -*-

import sqlalchemy.schema
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import mysql
from sqlalchemy import Column, String, Integer, Date, Table
from datetime import datetime
from zope import schema
from zope.interface import Interface,implements

from xChinese.medical.science import ORMBase as Base
from Chinese.medical.science import _


###药味
class IYaoWei(Interface):
    """wu wei:
    酸、苦、甘、辛、咸
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    wei = schema.TextLine(
            title=_(u"wu wei qizhong zhi yiwei"),
        ) 
       

class YaoWei(Base):
    
    implements(IYaoWei)
    __tablename__ = 'yaowei'

    id = Column(Integer, primary_key=True)
    wei = Column(String)    

    def __init__(self, wei):
        self.wei = wei


###药性
class IYaoXing(Interface):
    """药性:
    大热、热、平、大寒、寒
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    xing = schema.TextLine(
            title=_(u"yao xing"),
        ) 
       

class YaoXing(Base):
    
    implements(IYaoXing)
    __tablename__ = 'yaoxing'

    id = Column(Integer, primary_key=True)
    xing = Column(String)    

    def __init__(self, xing):
        self.xing = xing
 
        
### 经络
class IJingLuo(Interface):
    """经络:
    足太阳膀胱经、足少阳胆经等
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    mingcheng = schema.TextLine(
            title=_(u"ming cheng"),
        ) 
       

class JingLuo(Base):
    
    implements(IJingLuo)
    __tablename__ = 'jingluo'

    id = Column(Integer, primary_key=True)
    mingcheng = Column(String)    

    def __init__(self, mingcheng):
        self.mingcheng = mingcheng
       

###药
class IYao(Interface):
    """中药:
    人参、白术、甘草
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    wei_id = schema.Int(
            title=_(u"foreagn key link to wei"),
        ) 
    xing_id = schema.Int(
            title=_(u"foreagn key link to yao xing"),
        )       
    mingcheng = schema.TextLine(
            title=_(u"ming cheng"),
        )
    zhuzhi = schema.TextLine(
            title=_(u"zhu zhi"),
        )
    guijing = schema.Object(
            title=_(u"gui jing"),
            schema=IJingLuo,
        )
        
        
class Yao(Base):
    
    implements(IYao)    
    __tablename__ = 'yao'

    id = Column(Integer, primary_key=True)
    yaowei_id = Column(Integer, ForeignKey('yaowei.id'))
    yaoxing_id = Column(Integer, ForeignKey('yaoxing.id'))
    mingcheng = Column(String)
    zhuzhi = Column(String)
    guijing = relationship("JingLuo", secondary=Yao_JingLuo_Asso)    

    def __init__(self, mingcheng,zhuzhi):
        self.mingcheng = mingcheng
        self.zhuzhi = zhuzhi

 
 ###药和经络关联表
Yao_JingLuo_Asso = Table(
    'yao_jingluo', Base.metadata,
    Column('yao_id', Integer, ForeignKey('yao.id')),
    Column('jingluo_id', Integer, ForeignKey('jingluo.id'))
)
 

###处方
        