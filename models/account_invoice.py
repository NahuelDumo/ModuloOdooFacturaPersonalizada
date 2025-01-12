from odoo import models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def force_draft_invoices(self):
        for invoice in self:
            if invoice.state != 'draft':
                # Desvincular el asiento contable relacionado (si es necesario)
                if invoice.state == 'posted' and invoice.line_ids:
                    for line in invoice.line_ids:
                        move = line.move_id
                        if move.state == 'posted':
                            # Cambiar directamente el estado del asiento a 'draft'
                            move.sudo().write({'state': 'draft'})
                    # Eliminar las líneas contables
                    invoice.sudo().line_ids.unlink()
                
                # Cambiar directamente el estado de la factura
                invoice.sudo().write({'state': 'draft'})
        return True
