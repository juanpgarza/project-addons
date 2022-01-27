# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models
from datetime import timedelta

class ProjectTask(models.Model):
    _inherit = "project.task"

    type_id_sequence = fields.Integer(string="Secuencia", related="type_id.sequence", store=True)

    type_id_dias_proxima_etapa = fields.Integer(string="Días est. próxima etapa", related="type_id.dias_estimados_nodo_siguiente")

    fecha_estimada_proxima_tarea = fields.Date()

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        task = super(ProjectTask, self).copy(default)
        task.type_id = self.type_id
        return task