from geojson import Point, Feature, FeatureCollection

from plone import api
from Products.Five import BrowserView

from leam.isop import MessageFactory as _

from leam.isop.agency import IAgency
from leam.isop.plan import IPlan, plan_types
from leam.simmap.interfaces import ISimMap


# View class
class AgencyMapView(BrowserView):
    """ plan view class """

    def plans(self):
        """ return all plans in the agency """

        results = api.content.find(context=self.context, object_provides=IPlan)
        return [p.getObject() for p in results]


class AgencyLocations(BrowserView):
    """ a dynamically created geojson file based on agency locations """

    def agencies(self):
        results = api.content.find(context=self.context, 
                object_provides=IAgency)
        return [p.getObject() for p in results]

