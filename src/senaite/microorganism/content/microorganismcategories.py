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

from plone.dexterity.content import Container
from senaite.microorganism.interfaces import IMicroorganismCategories
from zope.interface import implementer


@implementer(IMicroorganismCategories)
class MicroorganismCategories(Container):
    """Microorganism categories folder
    """
