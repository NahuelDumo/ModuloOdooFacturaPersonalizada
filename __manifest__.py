{
    "name": "Custom Invoice Design",
    "version": "1.0",
    "depends": ["account", "l10n_ar"],
    "category": "Accounting",
    "summary": "Diseño personalizado de facturas con QR y CAE.",
    "description": "Este módulo agrega un diseño personalizado de factura, integrando datos del CAE y un código QR según normativa AFIP.",
    "data": [
        "views/report_invoice_template_a.xml",
        "views/report_invoice_template_b.xml",
        "views/report_tique_template.xml",
        "reports/invoice_report.xml",
    ],
    "installable": True,
    "application": False,
}