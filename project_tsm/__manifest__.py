# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Gestión de servicios en tareas",
    "summary": "Gestión de servicios en tareas",
    "version": "15.0.1.0.0",
    "category": "Project",
    "website": "https://github.com/juanpgarza/project-addons",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        "project",
        ],
    "data": [
        'security/tsm_security.xml',
        "data/ir_actions_server.xml",        
        "views/project_tsm_service_views.xml",        
        "views/project_task_views.xml",
        'security/ir.model.access.csv',        
        "views/project_project_views.xml",
        ],
    "installable": True,
    "maintainers": ["juanpgarza"],    
}
