# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project TSM Account",
    "summary": "Project TSM Account",
    "version": "15.0.1.0.0",
    "category": "Project",
    "website": "https://github.com/juanpgarza/project-addons",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        "project",
        "sale_project",
        "project_tsm",        
        "project_tsm_sale",
        ],
    "data": [
        "wizards/invoice_add_tsm_service_views.xml",
        "views/account_move_views.xml",        
        "data/ir_actions_server.xml",        
        "views/project_tsm_service_views.xml",
        'security/ir.model.access.csv',        
        ],
    "installable": True,
    "maintainers": ["juanpgarza"],    
}
