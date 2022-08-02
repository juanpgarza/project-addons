# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project Material",
    "summary": "Asignar materiales a proyectos y tareas",
    "version": "15.0.1.0.0",
    "category": "Project",
    "website": "https://github.com/juanpgarza/project-addons",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        "project",
        ],
    "data": [
        "views/project_material_views.xml",        
        "views/project_project_views.xml",
        "views/project_task_views.xml",        
        "wizards/task_material_import_views.xml",
        "security/ir.model.access.csv",        
        ],
    "installable": True,
}
