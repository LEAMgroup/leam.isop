from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from leam.isop import isopMessageFactory as _


class IPlanView(Interface):
    """
    PlanView view interface
    """

    def agency_summary():
        """ returns a summary of the plan's agency """


class PlanView(BrowserView):
    """
    PlanView browser view
    """
    implements(IPlanView)

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
        """ returns a list of maps associated with the plan """
        refs = self.context.getBRefs()
        return [r for r in refs if r.Type() == "SimMap"]

    def agency_summary(self):
        """
        returns a summary of the agency.
        """
        agency = self.context.getAgency()

        rep = '<a href="{href}">'
        if agency.getLogo():
            rep += '<img src="{logo}" title="{title}" alt="{title}" /></a>'
        else:
            rep += '{title}</a>'

        rep += '<h3 class="field-label">Web Site</h3><p>{website}</p>'
        rep += '<h3 class="field-label">Address</h3><p>{address}</p>'
        rep += '<h3 class="field-label">Phone</h3><p>{phone}</p>'
        return rep.format(
                href = agency.absolute_url(),
                title = agency.Title(),
                logo = agency.absolute_url()+'/logo_mini',
                website = agency.getWebsite(),
                address = agency.getAddress(),
                phone = agency.getPhone(),
                )

