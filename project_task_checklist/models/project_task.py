from odoo import _, api, fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    check_ids = fields.One2many(
        comodel_name="project.task.check",
        inverse_name="task_id",
        string="Checklist",
        copy=True
    )

    def map_checks(self, new_task):
        """Copy and map checks from old to new task"""
        self.ensure_one()   # ⚠️ garantiza que sea de a una tarea

        checks = self.env['project.task.check']
        # queremos copiar también archivados, sin active_test
        old_checks = self.env['project.task.check'].with_context(active_test=False).search(
            [('task_id', '=', self.id)], order='sequence'
        )

        for check in old_checks:
            new_check = check.copy({'task_id': new_task.id})
            checks += new_check

        return new_task.write({'check_ids': [(6, 0, checks.ids)]})

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        new_tasks = super(ProjectTask, self).copy(default)

        if len(self) == 1:
            # caso singleton
            for follower in self.message_follower_ids:
                new_tasks.message_subscribe(
                    partner_ids=follower.partner_id.ids,
                    subtype_ids=follower.subtype_ids.ids
                )
            self.map_checks(new_tasks)
        else:
            # caso batch: varias tareas de golpe (ej: duplicar proyecto con muchas tareas)
            for old_task, new_task in zip(self, new_tasks):
                for follower in old_task.message_follower_ids:
                    new_task.message_subscribe(
                        partner_ids=follower.partner_id.ids,
                        subtype_ids=follower.subtype_ids.ids
                    )
                old_task.map_checks(new_task)

        return new_tasks
