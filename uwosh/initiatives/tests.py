import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.Five.testbrowser import Browser

import uwosh.initiatives

ztc.installProduct("uwosh.initiatives")
ptc.setupPloneSite(products=('uwosh.initiatives',))

class Session(dict):
    def set(self, key, value):
        self[key] = value


class TestCase(ptc.PloneTestCase):
    
    def _setup(self):
        super(TestCase, self)._setup()
        self.setRoles(("Manager", "Member"))
        self.app.REQUEST['SESSION'] = Session()
        self.browser = Browser()
        self.app.acl_users.userFolderAddUser('root', 'secret', ['Manager'], [])
        self.browser.addHeader('Authorization', 'Basic root:secret')
        self.portal_url = 'http://nohost/plone'
        
    def afterSetUp(self):
        super(TestCase, self).afterSetUp()

    def setStatusCode(self, key, value):
        from ZPublisher import HTTPResponse
        HTTPResponse.status_codes[key.lower()] = value
    
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', uwosh.initiatives)
            fiveconfigure.debug_mode = False
            
        @classmethod
        def tearDown(cls):
            pass

def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='uwosh.initiatives',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='uwosh.initiatives.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='uwosh.initiatives',
        #    test_class=TestCase),

        ztc.ZopeDocFileSuite(
            'README.txt', package='uwosh.initiatives',
            test_class=TestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
