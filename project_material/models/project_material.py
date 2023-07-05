# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ProjectMaterial(models.Model):
    _name = 'project.material'
    _description = 'Materiales de la tarea'
    _rec_name = "product_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    project_id = fields.Many2one(
        comodel_name="project.project", string="Proyecto", ondelete="cascade", required=True
    )
    task_id = fields.Many2one(
        comodel_name="project.task", string="Tarea", ondelete="cascade", required=False, domain="[('project_id','=',project_id)]"
    )    
    product_id = fields.Many2one(
        comodel_name="product.product", string="Producto", required=True
    )
    quantity = fields.Float("Cantidad")
    qty_available = fields.Float("Cantidad a mano", related='product_id.qty_available')
    virtual_available = fields.Float("Cantidad pronosticada", related='product_id.virtual_available')    
    added = fields.Boolean("Agregado")

    @api.constrains("quantity")
    def _check_quantity(self):
        for material in self:
            if not material.quantity > 0.0:
                raise ValidationError(
                    ("La cantidad de material debe ser mayor a 0.")
                )