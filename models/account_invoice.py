from odoo import models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def force_draft_invoices(self):
        for invoice in self:
            if invoice.state != 'draft':
                # Verificar si el asiento está publicado (estado 'posted')
                if invoice.state == 'posted':
                    # Cancelar el asiento contable antes de cambiar el estado de la factura
                    invoice.sudo().button_cancel()

                # Forzar el cambio de estado a 'draft' de la factura
                invoice.sudo().button_draft()
        return True
