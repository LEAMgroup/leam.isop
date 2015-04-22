
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.supermodel import model
from Products.Five import BrowserView

from subprocess import check_call

from leam.isop import MessageFactory as _

plan_types = SimpleVocabulary([
    SimpleTerm(value=u'Comprehensive Plan', title=_(u'Comprehensive Plan')),
    SimpleTerm(value=u'Transportation Plan', title=_(u'Transportation Plan')),
    SimpleTerm(value=u'Capital Improvement Plan', 
               title=_(u'Capital Improvement Plan')),
    SimpleTerm(value=u'Zoning Regulations', title=_(u'Zoning Regulations')),
    SimpleTerm(value=u'Economic Development Plan', 
               title=_(u'Economic Development Plan')),
    SimpleTerm(value=u'Subdivision Plan', title=_(u'Subdivision Plan')),
    SimpleTerm(value=u'Land Use Plan', title=_(u'Land Use Plan')),
    SimpleTerm(value=u'Other', title=_(u'Other')),
    ])

# Interface class; used to define content-type schema.

class IPlan(model.Schema, IImageScaleTraversable):
    """
    A planning document
    """
    document = NamedBlobFile(
            title = _(u'Document'),
            )
    downloadable = schema.Bool(
            title = _(u'Downloadable'),
            description = _(u'allow direct download from this repository'),
            default = True,
            )
    url = schema.URI(
            title = _(u'Primary URL'),
            description = _(u'required if plan is not downloadable'),
            required = False,
            )
    plantype = schema.Choice(
            title = _(u'Plan Type'),
            vocabulary = plan_types,
            required = True,
            )
    summary = RichText(
            title = _(u'Summary'),
            description = _(u'A brief summary of the plan including purpose '
                    u'and key goals.'),
            required = False,
            )
    cover = NamedBlobImage(
            title = _(u'Cover Page'),
            description = _(u'Cover page or other resentative image. '
                u'If not given, one will be generated automatically for you'),
            required = False,
            )
    partners = schema.TextLine(
            title = _(u'Partner Agencies'),
            required = False,
            )
    contact = schema.TextLine(
            title = _(u'Contact Name'),
            required = False,
            )
    email = schema.ASCIILine(
            title = _(u'Contact Email'),
            required = False,
            )
    phone = schema.ASCIILine(
            title = _(u'Contact Phone'),
            required = False,
            )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Plan(Container):

    def generate_cover(self):
        try:
            f = self.document.getBlob().open()
            cmd = 'pdftocairo -jpeg -singlefile {0} /tmp/cover'.format(f.name)
            check_call(cmd.split())
            self.cover.getBlob().consumeFile('/tmp/cover.jpg')
        except Exception:
            pass
        finally:
            f.close()


# View class
class PlanView(BrowserView):
    """ plan view class """

class SummaryView(BrowserView):
    """ plan summary view (used when rendering agency page) """

