# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    # def _get_domain(self):
    #     dominio = []
    #     if self.parent_partner_id:
    #         dominio = "['|',('partner_id','=',partner_id),('partner_id','=',parent_partner_id)]"
    #     else:
    #         dominio = "[('partner_id','=',partner_id)]"
    #     import pdb; pdb.set_trace()
    #     return dominio

    # parent_partner_id = fields.Many2one(related='partner_id.parent_id')

    # project_id = fields.Many2one('project.project', string='Proyecto', 
    #                         domain="['|',('partner_id','child_of',parent_partner_id),('partner_id','=',partner_id)]")

    project_id = fields.Many2one('project.project', string='Proyecto') # , readonly=True
    task_id = fields.Many2one('project.task', 
                                string='Tarea', 
                                domain="[('project_id', '=', project_id)]", 
                                compute='_compute_task_id', 
                                readonly=False, 
                                store=True)

    # @api.depends("partner_id")
    # @api.onchange('partner_id')
    # def _onchange_partner_id(self):
    #     #if not self.partner_id:
    #     self.project_id = False

    @api.onchange('project_id')
    def _onchange_project_id(self):
        #if not self.partner_id:
        if self.project_id and not self.partner_id:
            self.partner_id = self.project_id.partner_delivery_id

    # @api.onchange('partner_id')
    # def _onchange_partner_id(self):
    #     # import pdb; pdb.set_trace()
    #     dominio = []
    #     if self.parent_partner_id:
    #         # dominio = "['|',('partner_id','=',self.partner_id.id),('partner_id','=',self.parent_partner_id.id)]"
    #         self.project_id = self.env['project.project'].search(['|',('partner_id','=',self.partner_id.id),('partner_id','=',self.parent_partner_id.id)])
    #     else:
    #         self.project_id = self.env['project.project'].search([('partner_id','=',self.partner_id.id)])
    #         # dominio = "[('partner_id','=',self.partner_id.id)]"

    #     # self.project_id = self.env['project.project'].search(dominio)

    @api.depends('project_id')
    def _compute_task_id(self):
        for rec in self:
            if rec.project_id != rec.task_id.project_id:
                rec.task_id = False