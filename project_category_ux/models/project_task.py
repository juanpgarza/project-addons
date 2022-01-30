# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models
from datetime import timedelta

class ProjectTask(models.Model):
    _inherit = "project.task"
    _order = "type_id_sequence asc"

    type_id_sequence = fields.Integer(string="Secuencia", related="type_id.sequence", store=True)

    type_id_dias_proxima_etapa = fields.Integer(string="Días est. próxima etapa", related="type_id.dias_estimados_nodo_siguiente")

    fecha_estimada_proxima_tarea = fields.Date()

    fecha_estimada_inicio = fields.Date()

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        task = super(ProjectTask, self).copy(default)
        task.type_id = self.type_id
        return task

    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        
        if 'planned_date_begin' in vals:
            self.project_id.calcular_fechas_estimadas()

        return res
