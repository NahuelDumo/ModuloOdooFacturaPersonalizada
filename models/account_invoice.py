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

                    # Añadir el impuesto del IVA 21% si la diferencia es significativa
                    if difference != 0:
                        # Calcular el impuesto IVA 21% basado en la diferencia
                        iva_percentage = 21 / 100
                        iva_amount = difference * iva_percentage

                        # Crear una línea contable para balancear el asiento, con el IVA
                        balancing_line = {
                            'move_id': invoice.id,
                            'account_id': invoice.journal_id.default_account_id.id,
                            'debit': abs(difference) if difference < 0 else 0.0,
                            'credit': abs(difference) if difference > 0 else 0.0,
                        }

                        # Agregar la línea del IVA
                        iva_line = {
                            'move_id': invoice.id,
                            'account_id': invoice.company_id.account_tax_collected_id.id,  # Cuenta del IVA 21% configurada en la compañía
                            'debit': iva_amount if iva_amount < 0 else 0.0,
                            'credit': iva_amount if iva_amount > 0 else 0.0,
                            'name': 'Ajuste IVA 21%',
                        }

                        # Crear las líneas contables
                        invoice.sudo().line_ids.create(balancing_line)
                        invoice.sudo().line_ids.create(iva_line)

                    # Eliminar las líneas contables (si es necesario para corregir inconsistencias)
                    invoice.sudo().line_ids.unlink()

                # Cambiar directamente el estado de la factura
                invoice.sudo().write({'state': 'draft'})

        return True
