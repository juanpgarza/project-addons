# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectTSMService(models.Model):
    _name = 'project.tsm.service'
    _description = 'Servicios'
    _rec_name = "product_template_id"

    # project_id = fields.Many2one(string='',related='task_id.project_id')

    # def _default_user_id(self):
    #     import pdb; pdb.set_trace()
    #     if self._context.get("params")["id"] and self._context.get("params")["model"] == 'project.task':
    #         task_id = self.env["project.task"].browse(self._context.get("params")["id"])
    #         return task_id.user_ids[0]
    #     else:
    #         return False

    task_id = fields.Many2one(comodel_name="project.task",
                            ondelete="cascade",
                            string="Tarea",
                            )

    product_template_id = fields.Many2one(comodel_name="product.template",
                                        ondelete="restrict",
                                        string="servicio",
                                        domain="[('detailed_type','=','service')]",
                                        )

    product_uom_qty = fields.Float(string="Cant. pedida",
                                )

    qty_delivered = fields.Float(string="Cant. ejecutada",default=0)

    user_id = fields.Many2one(
                            'res.users', 
                            string='Usuario', 
                            # default=lambda self:self._default_user_id(),
                            )

    delivered_date = fields.Date(string="Fecha ejecución")

    # def write(self, vals):
    #     import pdb; pdb.set_trace()
    #     if 'user_id' in vals and not vals["user_id"]:
    #         vals["user_id"] = self.task_id.user_ids[0]

    #     res = super(ProjectTSMService, self).write(vals)

    #     return res

    @api.model
    def create(self, vals):
        service_id = super(ProjectTSMService, self).create(vals)
        if not service_id.user_id:
            service_id.user_id = service_id.task_id.user_ids[0]
        return service_id