"""Definition of the Plan content type
"""
import os
from zope.interface import implements
from Products.CMFCore.utils import getToolByName

from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from plone.app.blob.field import FileField, ImageField
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from Products.DataGridField import Column, FixedColumn

# -*- Message Factory Imported Here -*-
from leam.isop import isopMessageFactory as _

from leam.isop.interfaces import IPlan
from leam.isop.config import PROJECTNAME
from leam.isop import logger

PlanSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    FileField(
        'document',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"Document"),
            description=_(u"A full version of the plan in PDF format."),
        ),
        required=True,
        validators=('isNonEmptyFile'),
    ),

    atapi.BooleanField(
        'downloadable',
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u"Allow Download"),
            description=_(u"Allow users to download directly from this site."),
        ),
        default=True,
    ),

    atapi.StringField(
        'homeurl',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Home URL"),
            description=_(u"The URL of the plan document on its home website."
                "  If the document is not downloadable directly from the Plan"
                " library then the Home URL is required."
                ),
            size=60,
        ),
    ),

    atapi.StringField(
        'contact',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
             label=_(u"Primary Contact"),
        ),
    ),

    atapi.StringField(
        'email',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
             label=_(u"Contact's Email"),
        ),
        validators=('isEmail'),
    ),

    atapi.TextField(
        'address',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Address"),
            rows = 6,
        ),
    ),

    atapi.StringField(
        'phone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
             label=_(u"Phone"),
        ),
        validators=('isUSPhoneNumber'),
    ),

    atapi.TextField(
        'synopsis',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Synopsis"),
            description=_(u"A brief synopsis of the plan including purpose and key goals."),
            rows=20,
        ),
    ),

    atapi.ReferenceField(
        'agency',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Agency"),
            description=_(u"Select the primary agency"),
        ),
        required=True,
        relationship='plan_agencies',
        allowed_types=('Agency',), 
        multiValued=False,
    ),

    atapi.StringField(
        'partners',
        storage=atapi.AnnotationStorage(),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Partners"),
            description=_(u"Select any partner agencies."),
        ),
        required=False,
        vocabulary="get_agencies",
     ),

    atapi.LinesField(
        'plantype',
        storage=atapi.AnnotationStorage(),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Plan Type"),
            description=_(u"One or more plan types that are appropriate for the plan."),
        ),
        vocabulary=["Comprehensive Plan", "Zoning Regulations", 
                    "Transportation Plan", "Capital Improvement Plan",
                    "Economic Development Plan", "Subdivision Regulations",
                    "Land Use Plan", "Other",
                   ],
        required=True,
    ),

    DataGridField(
            'issues',
            searchable = False,
            columns = ('issue', 'pages'),
            default = [
                { 'issue': 'Mobility', 'pages': '' },
                { 'issue': 'Economic Opportunity', 'pages': '' },
                { 'issue': 'Built Environment', 'pages': '' },
                { 'issue': 'Cultural Systems', 'pages': '' },
                { 'issue': 'Social Systems', 'pages': '' },
                { 'issue': 'Natural  Systems', 'pages': '' },
                { 'issue': 'Farm & Ranch', 'pages': '' },
                ],
            allow_insert = False,
            allow_delete = False,
            allow_reorder = False,
            widget = DataGridWidget(
                label=_(u"Issue Area References"),
                description=_(u"If possible provide the sections or page"
                    " numbers associated with each issue area.  This"
                    " information will be used to help locate relevant plans"
                    " from the Issue Areas section."
                    ),
                columns = {
                    'issue' : FixedColumn("Issue Area"),
                    'pages' : Column("Relevant Pages"),
                    },
                ),
            ),

    ImageField(
        'cover',
        required = False,
        allowable_content_types = ('image/png', 'image/jpeg'),
        sizes = {'large' : (768, 769),
                 'preview' : (400, 400),
                 'mini' : (200, 200),
                 'thumb' : (128, 128),
                 'tile' : (64, 64),
                 'icon' : (32, 32),
                 'listing' : (16, 16),
                 },
        storage=atapi.AnnotationStorage(),
        widget=atapi.ImageWidget(
            label=_(u"Cover Page"),
            description=_(u"An image used as the plan's cover page."),
            visible={'view':'hidden', 'edit':'visible'},
        ),
        #validators=('isNonEmptyFile'),
    ),

    atapi.ReferenceField(
        'layer',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"GIS Layer"),
            description=_(u"A GIS layer providing the spatial extent of the plan."),
            visible={'view':'hidden', 'edit':'visible'},
        ),
        relationship='plan_layer',
        allowed_types=('SimMap',),
        multiValued=False,
    ),

    atapi.StringField(
        'layertype',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"GIS Layer Type"),
            description=_(u"Used internally to determine the type of information provided by the GIS layer."),
            visible={'view':'hidden', 'edit':'hidden'},
        ),
        vocabulary=["boundary", "representation", "impact"],
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

PlanSchema['title'].storage = atapi.AnnotationStorage()
PlanSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema( PlanSchema, moveDiscussion=False)


class Plan(base.ATCTContent):
    """A plan"""
    implements(IPlan)

    meta_type = "Plan"
    schema = PlanSchema
    #security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    synopsis = atapi.ATFieldProperty('synopsis')
    homeurl = atapi.ATFieldProperty('homeurl')
    document = atapi.ATFieldProperty('document')
    downloadable = atapi.ATFieldProperty('downloadable')
    contact = atapi.ATFieldProperty('contact')
    email = atapi.ATFieldProperty('email')
    address = atapi.ATFieldProperty('address')
    phone = atapi.ATFieldProperty('phone')
    cover = atapi.ATFieldProperty('cover')
    plantype = atapi.ATFieldProperty('plantype')
    agency = atapi.ATReferenceFieldProperty('agency')
    partners = atapi.ATFieldProperty('partners')
    #agency = atapi.ATFieldProperty('agency')
    #partners = atapi.ATReferenceFieldProperty('partners')
    layer = atapi.ATReferenceFieldProperty('layer')
    layertype = atapi.ATFieldProperty('layertype')

    def get_agencies(self):
        """returns a list of agency titles"""
        catalog = getToolByName(self, 'portal_catalog')
        return [x.Title for x in catalog(portal_type='Agency')]
    

def planModified(context, event):
    """ turns the first page of the plan into a cover image """
    #import pdb; pdb.set_trace()

    # set the tag based on the primary agency 
    context.setSubject(context.getAgency().Title())
    context.reindexObject(idxs=['Subject',])

    # create the cover page
    f = context.getDocument().getBlob().open()
    os.system('pdftocairo -jpeg -singlefile %s /tmp/cover' % f.name)
    context.getCover().getBlob().consumeFile('/tmp/cover.jpg')
    f.close()

    # if a plan's map layer isn't given use the agency's default map
    if not context.layer:
        context.setLayer(context.getAgency().getCoverage())
        context.setLayertype('boundary')


atapi.registerType(Plan, PROJECTNAME)
