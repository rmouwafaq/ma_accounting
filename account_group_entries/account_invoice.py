# -*- coding: utf-8 -*-

from openerp import models, api, _
from openerp.osv import fields, osv
class account_invoice_inh(models.Model):
    _inherit = "account.invoice"
    
    def inv_line_characteristic_hashcode(self, invoice_line):
        """Overridable hashcode generation for invoice lines. Lines having the same hashcode
        will be grouped together if the journal has the 'group line' option. Of course a module
        can add fields to invoice lines that would need to be tested too before merging lines
        or not."""
        return "%s-%s-%s-%s" % (
            invoice_line['account_id'],
            invoice_line.get('tax_code_id', 'False'),
            invoice_line.get('analytic_account_id', 'False'),
            invoice_line.get('date_maturity', 'False'),
        )
    
    @api.model
    def line_get_convert(self, line, part, date):
        account =self.env['account.account'].browse(line['account_id'])
        return {
            'date_maturity': line.get('date_maturity', False),
            'partner_id': part,
            'name': account.name,
            'date': date,
            'debit': line['price']>0 and line['price'],
            'credit': line['price']<0 and -line['price'],
            'account_id': line['account_id'],
            'analytic_lines': line.get('analytic_lines', []),
            'amount_currency': line['price']>0 and abs(line.get('amount_currency', False)) or -abs(line.get('amount_currency', False)),
            'currency_id': line.get('currency_id', False),
            'tax_code_id': line.get('tax_code_id', False),
            'tax_amount': line.get('tax_amount', False),
            'ref': line.get('ref', False),
            'quantity': line.get('quantity',1.00),
            'product_id': line.get('product_id', False),
            'product_uom_id': line.get('uos_id', False),
            'analytic_account_id': line.get('account_analytic_id', False),
        }
        
# class account_journal(osv.osv):
#     _inherit = 'account.journal'
#     _columns = {
#         'entries_description': fields.char('Description for grouped Account move Lines',size=64),
#     }

