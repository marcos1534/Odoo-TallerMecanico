# -*- coding: utf-8 -*-
{
        'name': "Taller Mecánico",

    'summary': "Módulo para gestión de un taller mecánico",

    'description': """
        Este módulo permite gestionar mecánicos, citas, clientes, proveedores, repuestos y vehículos en un taller mecánico.
    """,

    'author': "Marcos José Ibáñez Quintana",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'snailmail'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/cita.xml',
        'views/cliente.xml',
        'views/factura.xml',
        'views/mecanico.xml',
        'views/menus.xml',
        'views/proveedor.xml',
        'views/repuestos.xml',
        'views/vehiculo.xml',
        'reports/report_factura.xml',
        'reports/report_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'icon': 'mjiq_taller/static/description/llave-inglesa.png',

    'installable': True,
    'application': True,
}