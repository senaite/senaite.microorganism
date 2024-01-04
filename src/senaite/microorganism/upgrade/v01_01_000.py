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

from bika.lims import api
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base
from senaite.core.upgrade import upgradestep
from senaite.core.upgrade.utils import UpgradeUtils
from senaite.microorganism import logger
from senaite.microorganism import PRODUCT_NAME as product
from senaite.microorganism.content.microorganism import Microorganism

version = "1.1.0"


@upgradestep(product, version)
def upgrade(tool):
    portal = tool.aq_inner.aq_parent
    ut = UpgradeUtils(portal)
    ver_from = ut.getInstalledVersion(product)

    if ut.isOlderVersion(product, version):
        logger.info("Skipping upgrade of {0}: {1} > {2}".format(
            product, ver_from, version))
        return True

    logger.info("Upgrading {0}: {1} -> {2}".format(product, ver_from, version))

    # -------- ADD YOUR STUFF BELOW --------

    logger.info("{0} upgraded to version {1}".format(product, version))
    return True


@upgradestep(product, version)
def remove_microorganism_behavior(tool):
    """Removes IMicroorganismBehavior and uses IMicroorganismSchema instead
    """
    logger.info("Remove microorganism behavior ...")
    pt = api.get_tool("portal_types")
    fti = pt.get("Microorganism")

    # set the new schema
    schema = "senaite.microorganism.content.microorganism.IMicroorganismSchema"
    fti.schema = schema

    # remove behaviors
    behaviors = fti.behaviors
    to_remove = [
        "plone.app.dexterity.behaviors.metadata.IBasic",
        "senaite.microorganism.behaviors.microorganism.IMicroorganismBehavior",
    ]
    behaviors = filter(lambda b: b not in to_remove, behaviors)

    # Re-assign behaviors
    fti.behaviors = tuple(behaviors)

    # Microorganism content types are now folderish
    setup = api.get_setup()
    microorganisms = setup.microorganisms
    for microorganism in setup.microorganisms.objectValues():
        mid = microorganism.getId()
        microorganisms._delOb(mid)
        microorganism.__class__ = Microorganism
        microorganisms._setOb(mid, microorganism)
        BTreeFolder2Base._initBTrees(microorganisms[mid])
        microorganisms[mid].reindexObject()

    logger.info("Remove microorganism behaviors [DONE]")
