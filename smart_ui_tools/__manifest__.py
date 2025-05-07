# -*- coding: utf-8 -*-
{
    'name': "smart_ui_tools",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Outils UI intelligents
    """,

    'author': "Sarobidy Andriatseheno",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','fleet'],

    # always loaded
    'data': [
        'views/rma/view_list_vehicule_employee.xml',
        'views/rma/action.xml',
        'views/menu_main.xml',
        'security/groups_rma.xml',
        'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb':[
        'static/src/xml/page_liste_vehicle_rma.xml',
        'static/src/xml/page_details_vehicle_rma.xml',
        'static/src/xml/page_list_tache_vehicle_rma.xml'
    ],
    'application':True
}
