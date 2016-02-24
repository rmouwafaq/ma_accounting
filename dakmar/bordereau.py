# -*- coding: utf-8 -*-
##############################################################################
#
#  
#
##############################################################################
from openerp.tools.translate import _
from openerp.osv import fields,osv

class bordereau(osv.osv):
    _name="dakmar.bordereau"
    _columns = {
        'name':fields.char('Reference bordereau',size=30,required=True),
        'provider_id':fields.many2one('res.partner', 'Fournisseur', required=True),
        'date_start':fields.datetime('Date debut', required=True),
        'date_end':fields.datetime('Date fin', required=True),
        'total_weight':fields.float('Poids Total Bordereau',required=True),
        'total_weight_brouillon':fields.float('Poids Total Bordereau'),
        'total_amount':fields.float('Montant total',required=True),
        'total_weight_receptions':fields.float('Poids Total Receptions',readonly=True),
        'payment_reference':fields.char('Reference paiement',size=60),
        'payment_amount':fields.float('Total Paiement'),
        'weights_difference':fields.float('Poids difference',readonly=True),
        'tax_weights_difference':fields.float('Taux difference (%)',readonly=True),
        'state': fields.selection([
                ('draft','Brouillon'),
                ('claim','Reclamation'),
                ('done','Done'),
                ('close','Fermer'),
            ], 'Etat bordereau',readonly=True,track_visibility='onchange', select=True),
        'bon_reception_ids': fields.one2many('stock.picking', 'bordereau_id', 'liste bon reception'),
        'average_price':fields.float('Prix moyenne',readonly=True),
    }
    
    _defaults={
        'state':'draft'
             }
    
    def button_calcul_total_weight(self,cr, uid, ids, context=None):
        cr.execute("SELECT total_weight,total_amount from dakmar_bordereau  WHERE id =%s",ids)
        result=cr.fetchall()[0]
        total_weight_bordereau=result[0]
        total_amount=result[1]
        if(total_weight_bordereau>0):
            cr.execute("SELECT sum(sm.product_uom_qty) from stock_picking sp,stock_move sm  WHERE sp.id=sm.picking_id and sp.bordereau_id =%s",ids)
            result=cr.fetchall()[0]
            total_weight_recepts=result[0]
            weights_difference=0.0
            taux_difference=0.0
            
            if(total_weight_recepts!=None):
                weights_difference=total_weight_bordereau-total_weight_recepts
                print "weights_difference =======",weights_difference
                #if(weights_difference>0):
                taux_difference=(weights_difference/total_weight_bordereau)*100
            
            state='draft'
            if(total_weight_recepts!=None):
                if(taux_difference>1):
                    state='claim'
                else:
                    state='done'
            else:
                total_weight_recepts=0.0
                
            average_price=total_amount/total_weight_bordereau
                    
            cr.execute("update dakmar_bordereau set average_price="+ str(average_price) +",state='"+ state +"',total_weight_brouillon=total_weight,total_weight_receptions="+ str(total_weight_recepts) +",weights_difference="+ str(weights_difference) +",tax_weights_difference="+ str(taux_difference) +" WHERE id =%s",ids)
                
            cr.execute("update stock_picking set average_price="+ str(average_price) +" WHERE bordereau_id=%s",ids)
        
        return True
    
    def get_bon_reception(self,cr,uid,ids,provider_id,date_debut=None,date_fin=None,context=None):
        bn_recept_ids_actif=self.pool.get("stock.picking").search(cr,uid,[('bordereau_id.id','>',0)],context)
        
        domain=[]
        if(len(ids)>0):
            bn_recept_ids_current_brd=self.pool.get("stock.picking").search(cr,uid,[('bordereau_id.id','=',ids[0])],context)
            domain=[
                    ('partner_id','=',provider_id),
                    ('date','>=',date_debut),
                    ('date','<=',date_fin),
                     '|',('id','not in',bn_recept_ids_actif),('id','in',bn_recept_ids_current_brd)
                    ]
        else:
            domain=[
                ('partner_id','=',provider_id),
                ('date','>=',date_debut),
                ('date','<=',date_fin),
                ('id','not in',bn_recept_ids_actif)
                ]
        
        bn_recept_ids=self.pool.get("stock.picking").search(cr,uid,domain,context)
        return {'value':{'bon_reception_ids':[(6,0,bn_recept_ids)]}}
    
    def action_confirm(self, cr, uid, ids, context=None):
        cr.execute("update dakmar_bordereau set state='done' WHERE id =%s",ids)
        return True
    def unlink(self, cr, uid, ids, context=None):
        context = context or {}
        for bordereau in self.browse(cr, uid, ids, context=context):
            if bordereau.state not in ('draft'):
                raise osv.except_osv(_('User Error!'), _('You can only delete draft Boredereau.'))
        return osv.osv.unlink(self, cr, uid, ids, context=context)
class bordereau_partner(osv.osv):
    _inherit = "res.partner"
    
    _columns = {
        'is_onp':fields.boolean('Fournisseur ONP '),
    }
    
    _defaults = {
        'is_onp':False,
    }