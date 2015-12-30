# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tools.translate import _
from openerp.osv import fields, osv
from openerp import models,tools

class wizard_releve_facture(osv.osv):
    _name = "wizard.releve.facture"
    _columns={
            'name':fields.char("name",size=32),
            
            }
    def print_releve_facture(self, cr, uid, ids, context=None):
        
        datas = {
            'ids': [],
            'model': 'barcode.label',
            'form': self.read(cr, uid, ids)[0]
        }
        account_invoices=self.pool.get("account.invoice").browse(cr,uid,context.get("active_ids"),context=context)
        partners=[]
        partner_name=""
        total_invoices={}
        total_amount=0.0
        for acc_invoice in account_invoices:
            if(acc_invoice.state!="open"):
                raise osv.except_osv( _('Error!'),
                            _("you must select the invoices state Opened"))
            if(acc_invoice.partner_id.name!= partner_name):
                partner=acc_invoice.partner_id
                total_amount=acc_invoice.amount_total
                if([partner.id,partner.name] not in partners):
                    partners.append([partner.id,partner.name])
                    total_invoices[str(partner.id)]=total_amount
                else:
                    total_invoices[str(partner.id)]=total_invoices[str(partner.id)]+total_amount
                
            else:
                total_amount=total_amount+acc_invoice.amount_total
        if(len(partners)>1):
            raise osv.except_osv( _('Error!'),
                            _("you must select a single client invoices"))
        datas['partners']=partners
        print "partners==",partners
        datas['total_invoices']=total_invoices
        print "total_invoices==",total_invoices   
        
        return self.pool['report'].get_action(cr, uid, [], 'samarkand.report_relevefacture', data=datas, context=context)
    
    