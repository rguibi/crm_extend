{
    "name": "CRM extend",
    "author": "Rgb",
    "version": "12.0.1.1.0",
    "category": "CRM",
    "depends": [
        "crm",'sale'
    ],
    "data": [
        "security/crm_extend.xml",
    "./security/ir.model.access.csv",
    "./views/crm.xml",
    "./views/sale_order.xml",
    "./views/invoice.xml",
    "./reports/quot.xml",
    "./reports/invoice.xml",
    ],
    "license": 'LGPL-3',
    'installable': True,
    'application': True,
}
