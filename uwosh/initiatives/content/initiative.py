from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from uwosh.initiatives.config import *
from Products.ATContentTypes.content.newsitem import ATNewsItem, ATNewsItemSchema
from Products.ATContentTypes.content.link import ATLink, ATLinkSchema

copied_fields = {}
copied_fields['text'] = ATNewsItemSchema['text'].copy()
copied_fields['text'].widget.description = "A more detailed description of the initiative."
copied_fields['text'].widget.label = "Initiative Details"

copied_fields['description'] = ATNewsItemSchema['description'].copy()
copied_fields['description'].widget.description = "An overview of the initiative.  This is what will be shown in the set of initative links."
copied_fields['description'].widget.label = "Initiative Overview"

copied_fields['remoteUrl'] = ATLinkSchema['remoteUrl'].copy()
copied_fields['remoteUrl'].default = ''
copied_fields['remoteUrl'].primary = False
copied_fields['remoteUrl'].required = False
copied_fields['remoteUrl'].widget.description = "If not linking to an external site this field can be left blank"
copied_fields['remoteUrl'].widget.label = "URL"

schema = Schema((
    copied_fields['text'],
    copied_fields['description'],
    copied_fields['remoteUrl'],

BooleanField( 
        name='externalWindow', 
        default=1, 
        widget=BooleanWidget( 
            label="Open Link in a New Window?",  
        ), 
        searchable=0, 


),

BooleanField( 
        name='showInitiative', 
        default=1, 
        widget=BooleanWidget( 
            label="Show Initiative?",  
        ), 
        searchable=0, 


),

)
)


InitiativeSchema = ATNewsItemSchema.copy() + schema.copy()
#InitiativeSchema['remoteUrl'] = ATLinkSchema['remoteUrl'].copy()
#InitiativeSchema['remoteUrl'].default = ""
#InitiativeSchema['remoteUrl'].required = False
#InitiativeSchema.['remoteUrl'].widget.description = "If not linking to an external site this field can be left as is"
#InitiativeSchema.['remoteUrl'].widget.label = "URL"





class Initiative(ATNewsItem):
    """
    
    """
    
    assocMimetypes = ('application/*', 'audio/*', 'video/*', )
    assocFileExt   = ('mp3', 'flv', 'mov', 'swf')
    
    security = ClassSecurityInfo()

    implements(interfaces.IInitiative)
    
    archetype_name = 'Initiative'
    meta_type = 'Initiative'
    portal_type = "Initiative"
    _at_rename_after_creation = True

    schema = InitiativeSchema
    
    
registerType(Initiative, PRODUCT_NAME)
