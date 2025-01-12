from odoo import models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def force_draft_invoices(self):
        for invoice in self:
            if invoice.state != 'draft':
                # Desvincular los asientos contables asociados antes de cambiar el estado
                for move_line in invoice.line_ids:
                    move_line.unlink()

                # Forzar el cambio de estado a 'draft' sin más verificaciones
                invoice.sudo().button_draft()
        return True
