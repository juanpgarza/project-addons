# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class Project(models.Model):
    _inherit = "project.project"

    milestone_ids = fields.One2many(comodel_name='project.milestone', 
                            inverse_name='project_id')

    def map_milestones(self, new_project_id):
        project = self.browse(new_project_id)
        milestones = self.env['project.milestone']
        milestone_ids = self.env['project.milestone'].with_context(active_test=False).search([('project_id', '=', self.id)]).ids
        defaults = {}
        for milestone in self.env['project.milestone'].browse(milestone_ids):
            defaults['project_id'] = new_project_id
            new_milestone = milestone.copy(defaults)
            milestones += new_milestone

        return project.write({'milestone_ids': [(6, 0, milestones.ids)]})

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        project = super(Project, self).copy(default)
        self.map_milestones(project.id)
        return project