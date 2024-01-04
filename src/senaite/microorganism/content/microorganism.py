# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.MICROORGANISM.
#
# SENAITE.MICROORGANISM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2020-2024 by it's authors.
# Some rights reserved, see README and LICENSE.

from AccessControl import ClassSecurityInfo
from bika.lims import api
from plone.autoform import directives
from plone.supermodel import model
from Products.CMFCore import permissions
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.content.base import Container
from senaite.core.schema import UIDReferenceField
from senaite.core.z3cform.widgets.uidreference import UIDReferenceWidgetFactory
from senaite.microorganism import messageFactory as _
from senaite.microorganism.interfaces import IMicroorganism
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant


class IMicroorganismSchema(model.Schema):
    """Schema interface
    """

    title = schema.TextLine(
        title=u"Title",
        required=True,
    )

    description = schema.Text(
        title=u"Description",
        required=False,
    )

    gram_stain = schema.Choice(
        title=_(u"Gram stain"),
        vocabulary="senaite.microorganism.vocabularies.gram_stains",
        required=False,
    )

    shape = schema.Choice(
        title=_(u"Shape"),
        vocabulary="senaite.microorganism.vocabularies.shapes",
        required=False,
    )

    glass = schema.Bool(
        title=_(u"GLASS organism"),
        description=_(
            "Whether this is an infectious organism included in the Global "
            "Antimicrobial Resistance Surveillance System (GLASS) for the "
            "the collection, analysis and sharing of Antimicrobial Resistance "
            "(AMR) data at a global level"
        ),
        required=False,
    )

    multi_resistant = schema.Bool(
        title=_(u"MRO Organism"),
        description=_(
            "Whether this organism is considered multi resistant (MRO)",
        ),
        required=False,
    )

    mro_phenotype = schema.TextLine(
        title=_(u"MRO phenotype"),
        required=False,
    )

    category = UIDReferenceField(
        title=_(u"Category / Group"),
        description=_(
            u"The category or group this microorganism belongs to"
        ),
        allowed_types=("MicroorganismCategory", ),
        multi_valued=False,
        required=False,
    )

    directives.widget(
        "category",
        UIDReferenceWidgetFactory,
        catalog=SETUP_CATALOG,
        query={
            "portal_type": "MicroorganismCategory",
            "is_active": True,
            "sort_on": "title",
            "sort_order": "ascending",
        },
        display_template="<a href='${url}'>${title}</a>",
        columns=[
            {
                "name": "title",
                "width": "30",
                "align": "left",
                "label": _(u"Title"),
            }, {
                "name": "description",
                "width": "70",
                "align": "left",
                "label": _(u"Description"),
            },
        ],
        limit=15,
    )

    @invariant
    def validate_title(data):
        """Checks if the title is unique
        """
        # https://community.plone.org/t/dexterity-unique-field-validation
        context = getattr(data, "__context__", None)
        if context is not None:
            if context.title == data.title:
                # nothing changed
                return

        if not data.title:
            # Support for non-required fields
            return

        query = {
            "portal_type": "Microorganism",
            "title": data.title
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) > 0:
            raise Invalid(_("Title must be unique"))


@implementer(IMicroorganism, IMicroorganismSchema)
class Microorganism(Container):
    """Microorganism content
    """
    # Catalogs where this type will be catalogued
    _catalogs = [SETUP_CATALOG]

    security = ClassSecurityInfo()
    exclude_from_nav = True

    @security.protected(permissions.View)
    def getGramStain(self):
        accessor = self.accessor("gram_stain")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setGramStain(self, value):
        mutator = self.mutator("gram_stain")
        mutator(self, value)

    @security.protected(permissions.View)
    def getShape(self):
        accessor = self.accessor("shape")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setShape(self, value):
        mutator = self.mutator("shape")
        mutator(self, value)

    @security.protected(permissions.View)
    def getGlass(self):
        accessor = self.accessor("glass")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setGlass(self, value):
        mutator = self.mutator("glass")
        mutator(self, value)

    @security.protected(permissions.View)
    def getMultiResistant(self):
        accessor = self.accessor("multi_resistant")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setMultiResistant(self, value):
        mutator = self.mutator("multi_resistant")
        mutator(self, value)

    @security.protected(permissions.View)
    def getMROPhenotype(self):
        accessor = self.accessor("mro_phenotype")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setMROPhenotype(self, value):
        mutator = self.mutator("mro_phenotype")
        mutator(self, value)

    @security.protected(permissions.View)
    def getCategory(self):
        accessor = self.accessor("category")
        return accessor(self)

    @security.protected(permissions.View)
    def getRawCategory(self):
        accessor = self.accessor("category", raw=True)
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setCategory(self, value):
        mutator = self.mutator("category")
        mutator(self, value)
