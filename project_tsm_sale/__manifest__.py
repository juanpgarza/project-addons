# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project TSM Sale",
    "summary": "Project TSM Sale",
    "version": "15.0.1.0.0",
    "category": "Project",
    "website": "https://github.com/juanpgarza/project-addons",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        "project",
        "sale_project",
        "project_tsm"
        ],
    "data": [
        # "views/project_project_views.xml",        
        "data/ir_actions_server.xml",        
        "views/project_tsm_service_views.xml", 
        "views/project_task_views.xml",
        'security/ir.model.access.csv',        
        ],
    "installable": True,
    "maintainers": ["juanpgarza"],    
}
