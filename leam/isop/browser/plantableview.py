from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from leam.isop import isopMessageFactory as _


class IPlanTableView(Interface):
    """
    PlanTable view interface
    """

    def test():
        """ test method"""


class PlanTableView(BrowserView):
    """
    PlanTable browser view
    """
    implements(IPlanTableView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def getplan(self, agency, plantype):
        return "<b>%s -- %s</b>" % (agency, plantype)

    def agencies(self):
        return self.portal_catalog(type='Agency')

    def plans(self, agency):
        return self.portal_catalog(type='Plan', Subject=agency)

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}
