from odoo import models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def force_draft_invoices(self):
        for invoice in self:
            if invoice.state != 'draft':
                # Si la factura está publicada, manejar sus asientos contables
                if invoice.state == 'posted' and invoice.line_ids:
                    for line in invoice.line_ids:
                        move = line.move_id
                        if move.state == 'posted':
                            # Cambiar directamente el estado del asiento a 'draft'
                            move.sudo().write({'state': 'draft'})

                    # Ajustar los débitos y créditos para balancear el asiento
                    debit_total = sum(line.debit for line in invoice.line_ids)
                    credit_total = sum(line.credit for line in invoice.line_ids)
                    difference = debit_total - credit_total

                    if difference != 0:
                        # Crear una línea contable para balancear el asiento
                        balancing_line = {
                            'move_id': invoice.id,
                            'account_id': invoice.journal_id.default_account_id.id,
                            'debit': abs(difference) if difference < 0 else 0.0,
                            'credit': abs(difference) if difference > 0 else 0.0,
                        }
                        invoice.sudo().line_ids.create(balancing_line)

                    # Eliminar las líneas contables (si es necesario para corregir inconsistencias)
                    invoice.sudo().line_ids.unlink()

                # Cambiar directamente el estado de la factura
                invoice.sudo().write({'state': 'draft'})

        return True
