from odoo import models, exceptions, Command


class Property(models.Model):
    _inherit = 'estate.property'

    def sell_property(self):
        import ipdb
        ipdb.set_trace()
        for record in self:
            partner_id = record.buyer_id.id
            move_type = 'out_invoice'

            journals = self.env['account.journal'].search([('type', '=', 'sale')])
            if len(journals) <= 0:
                raise exceptions.ValidationError('No sale journal found')
            journal = journals[0]

            invoice_line_ids = [
                Command.create({
                    'name': '6% of Selling Price',
                    'quantity': 1,
                    'price_unit': record.selling_price * .06,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ]

            self.env['account.move'].create({
                'partner_id': partner_id,
                'move_type': move_type,
                'journal_id': journal.id,
                'invoice_line_ids': invoice_line_ids,
            })
        return super().sell_property()
