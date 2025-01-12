from odoo import models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def force_draft_invoices(self):
        # Aplicar el cambio de estado solo al registro actual (la factura que se está viendo)
        if self.state != 'draft':
            self.sudo().button_draft()
        return True
