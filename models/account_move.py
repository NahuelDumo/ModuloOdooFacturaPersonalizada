from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    x_cae_number = fields.Char(string="Número de CAE", help="Número de CAE otorgado por AFIP")
    x_cae_due_date = fields.Date(string="Fecha de Vencimiento del CAE", help="Fecha de vencimiento del CAE")

    def _get_invoice_qr_data(self):
        """
        Genera la información necesaria para el código QR según normativa AFIP
        """
        for record in self:
            qr_data = {
                "cuit": record.company_id.vat,
                "pto_vta": record.journal_id.l10n_latam_document_number,
                "tipo_cmp": record.l10n_latam_document_type_id.code,
                "nro_cmp": record.name,
                "importe": record.amount_total,
                "moneda": record.currency_id.name,
                "fecha": record.invoice_date.strftime('%Y-%m-%d'),
                "cae": record.x_cae_number,
                "vto_cae": record.x_cae_due_date.strftime('%Y-%m-%d') if record.x_cae_due_date else '',
            }
            return qr_data