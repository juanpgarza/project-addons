# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectTSMService(models.Model):
    _name = 'project.tsm.service'
    _description = 'Servicios'
    _rec_name = "product_template_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    project_id = fields.Many2one(string='Proyecto',related='task_id.project_id', store=True)

    date_deadline = fields.Date(related='task_id.date_deadline')

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
                                        string="Servicio",
                                        domain="[('detailed_type','=','service')]",
                                        )

    product_uom_qty = fields.Float(string="Pedido",
                                )

    qty_delivered = fields.Float(string="Ejecutado",
                                tracking=True,
                                default=0)

    user_id = fields.Many2one(
                            'res.users', 
                            string='Usuario',
                            tracking=True,
                            # default=lambda self:self._default_user_id(),
                            )
    user_ids = fields.Many2many(related='task_id.user_ids')

    partner_id = fields.Many2one(related='user_id.partner_id')

    delivered_date = fields.Date(string="Fecha ejecución", 
                    help="La fecha de ejecución se muestra en rojo "
                    "cuando la fecha de ejecución informada es posterior "
                    "a la fecha límite de la tarea o cuando esta última no fue informada",)

    state = fields.Selection([
            ("draft", "Pendiente"),
            ("done", "Revisado"),
            ("approved", "Aprobado"),
        ],
        default="draft",
        string="Estado",
        readonly=True,
        tracking=True,
        )

    subcontracted = fields.Boolean('Subcontratado', default=True)

    note = fields.Text(string="Observaciones")

    def action_set_draft(self):
        for rec in self:
            rec.write(
                {
                    'state': "draft"
                }
            )

    def action_set_approved(self):
        for rec in self:
            rec.write(
                {
                    'state': "approved"
                }
            )

    def action_set_done(self):
        for rec in self:
            rec.write(
                {
                    'state': "done"
                }
            )
