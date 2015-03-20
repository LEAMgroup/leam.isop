from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from leam.isop import isopMessageFactory as _

__table__ = """
    <table id="agency-table">
        <thead>
            <tr>{headers}</tr>
        </thead>
        <tbody>
            {agencies}
        </tbody>
    </table>
"""

__plantypes__ = [
        "Comprehensive Plan", 
        "Zoning Regulations",
        "Land Use Plan",
        "Transportation Plan",
        "Economic Development Plan",
        ]

class IagencytableView(Interface):
    """
    agencytable view interface
    """

    def test():
        """ test method"""

class agencytableView(BrowserView):
    """
    agencytable browser view
    """
    implements(IagencytableView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def getPlanRep(self, brain):
        """give the brain of plan create a representation appropriate 
        for table listing."""
        if not brain:
            return "Not Found"

        # we may have more than one plan of the same type
        plan = brain[0].getObject()

        rep = '<a href="{homeurl}"> <img src="{cover}" alt="{title}"' + \
                'title="{title}" class="planrep" /></a>'
        if plan.downloadable:
            rep += '<a href="{download}" class="discreet" download </a>'

        return rep.format(
                title=plan.Title(),
                cover=plan.absolute_url()+"/cover_thumb",
                homeurl=plan.getHomeurl(),
                download=plan.absolute_url()+"/at_download/document",
                )

    def _agency_cell(self, agency):
        """formats the agency logo cell"""

        if agency.logo:
            rep = '<th><a href="{href}"><img src="{logo}" title="{title}"' + \
                  ' alt="{title}" class="agencyrep"/></a></th>'
            return rep.format(
                    title = agency.Title(),
                    href = agency.absolute_url(),
                    logo = agency.absolute_url() + '/logo_mini',
                    )

        else:
            rep = '<th><a href="{href}">{title}</a></th>'
            return rep.format(
                    href = agency.absolute_url(),
                    title = agency.Title(),
                    )

    def _plan_cell(self, plan):
        """formats the plan cell"""

        # ignore more than one plan for now
        plan = plan[0]

        rep = '<th><a href="{href}"><img src="{cover}" title="{title}"' + \
              ' alt="{title}" class="planrep" /></a></th>'
        return rep.format(
               href=plan.absolute_url(),
               title=plan.Title(),
               cover=plan.absolute_url() + '/cover_thumb',
               )


    def getAgencyTable(self):
        """return a table of all agencies and selected plans"""

        cols = ['<th>Agency</th>',]
        for ptype in __plantypes__:
            cols.append('<th>' + ptype + '</th>')
        headers = '\n'.join(cols)
        
        agency_rows = []
        for a in self.portal_catalog(portal_type="Agency"):
            agency = a.getObject()
            cols = [self._agency_cell(agency),]
            plans = agency.getPlans()
            for ptype in __plantypes__:
                if ptype in plans.keys():
                    cols.append(self._plan_cell(plans[ptype]))
                else:
                    cols.append('<th class="no-plan">NONE</th>')
            agency_rows.append('<tr>\n' + '\n'.join(cols) + '\n</tr>')

        return __table__.format(
                headers = headers,
                agencies = '\n'.join(agency_rows),
                )

    def getPlan(self, agency, plantype):
        """locate an agency's plan by plan type"""
        import pdb; pdb.set_trace()
        print "finding plan"


    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}
