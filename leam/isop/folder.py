from geojson import dumps, Point, Feature, FeatureCollection

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
        #import pdb; pdb.set_trace()

        results = api.content.find(context=self.context, object_provides=IPlan)
        return [{'title': p.Title(),
                 'url': p.getURL(),
                 'agency': p.getObject().getParentNode().Title(),
                 'plantype': p.getObject().plantype,
                } for p in results]


class AgencyLocations(BrowserView):
    """ a dynamically created geojson file based on agency locations """

    def agencies(self):
        results = api.content.find(context=self.context, 
                object_provides=IAgency)
        return [p.getObject() for p in results]


    def __call__(self):
        features = []
        for i, obj in enumerate(self.agencies()):
            pt = Point((obj.longitude, obj.latitude))
            props = dict(name=obj.title, url=obj.absolute_url(),
                    plans=obj.plan_count(), maps=obj.map_count())
            features.append(Feature(id=i, geometry=pt, properties=props))

        self.request.response.setHeader('Content-Type', 'application/json')
        if features:
            return dumps(FeatureCollection(features))
        else:
            return dumps({})
