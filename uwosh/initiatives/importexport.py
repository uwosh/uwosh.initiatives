
def import_all(context):
    if not context.readDataFile('uwosh.initiatives.txt'):
        return
    
    site = context.getSite()
    
    if 'initiatives' not in site.objectIds():
        site.invokeFactory(type_name="Folder", id="initiatives")
        site['initiatives'].setTitle('Initiatives')
        site.portal_workflow.doActionFor(site['initiatives'], 'publish')