from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from leam.isop import isopMessageFactory as _


class IAgencyView(Interface):
    """
    Agent view interface
    """

    def map():
        """ get the referenced simmap widget """

    def plans():
        """ get the referenced simmap widget """


class AgencyView(BrowserView):
    """
    Agent browser view
    """
    implements(IAgencyView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def maps(self):
        """ returns a list of plan maps associated with the agency """
        refs = []
        for r in self.context.getBRefs():
            # get all the maps referencing the agency
            if r.Type() == "SimMap":
                refs.append(r)

            # get all the maps referencing a plan that references the agency
            # Note: perhaps only get the first map reference?
            elif r.Type() == "Plan":
                refs.extend([p for p in r.getBRefs() if p.Type() == 'SimMap'])
        return refs


    def plans(self):
        """
        return a table of plans.
        """
        title = self.context.Title()
        return  self.portal_catalog(portal_type='Plan', Subject=title) 

