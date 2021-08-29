# Copyright 2021 ITSur - Juan Pablo Garza <jgarza@itsur.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
import base64
from io import BytesIO
from xlrd import open_workbook

import logging
_logger = logging.getLogger(__name__)

class TaskMaterialImport(models.TransientModel):
    _name = 'task.material.import.wizard'
    _description = 'Importación de productos'

    task_id = fields.Many2one(comodel_name="project.task",
                                string="Tarea")

    project_id = fields.Many2one(comodel_name="project.project",
                                string="Projecto")

    excel_file_for_import = fields.Binary("Archivo")
    file_name = fields.Char("File Name")

    @api.model
    def _default_project_category_enable(self):
        return 'type_id' in self.env['project.task']._fields

    project_category_enable = fields.Boolean("project_category_enable", default=_default_project_category_enable)

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

        material_tarea = self.env["project.task.material"]
        for i in list(range(sheet.nrows)):
            # columna 0 = código de producto
            default_code = int(sheet.cell(i, 0).value)
            # columna 1 = descripcion
            # columna 2 = cantidad
            cantidad = sheet.cell(i, 2).value
            # columna 3 = xmlID del estandar
            # estandar_id = self.env.ref(sheet.cell(i, 0).value)
            # import pdb; pdb.set_trace()
            if self.task_id:
                # si informó la tarea, no se asigna a esa tarea sin tener en cuenta la categoría
                task_id = self.task_id
            else:
                if self.project_category_enable:
                    # falta verificar que el archivo tenga las columnas necesarias
                    type_id = self.env["project.type"].search([('name','=',sheet.cell(i, 3).value)])
                    task_id = self.env["project.task"].search([('project_id','=',self.project_id.id),('type_id','=',type_id.id)])
                else:
                    raise UserError("Debe informar una tarea o activar el módulo de categorías")

            producto = self.env["product.template"].search([("default_code","=", default_code)])

            val = {
                'task_id': task_id.id,
                'product_id': producto.product_variant_id.id,
                'quantity': cantidad
            }

            material_tarea.create(val)            