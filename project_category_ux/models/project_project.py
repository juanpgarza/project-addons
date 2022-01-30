# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from datetime import timedelta

class Project(models.Model):
    _inherit = "project.project"

    tarea_actual_id = fields.Many2one('project.task',
                        string='Tarea actual',
                        compute="_compute_tarea_actual",
                        store=True)

    fecha_estimada_inicio = fields.Date(related="tarea_actual_id.fecha_estimada_inicio")
    type_id_dias_proxima_etapa = fields.Integer(related="tarea_actual_id.type_id_dias_proxima_etapa")
    fecha_estimada_proxima_tarea = fields.Date(related="tarea_actual_id.fecha_estimada_proxima_tarea")

    def calcular_fechas_estimadas(self):
        for rec in self:
            
            fecha_estimada_proxima_anterior = False
            for task in rec.task_ids.sorted('type_id_sequence', reverse=False):

                task.fecha_estimada_inicio = task.planned_date_begin or fecha_estimada_proxima_anterior

                if task.fecha_estimada_inicio:
                    task.fecha_estimada_proxima_tarea = task.fecha_estimada_inicio + timedelta(days=task.type_id_dias_proxima_etapa)

                fecha_estimada_proxima_anterior = task.fecha_estimada_proxima_tarea or False

    @api.depends('task_ids.planned_date_begin')
    def _compute_tarea_actual(self):

        for rec in self:
            tareas_ordenadas = rec.task_ids.filtered(lambda x: x.planned_date_begin).sorted('type_id_sequence', reverse=True)
            if tareas_ordenadas:
                rec.tarea_actual_id = tareas_ordenadas[0]
            else:
                rec.tarea_actual_id = False
