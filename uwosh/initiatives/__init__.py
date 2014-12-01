from Products.Archetypes import atapi
from Products.CMFCore import utils as cmfutils
ADD_CONTENT_PERMISSION = "Add portal content"

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    import content

    content_types, constructors, ftis = atapi.process_types(atapi.listTypes('uwosh.initiatives'), 'uwosh.initiatives')

    cmfutils.ContentInit(
        'uwosh.initiatives Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis,
        ).initialize(context)

