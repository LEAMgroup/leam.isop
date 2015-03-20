from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from leam.isop import isopMessageFactory as _
from leam.isop.interfaces import IAgency
from leam.simmap.interfaces import ISimMap


class IPlan(Interface):
    """A plan"""

    # -*- schema definition goes here -*-
    synopsis = schema.Text(
        title=_(u"Synopsis"),
        required=False,
        description=_(u"A brief synopsis of the plan including purpose and key goals."),
    )
#
    homeurl = schema.TextLine(
        title=_(u"Home URL"),
        required=False,
        description=_(u"The URL of the plan document on its home website."),
    )
#
    document = schema.Bytes(
        title=_(u"Document"),
        required=True,
        description=_(u"A full text version of the plan in either PDF or Word format."),
    )
#
    downloadable = schema.Bool(
        title=_(u"Downloadable"),
        required=False,
        description=_(u"Flag if the plan can be downloaded from the current site."),
    )
#
    cover = schema.Bytes(
        title=_(u"Cover Page"),
        required=False,
        description=_(u"An image used as the plan's cover page."),
    )
#
    plantype = schema.List(
        title=_(u"Plan Type"),
        required=False,
        description=_(u"One or more plan types that are appropriate for the plan."),
    )
#    agency = schema.TextLine(
#        title=_(u"Agency"),
#        required=True,
#        description=_(u"Name of the primary agency."),
#    )
    partners = schema.List(
        title=_(u"Partners"),
        required=False,
        description=_(u"Select the name of any partner agencies."),
    )

    agency = schema.Object(
        title=_(u"Primary Agency"),
        required=False,
        description=_(u"The agency or agencies responsible for the creation and implementation of the plan."),
        schema=IAgency, # specify the interface(s) of the addable types here
    )

#    partners = schema.Object(
#        title=_(u"Partner Agencies"),
#        required=False,
#        description=_(u"The agency or agencies responsible for the creation and implementation of the plan."),
#        schema=Interface, # specify the interface(s) of the addable types here
#    )
#
    layer = schema.Object(
        title=_(u"GIS Layer"),
        required=False,
        description=_(u"A GIS layer providing the spatial extent of the plan."),
        schema=ISimMap, # specify the interface(s) of the addable types here
    )
#
    layertype = schema.List(
        title=_(u"GIS Layer Type"),
        required=False,
        description=_(u"A GIS layer providing the spatial extent of the plan."),
    )
#
