# Copyright 2021 ITSur - Juan Pablo Garza <jgarza@itsur.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project Task Checklist",
    "summary": "",
    "version": "13.0.1.0.0",
    "category": "Project",
    "website": "https://github.com/itsurnqn/project-addons",
    "author": "ITSur",
    "license": "AGPL-3",
    "depends": ["project"],
    "data": [
        "security/ir.model.access.csv",
        'views/project_task_check_views.xml',
        'views/project_task_views.xml',
        'views/project_project_views.xml',        
        ],
    "installable": True,
}
