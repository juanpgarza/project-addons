# Copyright 2019 Patrick Wilson <patrickraymondwilson@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ProjectMaterial(models.Model):

    _name = "project.material"
    _description = "Recursos utilizados"
    _rec_name = "product_id"

    project_id = fields.Many2one(
        comodel_name="project.project", string="Proyecto", ondelete="cascade", required=True
    )

    product_id = fields.Many2one(
        comodel_name="product.product", string="Producto", required=True
    )
    quantity = fields.Float(string="Cantidad")

    task_id = fields.Many2one(
        comodel_name="project.task", string="Tarea", ondelete="cascade", required=False, domain="[('project_id','=',project_id)]"
    )

    @api.constrains("quantity")
    def _check_quantity(self):
        for material in self:
            if not material.quantity > 0.0:
                raise ValidationError(
                    _("La cantidad debe ser mayor a 0.")
                )