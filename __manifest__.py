{
    'name': 'Force Draft Invoice',
    'version': '1.0',
    'category': 'Accounting',
    'author': 'Tu Nombre',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_invoice_view.xml',  # Asegúrate de que el archivo de vistas esté registrado aquí
    ],
    'installable': True,
    'application': False,
}
