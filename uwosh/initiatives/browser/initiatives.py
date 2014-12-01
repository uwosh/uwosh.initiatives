from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from AccessControl import getSecurityManager
from zope.component import getMultiAdapter
from zope.app.component.hooks import getSite

class InitiativesViewlet(ViewletBase):
    render = ViewPageTemplateFile('initiatives_viewlet.pt')
    
    def update(self):
        
        super(InitiativesViewlet, self).update()
        
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        
        site = getSite()
        props = getToolByName(self.context, 'portal_properties').uwosh_initiatives
        
        if props.getProperty('only_show_in_site_root', True):
            #must be site root
            self.should_display = context_state.is_portal_root()
        else:
            self.should_display = True
        
        if self.should_display:
            self.sitetitle = site.title
            catalog = getToolByName(self.context, 'portal_catalog')
            self.view_all_url = props.getProperty('view_all_url', None)
            
            if self.view_all_url is None and 'initiatives' in site.objectIds():
                self.view_all_url = site.absolute_url() + '/initiatives'
            
            self.initiatives = catalog(
                portal_type = 'Initiative', 
                review_state = 'published',
                sort_on = 'getObjPositionInParent',
                sort_order = 'ascending',
                getShowInitiative='True'
            )
            
            if len(self.initiatives) == 0:
                self.should_display = False

            catalog.refreshCatalog()
        
        
        
        
