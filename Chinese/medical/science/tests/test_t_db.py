#-*- coding: UTF-8 -*-
import datetime
import unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from emc.kb.testing import INTEGRATION_TESTING
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func

class TestEmc_test(unittest.TestCase):
    """docstring for TestEmc_test."""

    layer = INTEGRATION_TESTING

    def test_t_db_mapping_danwei(self):
        from emc.kb.mapping_t_db import Danwei
        from emc.kb.mapping_t_db import T_ry
        from emc.kb import t_session as Session

        orig = Session.query(func.count(Danwei.danweiId)).scalar()
        ry_orig = Session.query(func.count(T_ry.t_ryId)).scalar()
        dw = Danwei()
        dw.danweimc = u"单位名称1"
        dw.danweidz = u"单位地址1"
        dw.danweilxfs = u"单位电话:85414302"
        dw.users = [T_ry(t_ryname = u"李四"),]
        Session.add(dw)        
        nums = Session.query(func.count(Danwei.danweiId)).scalar()
        ry_nums = Session.query(func.count(T_ry.t_ryId)).scalar()
        self.assertTrue(orig == nums-1)
        self.assertTrue(ry_nums == ry_orig + 1)
        import pdb
        pdb.set_trace()
        Session.rollback()
        nums = Session.query(func.count(Danwei.danweiId)).scalar()
        self.assertTrue(orig == nums)
        print dw.danweimc
        print nums

    def test_t_db_mapping_t_ry(self):
        from emc.kb.mapping_t_db import T_ry
        from emc.kb.mapping_t_db import Danwei
        from emc.kb import t_session as Session

        import pdb
        pdb.set_trace()

        t_ry = T_ry()
        dw = Danwei()

        flag = Session.query(func.count(dw.danweiId)).scalar()
        t_ry.t_ryname = u"张三"
        t_ry.t_rygender = u"男"
        t_ry.t_ryage = u"22"
        t_ry.t_rydegree = u"硕士"
        t_ry.t_rytitle = u"研究员"
        t_ry.t_rynumber = u"123x456abc"
        t_ry.danwei = Danwei(danweimc=u"人员单位1")
        Session.add(t_ry)
        Session.commit()
        nums = Session.query(func.count(dw.danweiId)).scalar()
#         print flag
#         print nums

        import pdb
        pdb.set_trace()
#       a = t_ry(t_ryname = u"张三",t_rygender = u"男",t_ryage = u"22",t_rydegree = u"硕士",t_rytitle = u"研究员",t_rynumber = u"123x456abc")
        # Session.add(t_ry)
        # nums = Session.query(func.count(t_ry.t_ryId)).scalar()


    def test_t_db_danwei_locator(self):
        from emc.kb.mapping_t_db import Danwei
        from emc.kb.interfaces import IDanweiLocator
        from zope.component import getUtility
        from emc.kb import t_session as Session

        locator = getUtility(IDanweiLocator)
        danweimc = u"单位名称1"
        danweidz = u"单位地址1"
        danweilxfs = u"单位电话:85414302"

        danwei = locator.getByCode(danweimc)
        import pdb
        pdb.set_trace()
        if danwei == None:
            locator.add(danweimc)
