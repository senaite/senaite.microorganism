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
# Copyright 2020 by it's authors.
# Some rights reserved, see README and LICENSE.

from copy import copy

from bika.lims import api
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from senaite.ast import messageFactory as _
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IMicroorganismBehavior(model.Schema):

    gram_stain = schema.Choice(
        title=_(u"Gram stain"),
        vocabulary="senaite.microorganism.vocabularies.gram_stains",
        default="Undefined",
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


@implementer(IMicroorganismBehavior)
@adapter(IDexterityContent)
class Microorganism(object):

    def __init__(self, context):
        self.context = context
