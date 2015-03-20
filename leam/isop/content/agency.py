"""Definition of the Agency content type
"""

from zope.interface import implements
from Products.CMFCore.utils import getToolByName

from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

# -*- Message Factory Imported Here -*-
from leam.isop import isopMessageFactory as _

from leam.isop.interfaces import IAgency
from leam.isop.config import PROJECTNAME
from leam.isop import logger

AgencySchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.BooleanField(
        'autotag',
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u"Auto Tag"),
            description=_(u"Should the title of this agency be used as a tag?"),
            visible={'view':'hidden', 'edit':'visible'},
        ),
        default=_(u"True"),
    ),

    atapi.StringField(
        'website',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Web Site"),
            description=_(u"The main web site for the Agency."),
        ),
        required=True,
        validators=('isURL'),
    ),

    atapi.ImageField(
        'logo',
        storage=atapi.AnnotationStorage(),
        sizes = {'large' : (768, 769),
                 'preview' : (400, 400),
                 'mini' : (200, 200),
                 'thumb' : (128, 128),
                 'tile' : (64, 64),
                 'icon' : (32, 32),
                 'listing' : (16, 16),
                },

        widget=atapi.ImageWidget(
            label=_(u"Logo"),
            description=_(u"Image to be used as the agency's logo."),
        ),
        validators=('isNonEmptyFile'),
    ),

    atapi.TextField(
        'overview',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Agency Information"),
            description=_(u"A brief overview of the agency."),
            rows = 10,
        ),
    ),

    atapi.TextField(
        'address',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Address"),
            description=_(u"Address and contact information."),
            rows = 6,
        ),
    ),

    atapi.StringField(
        'phone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Phone"),
            description=_(u"Primary phone number"),
        ),
        validators=('isUSPhoneNumber'),
    ),

    atapi.ReferenceField(
        'coverage',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Default Area"),
            description=_(u"GIS layer (used as the default for plan boundaries)."),
        ),
        relationship='agency_coverage',
        allowed_types=('SimMap',), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

AgencySchema['title'].storage = atapi.AnnotationStorage()
AgencySchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(AgencySchema, moveDiscussion=False)


class Agency(base.ATCTContent):
    """A planning agency"""
    implements(IAgency)

    meta_type = "Agency"
    schema = AgencySchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    autotag = atapi.ATFieldProperty('autotag')
    website = atapi.ATFieldProperty('website')
    logo = atapi.ATFieldProperty('logo')
    address = atapi.ATFieldProperty('address')
    phone = atapi.ATFieldProperty('phone')
    overview = atapi.ATFieldProperty('overview')
    coverage = atapi.ATReferenceFieldProperty('coverage')

    def getPlans(self):
        """returns a dictionary of Plan object associated the the agency"""
        #import pdb; pdb.set_trace()
        # might be able to back reference to avoid Subject search
        #myplans = self.getBRefs()
        d = {}
        plans = self.portal_catalog(portal_type='Plan', Subject=self.title)
        for brain in plans:
            obj = brain.getObject()
            d.setdefault(obj.getPlantype()[0], []).append(obj)
        return d

    def logo_or_title(self):
        """returns the logo (or title) as a link"""
        #import pdb; pdb.set_trace()
        if self.logo:
            return '<a href="%s"><img src="%s"/></a>' % (self.absolute_url(), self.logo.absolute_url())
        else:
            return '<a href="%s">%s</a>' % (self.absolute_url(), self.title)


atapi.registerType(Agency, PROJECTNAME)
