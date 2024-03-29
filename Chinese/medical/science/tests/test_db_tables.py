#-*- coding: UTF-8 -*-
import datetime
import unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from Chinese.medical.science.testing import INTEGRATION_TESTING
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

from Chinese.medical.science.interfaces import IDbapi
from zope.component import queryUtility
from Chinese.medical.science import  Session
from Chinese.medical.science import  engine
from Chinese.medical.science import ORMBase as Base
from Chinese.medical.science.orm import Yao_JingLuo_Asso, Yao_ChuFang_Asso

class TestDatabase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def drop_tables(self,tbls=None):
        """drop all db tables
        """

        if tbls == None:
            tbls = ['Yao','YaoWei','YaoXing','JingLuo','Yao_JingLuo_Asso']
        for tb in tbls:
            import_str = "from %(p)s import %(t)s as tablecls" % dict(p='Chinese.medical.science.orm',t=tb) 
            exec import_str
            tablecls.__table__.drop(engine)
                                

    def create_tables(self,tbls=None):
        """create all db tables
        """

        for tb in tbls:
            import_str = "from %(p)s import %(t)s as tablecls" % dict(p='Chinese.medical.science.orm',t=tb) 
            exec import_str
#             tablecls.__table__.create(engine)
        Base.metadata.create_all(engine)

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        tbls = ['YaoWei','YaoXing','JingLuo','Yao_JingLuo_Asso','Yao']
#         tbls = ['Yao','YaoWei','YaoXing']
        self.create_tables(tbls)

    def test_yaowei(self):
        
        from Chinese.medical.science.orm import YaoWei
        yaowei = YaoWei("酸")
        Session.add(yaowei)
        Session.commit()
        suan = Session.query(YaoWei).filter(YaoWei.wei=="酸").all()
        self.assertEqual(len(suan),1)
        for xing in suan:
            Session.delete(xing)            
        Session.commit()
        suan = Session.query(YaoWei).all()        
        self.assertEqual(bool(suan),False)
        
    def test_yaoxing(self):
        
        from Chinese.medical.science.orm import YaoXing
        yaoxing = YaoXing("寒")
        Session.add(yaoxing)
        Session.commit()
        suan = Session.query(YaoXing).filter(YaoXing.xing=="寒").all()
        self.assertEqual(len(suan),1)              
        
        suan = Session.query(YaoXing).all()
        for xing in suan:
            Session.delete(xing)            
        Session.commit()
        suan = Session.query(YaoXing).all()
        self.assertEqual(bool(suan),False)
 
    def test_jingluo(self):
        
        from Chinese.medical.science.orm import JingLuo
        item = JingLuo("足少阳胆经")
        Session.add(item)
        Session.commit()
        items = Session.query(JingLuo).filter(JingLuo.mingcheng=="足少阳胆经").all()
        self.assertEqual(len(items),1)             
        for m in items:
            Session.delete(m)            
        Session.commit()
        items = Session.query(JingLuo).all()
        self.assertEqual(bool(items),False)               

    def test_yaoes(self):
        
        from Chinese.medical.science.orm import Yao,YaoXing,YaoWei,JingLuo
        items = Session.query(Yao).all()
        items.extend(Session.query(YaoXing).all())
        items.extend(Session.query(YaoWei).all())
        items.extend(Session.query(JingLuo).all())
        for m in items:
            Session.delete(m)            
        Session.commit()        
        yaowei = YaoWei("酸")
        yaoxing = YaoXing("寒")
        jingluo = JingLuo("足厥阴肝经")
        yao = Yao("白芍")        
        yao.yaowei = yaowei
        yao.yaoxing = yaoxing
        yao.guijing = [jingluo]
        Session.add(yao)
        Session.add(yaowei)
        Session.add(yaoxing)
        Session.add(jingluo)                                     
        Session.commit()
        items = Session.query(Yao.mingcheng,YaoWei.wei).filter(YaoWei.wei=="酸").all()
        self.assertEqual(len(items),1)             

        items = Session.query(JingLuo).all()

        
        

    def test_dbapi_yaowei(self):
# oracle env setting        
#         import os
#         os.environ['NLS_LANG'] = '.AL32UTF8'            
#         self.create_tables(tbls=['Fashej'])
#         self.drop_tables(tbls=['Fashej'])
#         import pdb
#         pdb.set_trace()
        
# ('333333002','发射机01','asd2w23sds212211111','m',2.4,0,2.8,10,0,2.8,20,1.1,'AM-V',2,1,' 常用发射机1')
        values = dict(sbdm="333333003",sbmc=u"发射机02",pcdm="asd2w23sds212211111",location=u"m",
                      freq=2.4,pd_upper=0,pd_lower=2.8,num=10,
                      freq_upper=0,freq_lower=2.8,bw=20,base_power=1.1,
                      tzlx="AM-V",bzf=2,mid_freq=1,comment1=u"常用发射机1")        
        dbapi = queryUtility(IDbapi, name='fashej')
        dbapi.add(values)
        nums = dbapi.query({'start':0,'size':1,'SearchableText':'','sort_order':'reverse'})
        id = nums[0].id        
        rt = dbapi.getByCode(id)
        self.assertTrue(nums is not None)
        self.assertEqual(len(nums),1)
#         rt = dbapi.DeleteByCode(id)
        self.assertTrue(rt)

