from os.path import splitext
import json

from z3c.form import group, field
from zope import schema
from zope.interface import implements
from zope.interface import invariant, Invalid
from zope.security import checkPermission
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Acquisition import aq_inner

from plone import api
from plone.dexterity.content import Container

from plone.app.textfield import RichText, RichTextValue
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

import plone.namedfile.file
from plone.supermodel import model
from Products.Five import BrowserView
from plone.dexterity.browser.view import DefaultView

from leam.isop import MessageFactory as _

from leam.isop.plan import IPlan
from leam.isop.plan import plan_types as _plan_types
from leam.simmap.interfaces import ISimMap

# Interface class; used to define content-type schema.

class IAgency(model.Schema, IImageScaleTraversable):
    """
    Planning Agency
    """
    overview = RichText(
            title = _(u'Agency Information'),
            description = _(u'A brief overview of the agency.'),
            required = False,
            )

    address = schema.TextLine(
            title = _(u'Address'),
            )
    city = schema.TextLine(
            title = _(u'City'),
            )
    state = schema.TextLine(
            title = _(u'State'),
            )
    zipcode = schema.TextLine(
            title = _(u'Zipcode'),
            )
    location = schema.TextLine(
            title = _(u'Location'),
            description = _(u'provided in lat, long format'),
            required = False,
            )
    phone = schema.TextLine(
            title = _(u'Phone'),
            required = False,
            )
    email = schema.ASCIILine(
            title = _(u'Email'),
            required = False,
            )
    website = schema.URI(
            title = _(u'Web Site'),
            required = False,
            )
    logo = NamedBlobImage(
            title = _(u'Logo'),
            required = False,
            )
    boundary = NamedBlobFile(
            title = _(u'Agency Boundary Map'),
            description = _('only supports geojson files'),
            required = False,
            )

class Agency(Container):

    @property
    def latitude(self):
        try:
            return float(self.location.split(',')[0].strip())
        except AttributeError, IndexError:
            return 0.0

    @property
    def longitude(self):
        try:
            return float(self.location.split(',')[1].strip())
        except AttributeError, IndexError:
            return 0.0

    @property
    def templates(self):
        """return the GIS templates folder"""
        templates = api.content.find(id='gistemplates')
        if len(templates): 
            return aq_inner(templates[0].getObject())
        else:
            return None

    def plan_count(self):
        """ return the number of primary plans in the agency """

        results = api.content.find(context=self, object_provides=IPlan)
        ptypes = set([p.getObject().plantype for p in results])
        try:
            ptypes.remove('Other')
        except KeyError:
            pass

        return len(ptypes)

    def map_count(self):
        """ return the number of maps in the agency """

        results = api.content.find(context=self, object_provides=ISimMap)
        return len(results)


class addPlan(BrowserView):
    """ addPlan view is intended as an ajax call based on a file upload form
        created by dropzone.js. Rending this view directly quietly redirects
        to agency view.
    """

    def __call__(self):

        context = aq_inner(self.context)

        title = self.request.form['plan-title']
        plantype = self.request.form['plan-type']

        obj = api.content.create(
                container=context,
                type='leam.isop.plan', 
                title=title,
                safe_id = True,
                )

        obj.plantype = plantype

        obj.synopsis = RichTextValue(
                raw=u'<a href="%s">Click to edit Plan '
                    'data and add a plan synopsis.</a>' % 
                    (obj.absolute_url()+'/edit'),
                mimeType='text/html',
                outputMimeType='text/html')

        obj.document = plone.namedfile.file.NamedBlobFile(
                filename=self.request.form['file'].filename.decode('utf-8'))
        obj.document._blob.consumeFile(self.request.form['file'].name)

        api.content.transition(obj=obj, transition='submit')

        return self.request.response.redirect(context.absolute_url())


class addLayer(BrowserView):

    def __call__(self):

        context = aq_inner(self.context)

        title = self.request.form['layer-title']
        gistype = self.request.form['layer-type']
        filename = self.request.form['file'].filename

        simmap = api.content.create(
                container=context,
                type='SimMap', 
                title=title,
                safe_id = True,
                )

        with open(self.request.form['file'].name) as f:
            simmap.setSimImage(f.read(), filename=filename)

        mapfile = context.templates[gistype].getMapFile()
        simmap.setMapFile(mapfile, filename=mapfile.filename)

        api.content.transition(obj=simmap, transition='submit')

        return self.request.response.redirect(context.absolute_url())


# default view class
class AgencyView(DefaultView):
    """ agency view class """

    def summary(self):
        """ currently unused method """
        plans = api.content.find(context=self.context, object_provides=IPlan)
        if plans:
            return plans[0].getObject().unrestrictedTraverse(
                    '@@summary').render()
        else:
            return ''

    def canManage(self):
            return checkPermission('cmf.AddPortalContent', self.context)

    def plans(self):
        """ return all plans in the agency """
        results = api.content.find(context=self.context, 
                object_provides=IPlan)
        return [p.getObject() for p in results]

    def maps(self):
        """ return all maps in the agency """
        results =  api.content.find(context=self.context, 
                object_provides=ISimMap)
        return [m.getObject() for m in results]

    def plan_types(self):
        return [{'value': term.value, 'token':term.token, 'title':term.title}
                for term in _plan_types]

    def layer_types(self):
        """ return list of SimMaps from the template folder """

        # TODO: the page template should probably use getPath instead 
        # of getId. With getId the assumption is that the id is from 
        # the one and only templates folder.
        results = api.content.find(
                context=self.context.templates, 
                object_provides=ISimMap
                )

        return [{'id':m.getId(), 'path':m.getPath(), 'title':m.Title()} 
                for m in results ]


class AgencyStats(BrowserView):
    """ provide stats for each agency in JSON format """

    def plans(self, context):
        """ return count of plans """
        return len(api.content.find(context=context, object_provides=IPlan))

    def __call__(self):

        stats = []
        agencies = api.content.find(context=api.portal.get(),
                object_provides=IAgency)
        for a in agencies:
            stats.append(dict(
                    name = a.Title(),
                    url = a.getURL(),
                    plans = self.plans(context=a),
                    layers = len(api.content.find(context=a, 
                        object_provides=ISimMap)),
            ))

        self.request.response.setHeader('content-type', 'application/json')
        return json.dumps(stats)


def agencyCreated(context, event):
    """creation event"""
    import pdb; pdb.set_trace()

    group = api.group.get(groupname=context.getId())
    if not group:
        group = api.group.create(
                groupname=context.id,
                title=context.title,
                description="automatically generated group for agency",
                roles=['Reader'],
                )

    context.manage_setLocalRoles(group.getGroupName(), 
            ('Contributor', 'Editor'))
    context.reindexObjectSecurity()

