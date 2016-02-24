# -*- coding: utf-8 -*-
##############################################################################
#
#  
#
##############################################################################
from openerp.osv import fields,osv
from openerp.addons.ao_basic_module import ao_class 
from openerp import api
from openerp.tools.translate import _

class dakmar_account_invoice(osv.osv):
    _inherit = "account.invoice"
    
    _columns = {
        'container':fields.char('Container',size=64),
        'truck':fields.char('Camion',size=64),
        'destination':fields.char('Destination',size=64),
        'via':fields.char('Via',size=64),
        'total_lettre':fields.text('total en lettre')
    }
    def get_total_lettre(self, cr, uid, account_inv_id, context=None):
        account_inv=self.pool.get("account.invoice")
        account_inv_obj=account_inv.browse(cr, uid,[account_inv_id],context=context)
        amount_to_lettre= ao_class.amount_to_letter(account_inv_obj.amount_total,account_inv_obj.currency_id.symbol,"CTS",0)
        return amount_to_lettre.get_lettrer_amount()
    
    
    def create(self, cr, uid, values, context=None):
        account_inv_id=super(dakmar_account_invoice, self).create(cr, uid, values, context)
        tot_lettre=self.get_total_lettre(cr, uid, account_inv_id, context=context)
        self.write(cr, uid,[account_inv_id], {'total_lettre':tot_lettre}, context)
        return account_inv_id
       
    def write(self,cr, uid,ids, values, context=None):
        tot_lettre=self.get_total_lettre(cr, uid, ids[0], context=context)
        k=None
        if(values.has_key('total_lettre')):
            values.update({'total_lettre':tot_lettre})
        else:
            values['total_lettre']=self.get_total_lettre(cr, uid, ids[0], context=context)
            
        return super(dakmar_account_invoice, self).write(cr, uid,ids, values, context)
  

class dakmar_account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"

    _columns = {
        'nombre_caisse':fields.integer('Nbr Caisse'),
#         'average_price':fields.float('Prix moyenne'),
    }
