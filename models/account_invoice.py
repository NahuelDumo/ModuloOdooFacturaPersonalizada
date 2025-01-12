from odoo import models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    @api.model
    def force_draft_invoices(self):
        records = self.search([('state', '!=', 'draft')])  # Buscar todas las facturas no en borrador
        for invoice in records:
            # Forzar el cambio de estado a 'draft' usando sudo para evitar restricciones
            if invoice.state != 'draft':
                invoice.sudo().button_draft()


        return True
