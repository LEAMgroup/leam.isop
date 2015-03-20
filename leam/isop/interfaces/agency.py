from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from leam.isop import isopMessageFactory as _



class IAgency(Interface):
    """A planning agency"""

    # -*- schema definition goes here -*-
    autotag = schema.Bool(
        title=_(u"Auto Tag"),
        required=False,
        description=_(u"Should the title of this agency be used as a tag?"),
    )
#
    coverage = schema.Object(
        title=_(u"Default Area"),
        required=False,
        description=_(u"Identify a GIS layer to be used as the default for plan boundaries."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    overview = schema.Text(
        title=_(u"Overview"),
        required=False,
        description=_(u"A brief overview of the agency."),
    )
#
    address = schema.Text(
        title=_(u"Address"),
        required=False,
        description=_(u"Address and contact information."),
    )
#
    phone = schema.Text(
        title=_(u"Phone"),
        required=False,
        description=_(u"Primary phone number."),
    )
#
    logo = schema.Bytes(
        title=_(u"Logo"),
        required=False,
        description=_(u"Image to be used as the agency's logo."),
    )
#
