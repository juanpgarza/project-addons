# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class ProjectAssignment(models.Model):
    _inherit = "project.assignment"

    partner_id = fields.Many2one(
        related="user_id.partner_id"
    )

    mobile = fields.Char(
        related="user_id.partner_id.mobile"
    )

    email = fields.Char(
        related="user_id.partner_id.email"
    )

