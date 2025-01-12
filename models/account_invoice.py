from odoo import models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def force_draft_invoices(self):
        for invoice in self:
            if invoice.state != 'draft':
                # Si el estado es 'posted', despublicar el asiento contable relacionado
                if invoice.state == 'posted':
                    # Verificar si hay líneas contables asociadas
                    if invoice.line_ids:
                        # Forzar la despublicación de los asientos contables relacionados
                        for line in invoice.line_ids:
                            move = line.move_id
                            if move.state == 'posted':
                                move.sudo().button_draft()
                        # Eliminar las líneas contables para desvincular el asiento
                        invoice.sudo().line_ids.unlink()

                # Forzar el cambio de estado de la factura a 'draft'
                invoice.sudo().button_draft()
        return True
