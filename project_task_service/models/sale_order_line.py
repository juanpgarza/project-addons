# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_create_project(self):
        res = super(SaleOrderLine,self)._timesheet_create_project()

        # por acá SOLO en las líneas que crean proyecto.
        # la idea es que solo tenga una por sale.order.
        # lo tendré que controlar?

        # todas las lineas cuyo producto tiene un estandar asociado
        # order_line_ids = self.order_id.mapped("order_line").filtered(lambda x: x.product_id.estandar_id)
        order_line_ids = self.order_id.mapped("order_line").filtered(lambda x: x.product_id.detailed_type == 'service')

        servicio_tarea = self.env["project.task.service"]
        for line in order_line_ids:
            # se busca la tarea tiene el mismo estandar que el producto.
            # tarea = self.project_id.task_ids.filtered(lambda x: x.task_estandar_id.id == line.product_id.estandar_id.id and x.project_id.id == self.project_id.id)
            tarea = self.project_id.task_ids.filtered(lambda x: x.type_id.id == 47)

            for t in tarea:
                # se crea el servicio para la tarea
                val = {
                    'task_id': t.id,
                    'product_template_id': line.product_id.product_tmpl_id.id,
                    'cantidad_pedida': line.product_uom_qty
                }
                servicio_tarea.create(val)