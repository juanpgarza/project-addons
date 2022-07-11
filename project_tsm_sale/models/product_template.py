# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    service_type = fields.Selection(
        selection_add=[
            ("project_task", "Tarea de proyecto"),
        ],
        ondelete={"project_task": "cascade"},
    )
