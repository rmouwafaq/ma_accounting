# -*- coding: utf-8 -*-
##############################################################################
#
#  
#
##############################################################################
from openerp.osv import fields,osv
class dakmar_sale_order(osv.osv):
    _inherit="sale.order"
    
    def _prepare_order_line_procurement(self, cr, uid, order, line, group_id=False, context=None):
        print "******** Trd  ******"
        vals = super(dakmar_sale_order, self)._prepare_order_line_procurement(cr, uid, order, line, group_id=group_id, context=context)
        location_id = order.partner_shipping_id.property_stock_customer.id
        vals['nombre_caisse']=line.nombre_caisse
        vals['location_id'] = location_id
        routes = line.route_id and [(4, line.route_id.id)] or []
        vals['route_ids'] = routes
        vals['warehouse_id'] = order.warehouse_id and order.warehouse_id.id or False
        vals['partner_dest_id'] = order.partner_shipping_id.id
        return vals
    
#     def _prepare_order_line_procurement(self, cr, uid, order, line, group_id=False, context=None):
#         date_planned = self._get_date_planned(cr, uid, order, line, order.date_order, context=context)
#         print "******* ",line.nombre_caisse
#         return {
#             'name': line.name,
#             'origin': order.name,
#             'date_planned': date_planned,
#             'product_id': line.product_id.id,
#             'nombre_caisse':line.nombre_caisse,
#             'product_qty': line.product_uom_qty,
#             'product_uom': line.product_uom.id,
#             'product_uos_qty': (line.product_uos and line.product_uos_qty) or line.product_uom_qty,
#             'product_uos': (line.product_uos and line.product_uos.id) or line.product_uom.id,
#             'company_id': order.company_id.id,
#             'group_id': group_id,
#             'invoice_state': (order.order_policy == 'picking') and '2binvoiced' or 'none',
#             'sale_line_id': line.id
#         }
      
class dakmar_sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    
    _columns = {
        'nombre_caisse':fields.integer('Nbr Caisse'),
    }
    
class procurement_order(osv.osv):
    _inherit = 'procurement.order'
    _columns = {
        'nombre_caisse':fields.integer('Nbr Caisse'),
        'poid_brut':fields.float('Poid brut'),
    }