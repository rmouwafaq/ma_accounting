# -*- coding: utf-8 -*-
##############################################################################
#
#  
#
##############################################################################
from openerp.osv import fields,osv
from openerp import SUPERUSER_ID, api

class bon_reception(osv.osv):
    _inherit = "stock.picking"
    
    _columns = {
       # 'name':fields.char('name',size=50),
        'bordereau_id':fields.many2one('dakmar.bordereau', 'ID Bordereau'),
        'driver_id': fields.many2one('res.partner', 'Chauffeur'),
        'vehicule_matricule':fields.char('Matricule vehicule',size=32),
        'average_price':fields.float('Prix moyenne'),
        'container':fields.char('Container',size=64),
        'truck':fields.char('Camion',size=64),
        'destination':fields.char('Destination',size=64),
        'via':fields.char('Via',size=64),
    }
    
    def _get_default_picking_type(self,cr,uid,context=None):
        picking_type=self.pool.get("stock.picking.type")
        picking_type_ids=self.pool.get("stock.picking.type").search(cr,uid,[])
        for pt in picking_type.browse(cr, uid, picking_type_ids):
            if(pt.name=='Receipts'):
                return pt.id
        return 1
    def _create_invoice_from_picking(self, cr, uid, picking, vals, context=None):
        ''' This function simply creates the invoice from the given values. It is overriden in delivery module to add the delivery costs.
        '''
        invoice_obj = self.pool.get('account.invoice')
        vals['container']=picking.container
        vals['truck']=picking.truck
        vals['destination']=picking.destination
        vals['via']=picking.via
        id_invoice=invoice_obj.create(cr, uid, vals, context=context)
        #invoice_obj.set_total_lettre(cr, uid, id_invoice, context=context)
        return id_invoice
    
    _defaults = {
        'move_type':'one',
        'invoice_state':'2binvoiced',
        'picking_type_id':_get_default_picking_type
    }
    
class dakmar_stock_move(osv.osv):
    _inherit = "stock.move"
    
    _columns = {
        'poid_brut':fields.float('Poid Brut'),
        'nombre_caisse':fields.integer('Nbr Caisse'),
    }
    
    _defaults = {
        'invoice_state':'2binvoiced'
    }
    
    def _create_invoice_line_from_vals(self, cr, uid, move, invoice_line_vals, context=None):
        picking_ids=[]
        picking_ids.append(move.picking_id.id)
        picking_obj=self.pool.get('stock.picking').browse(cr,uid,picking_ids,context=context)
#         invoice_line_vals['average_price']=picking_obj.average_price
        invoice_line_vals['poid_brut']=move.poid_brut
        invoice_line_vals['nombre_caisse']=move.nombre_caisse
        return self.pool.get('account.invoice.line').create(cr, uid, invoice_line_vals, context=context)
    
    @api.cr_uid_ids_context
    def _picking_assign(self, cr, uid, move_ids, procurement_group, location_from, location_to, context=None):
        """Assign a picking on the given move_ids, which is a list of move supposed to share the same procurement_group, location_from and location_to
        (and company). Those attributes are also given as parameters.
        """
        for move_obj in self.browse(cr, uid, move_ids, context=context):
            if(move_obj.procurement_id.nombre_caisse != move_obj.nombre_caisse):
                self.write(cr, uid, [move_obj.id], {'nombre_caisse':move_obj.procurement_id.nombre_caisse,
                                                    'poid_brut':move_obj.procurement_id.poid_brut
                                                    }, context=context)
        pick_obj = self.pool.get("stock.picking")
        picks = pick_obj.search(cr, uid, [
                ('group_id', '=', procurement_group),
                ('location_id', '=', location_from),
                ('location_dest_id', '=', location_to),
                ('state', 'in', ['draft', 'confirmed', 'waiting'])], context=context)
        if picks:
            pick = picks[0]
        else:
            move = self.browse(cr, uid, move_ids, context=context)[0]
            values = {
                'origin': move.origin,
                'company_id': move.company_id and move.company_id.id or False,
                'move_type': move.group_id and move.group_id.move_type or 'direct',
                'partner_id': move.partner_id.id or False,
                'picking_type_id': move.picking_type_id and move.picking_type_id.id or False,
            }
            pick = pick_obj.create(cr, uid, values, context=context)
        return self.write(cr, uid, move_ids, {'picking_id': pick}, context=context)
    
class dakmar_picking_type(osv.osv):
    _inherit = "stock.picking.type"
    
    _defaults={
               'name':'Receipts'
               }   
class dakmar_stock_pack_operation(osv.osv):
    _inherit = "stock.pack.operation"
    
    _columns = {
        'nombre_caisse':fields.integer('Nbr Caisse'),
        'poid_brut':fields.float('Poid brut'),
    }
