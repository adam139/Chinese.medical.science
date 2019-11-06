#-*- coding: UTF-8 -*-

import sqlalchemy.schema
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import mysql
from sqlalchemy import Column, String, Integer, Date, Table
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from zope import schema
from zope.interface import Interface,implements

from Chinese.medical.science import ORMBase as Base
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
    wei = Column(String(8))    

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
    xing = Column(String((8)))    

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
    mingcheng = Column(String(14))    

    def __init__(self, mingcheng):
        self.mingcheng = mingcheng

       
 ###药和经络关联表
Yao_JingLuo_Asso = Table(
    'yao_jingluo', Base.metadata,
    Column('yao_id', Integer, ForeignKey('yao.id')),
    Column('jingluo_id', Integer, ForeignKey('jingluo.id'))
)


###药
class IYao(Interface):
    """中药:
    人参、白术、甘草
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    yaowei_id = schema.Int(
            title=_(u"foreagn key link to wei"),
        ) 
    yaoxing_id = schema.Int(
            title=_(u"foreagn key link to yao xing"),
        )       
    mingcheng = schema.TextLine(
            title=_(u"ming cheng"),
        )
    zhuzhi = schema.TextLine(
            title=_(u"zhu zhi"),
        )
    yaowei = schema.Object(
            title=_(u"gui jing"),
            schema=IJingLuo,
        )
    yaoxing = schema.Object(
            title=_(u"gui jing"),
            schema=IJingLuo,
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
    mingcheng = Column(String(4))
    zhuzhi = Column(String(64))
    guijing = relationship("YaoWei", backref="yaoes")
    guijing = relationship("YaoXing", backref="yaoes")
    guijing = relationship("JingLuo", secondary=Yao_JingLuo_Asso)    

    def __init__(self, mingcheng,zhuzhi):
        self.mingcheng = mingcheng
        self.zhuzhi = zhuzhi

 
###处方
class IChuFang(Interface):
    """中药:
    人参、白术、甘草
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    yisheng_id = schema.Int(
            title=_(u"foreagn key link to wei"),
        ) 
    mingcheng = schema.TextLine(
            title=_(u"ming cheng"),
        )
    yizhu = schema.TextLine(
            title=_(u"zhu zhi"),
        )
    jiliang = schema.Int(
            title=_(u"ji liang"),
        )    
        
        
class ChuFang(Base):
    
    implements(IChuFang)    
    __tablename__ = 'chufang'

    id = Column(Integer, primary_key=True)
    yao_id = Column(Integer, ForeignKey('yao.id'))
    mingcheng = Column(String(24))
    jiliang = Column(Integer)
    yizhu = Column(String(64))
    
    # association proxy of "user_keywords" collection
    # to "keyword" attribute
    yaoes = association_proxy('yao_chufang', 'yao')    
   
    def __init__(self, mingcheng,zhuzhi):
        self.mingcheng = mingcheng
        self.zhuzhi = zhuzhi
        

 ###药和处方关联表
class Yao_ChuFang_Asso(Base):
    __tablename__ = 'yao_chufang'
    
    yao_id = Column(Integer, ForeignKey('yao.id'), primary_key=True)
    chufang_id = Column(Integer, ForeignKey('chufang.id'), primary_key=True)
    yaoliang = Column(Integer)
    paozhi = Column(String(64))
     
    # bidirectional attribute/collection of "chufang"/"yao_chufang"
    chufang = relationship(ChuFang,
                backref=backref("yao_chufang",
                                cascade="all, delete-orphan")
            )

    # reference to the "Yao" object
    yao = relationship("Yao")

    def __init__(self, yao=None, chufang=None, yaoliang=None, paozhi=None):
        self.yao = yao
        self.chufang = chufang
        self.yaoliang = yaoliang
        self.paozhi = paozhi



               