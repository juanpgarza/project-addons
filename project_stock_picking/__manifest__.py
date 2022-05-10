# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "project_stock_picking",
    "summary": "",
    "version": "15.0.1.0.0",
    "category": "Project",
    "website": "https://github.com/juanpgarza/project-addons",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
                "project",
                "stock"
            ],
    "data": [
        'views/stock_picking_views.xml',
        'views/project_project_views.xml',        
        ],
    "installable": True,
}