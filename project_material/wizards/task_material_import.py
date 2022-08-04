# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
import base64
from io import BytesIO
from xlrd import open_workbook

import logging
_logger = logging.getLogger(__name__)

class TaskMaterialImport(models.TransientModel):
    _name = 'task.material.import.wizard'
    _description = 'Importación de productos'

    project_id = fields.Many2one(comodel_name="project.project",
                                string="Projecto")

    excel_file_for_import = fields.Binary("Archivo")
    file_name = fields.Char("File Name")

    @api.model
    def default_get(self, field_names):
        defaults = super(
            TaskMaterialImport, self).default_get(field_names)
        defaults['project_id'] = self.env.context['active_id']
        return defaults

    def do_import(self):
        try:
            inputx = BytesIO()
            inputx.write(base64.decodestring(self.excel_file_for_import))
            book = open_workbook(file_contents=inputx.getvalue())
        except TypeError as e:
            raise UserError(u'ERROR: {}'.format(e))

        sheet = book.sheets()[0]

        material_tarea = self.env["project.material"]
        for i in list(range(sheet.nrows)):
            # columna 0 = código de producto
            default_code = int(sheet.cell(i, 0).value)
            # columna 1 = descripcion
            # columna 2 = cantidad
            cantidad = sheet.cell(i, 2).value

            producto = self.env["product.template"].search([("default_code","=", default_code)])

            if not producto:
                raise ValidationError("No existe un producto con Referencia Interna {}".format(default_code))

            val = {
                # 'task_id': task_id.id,
                'project_id': self.project_id.id,
                'product_id': producto.product_variant_id.id,
                'quantity': cantidad
            }

            material_tarea.create(val)            