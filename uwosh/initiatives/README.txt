Introduction
============

uwosh.initiatves provides an additional content type, Initiative, a viewlet
that will the most recent initiatives on the site on the main page.
    
Let's set up the test browser::
    
    >>> browser = self.browser

	>>> portal_url = self.portal_url
    >>> self.portal.error_log._ignored_exceptions = ()
    
We need to log in as a manager, because you need permission to create a content type:
	>>> from Products.PloneTestCase.setup import portal_owner, default_password

	>>> browser.open(portal_url + '/login_form?came_from=' + portal_url)
	>>> browser.getControl(name='__ac_name').value = portal_owner
	>>> browser.getControl(name='__ac_password').value = default_password
	>>> browser.getControl(name='submit').click()
	>>> browser.open(portal_url)

First off, let's navigate to the initiatives folder

	>>> browser.getLink('Initiatives').click()
	
There shouldn't be any initiatives in the folder since we haven't added
any Initiatives yet.

	>>> "There are currently no items in this folder" in browser.contents
	True
	
Also, the initiatives viewlet shouldn't be showing if there are no
initiatives

	>>> browser.open(portal_url)
	>>> "Plone site Initiatives" not in browser.contents
	True
	
Let's create an Initiatives now
	
	>>> browser.open(portal_url + "/createObject?type_name=Initiative")
	>>> browser.getControl(name='title').value = "Lower prices for all students!"
	>>> browser.getControl(name='description').value = "UW Oshkosh is looking to lower prices for all their students."
	>>> browser.getControl('Save').click()
	>>> initiative_url = browser.url
	
Check that it got moved to the initiatives folder

	>>> browser.open(portal_url + "/initiatives")
	>>> "Lower prices for all students!" in browser.contents
	True
	
The Initiative still won't show up on the home page because it isn't 
published.  Let's check to make sure.

	>>> browser.open(portal_url)
	>>> "UW Oshkosh is looking to lower prices for all their students." in browser.contents
	False
	
Let's publish the Initiative now.

	>>> browser.getLink("Contents").click()
	>>> browser.getLink("Initiatives").click()
	>>> browser.getLink("Lower prices for all students!").click()
	
	>>> "private" in browser.contents
	True
	
	>>> browser.open(browser.url + "/content_status_modify?workflow_action=publish")
	>>> "published" in browser.contents
	True
	
Now we should see it on the home page
	
	>>> browser.open(portal_url)
	>>> "Plone site Initiatives" in browser.contents
	True
	
	>>> "UW Oshkosh is looking to lower prices for all their students." in browser.contents
	True
	
Make sure the link is right

	>>> browser.getLink("UW Oshkosh is looking to lower prices for all their students.").click()
	>>> browser.url == initiative_url
	True
	
Now Let's change some settings.  The settings are located in
portal_properties.

	>>> browser.open(portal_url + "/manage")
	>>> browser.getLink("portal_properties").click()
	>>> browser.getLink("uwosh_initiatives (uwosh.initiatives properties)").click()
	>>> browser.getControl(name="number_of_initiatives_to_show:int").value = 4
	>>> browser.getControl(name="only_show_in_site_root:boolean").checked = 'true'
	>>> browser.getControl(name="view_all_url:string").value = portal_url + "/initiatives"
	>>> browser.getControl("Save Changes").click()
	
Now the 4 most recent initiatives will be listed, the viewlet will show on all pages, 
and it will now show the link to view all of the iniatives

Let's add a bunch more Initiatives

	>>> browser.open(portal_url + "/createObject?type_name=Initiative")
	>>> browser.getControl(name='title').value = "Second Initiative"
	>>> browser.getControl(name='description').value = "Overview of second Initiative."
	>>> browser.getControl('Save').click()
	>>> browser.open(browser.url + "/content_status_modify?workflow_action=publish")
	
	>>> browser.open(portal_url + "/createObject?type_name=Initiative")
	>>> browser.getControl(name='title').value = "Third Initiative"
	>>> browser.getControl(name='description').value = "Overview of third Initiative."
	>>> browser.getControl('Save').click()
	>>> browser.open(browser.url + "/content_status_modify?workflow_action=publish")
	
	>>> browser.open(portal_url + "/createObject?type_name=Initiative")
	>>> browser.getControl(name='title').value = "Fourth Initiative"
	>>> browser.getControl(name='description').value = "Overview of fourth Initiative"
	>>> browser.getControl('Save').click()
	>>> browser.open(browser.url + "/content_status_modify?workflow_action=publish")
	
	>>> browser.open(portal_url + "/createObject?type_name=Initiative")
	>>> browser.getControl(name='title').value = "Fifth Initiative"
	>>> browser.getControl(name='description').value = "Overview of fifth Initiative"
	>>> browser.getControl('Save').click()
	>>> browser.open(browser.url + "/content_status_modify?workflow_action=publish")
	
Let's make sure that all of these were added to the initiatives folder

	>>> browser.open(portal_url + "/initiatives")
	>>> "Second Initiative" in browser.contents
	True
	>>> "Third Initiative" in browser.contents
	True
	>>> "Fourth Initiative" in browser.contents
	True
	>>> "Fifth Initiative" in browser.contents
	True
	
Check to see if the four most recent initiatives are shown on the main page
	
	>>> browser.open(portal_url)
	
	>>> "Overview of second Initiative." in browser.contents
	True
	
	>>> "Overview of third Initiative." in browser.contents
	True
	
	>>> "Overview of fourth Initiative." in browser.contents
	True
	
	>>> "Overview of fifth Initiative." in browser.contents
	True
	
Also, make sure more link is there!
	>>> browser.getLink("more").click()
	>>> browser.url == portal_url + "/initiatives"
	True
