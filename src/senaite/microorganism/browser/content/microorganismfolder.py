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

import collections

from bika.lims import _ as _c
from bika.lims import api
from bika.lims.catalog import SETUP_CATALOG
from bika.lims.utils import get_link_for
from plone.memoize import view
from senaite.app.listing import ListingView
from senaite.microorganism import messageFactory as _
from senaite.microorganism.config import GRAM_STAIN_OPTIONS


class MicroorganismFolderView(ListingView):
    """Microorganisms listing view
    """

    def __init__(self, context, request):
        super(MicroorganismFolderView, self).__init__(context, request)

        self.catalog = SETUP_CATALOG

        self.contentFilter = {
            "portal_type": "Microorganism",
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }

        self.context_actions = {
            _c("Add"): {
                "url": "++add++Microorganism",
                "icon": "add.png"}
            }

        self.show_select_column = True

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _c("Title"),
                "index": "sortable_title"
            }),
            ("gram_stain", {
                "title": _("Gram stain")
            }),
            ("glass", {
                "title": _("GLASS"),
                "type": "boolean",
            }),
            ("mro", {
                "title": _("MRO"),
                "type": "boolean",
            }),
            ("mro_phenotype", {
                "title": _("MRO phenotype")
            }),
            ("Description", {
                "title": _c("Description"),
                "index": "Description"
            }),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _c("Active"),
                "contentFilter": {"is_active": True},
                "transitions": [],
                "columns": self.columns.keys(),
            }, {
                "id": "inactive",
                "title": _c("Inactive"),
                "contentFilter": {'is_active': False},
                "transitions": [],
                "columns": self.columns.keys(),
            }, {
                "id": "all",
                "title": _c("All"),
                "contentFilter": {},
                "columns": self.columns.keys(),
            },
        ]

    def update(self):
        """Update hook
        """
        super(MicroorganismFolderView, self).update()

    def before_render(self):
        """Before template render hook
        """
        super(MicroorganismFolderView, self).before_render()

    def folderitem(self, obj, item, index):
        """Service triggered each time an item is iterated in folderitems.
        The use of this service prevents the extra-loops in child objects.
        :obj: the instance of the class to be foldered
        :item: dict containing the properties of the object to be used by
            the template
        :index: current index of the item
        """
        item["replace"]["Title"] = get_link_for(obj)

        obj = api.get_object(obj)
        item["gram_stain"] = self.get_gram_stain_title(obj.gram_stain)
        item["glass"] = obj.glass
        item["mro"] = obj.multi_resistant
        item["mro_phenotype"] = obj.mro_phenotype
        item["class"]["mro"] = "center"
        item["class"]["glass"] = "center"

        max_length = 150
        description = obj.description
        if len(description) > max_length:
            item["Description"] = "{} ...".format(description[:max_length-4])
        return item

    def get_children_hook(self, parent_uid, child_uids=None):
        """Hook to get the children of an item
        """
        super(MicroorganismFolderView, self).get_children_hook(
            parent_uid, child_uids=child_uids)

    @view.memoize
    def get_gram_stain_title(self, gram_stain_value):
        """Returns the title of the gram satin value passed-in
        """
        return dict(GRAM_STAIN_OPTIONS).get(gram_stain_value, "")
