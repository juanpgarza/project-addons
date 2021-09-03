# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    accountable_user_id = fields.Many2one('res.users', string='Aprobador', tracking=True,
        domain="[('id','in',assignment_user_ids)]",
        help="Responsable por la finalización adecuada de una tarea."
        "Es quien asigna la tarea al responsable de su ejecución.")
        
    consulted_user_id = fields.Many2one('res.users', string='Consultado', tracking=True,
        domain="[('id','in',assignment_user_ids)]",
        help="Experto al que los involucrados acuden para comprender mejor algún aspecto relacionado con la tarea.")

    informed_user_id = fields.Many2one('res.users', string='Informado', tracking=True,
        domain="[('id','in',assignment_user_ids)]",
        help="Debe ser informado sobre el avance de la tarea. Generalmente al momento de su finalización.")

    assignment_user_ids = fields.Many2many(
        string="Roles habilitados",
        comodel_name="res.users",        
        compute="_compute_assignment_user_ids"
    )

    @api.depends("project_id")
    def _compute_assignment_user_ids(self):
        for task in self:
            task.assignment_user_ids = task.project_id.assignment_ids.mapped("user_id")