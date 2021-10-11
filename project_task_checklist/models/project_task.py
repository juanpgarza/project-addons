# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    check_ids = fields.One2many(
        comodel_name="project.task.check",
        inverse_name="task_id",
        string="Checklist",
        copy=True
    )

    def map_checks(self, new_task_id):
        """ copy and map checks from old to new task """
        task = self.browse(new_task_id)
        checks = self.env['project.task.check']
        # We want to copy archived task, but do not propagate an active_test context key
        check_ids = self.env['project.task.check'].with_context(active_test=False).search([('task_id', '=', self.id)], order='sequence').ids
        defaults = {}
        for check in self.env['project.task.check'].browse(check_ids):
            defaults['task_id'] = new_task_id
            new_check = check.copy(defaults)
            checks += new_check

        return task.write({'check_ids': [(6, 0, checks.ids)]})

    # src/addons/project/models/project.py:440
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        task = super(ProjectTask, self).copy(default)
        for follower in self.message_follower_ids:
            task.message_subscribe(partner_ids=follower.partner_id.ids, subtype_ids=follower.subtype_ids.ids)

        self.map_checks(task.id)
        return task