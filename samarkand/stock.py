from openerp.osv import fields, osv

class samarkand_stock_move(osv.osv):
    _inherit="stock.move"
    _columns={
              'qty_available':fields.float('Quantite en stock',readonly=True),
              }
    
    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False, loc_dest_id=False, partner_id=False):
        """ On change of product id, if finds UoM, UoS, quantity and UoS quantity.
        @param prod_id: Changed Product id
        @param loc_id: Source location id
        @param loc_dest_id: Destination location id
        @param partner_id: Address id of partner
        @return: Dictionary of values
        """
        if not prod_id:
            return {}
        user = self.pool.get('res.users').browse(cr, uid, uid)
        lang = user and user.lang or False
        if partner_id:
            addr_rec = self.pool.get('res.partner').browse(cr, uid, partner_id)
            if addr_rec:
                lang = addr_rec and addr_rec.lang or False
        ctx = {'lang': lang}

        product = self.pool.get('product.product').browse(cr, uid, [prod_id], context=ctx)[0]
        uos_id = product.uos_id and product.uos_id.id or False
        result = {
            'name': product.partner_ref,
            'product_uom': product.uom_id.id,
            'product_uos': uos_id,
            'product_uom_qty': 1.00,
            'product_uos_qty': self.pool.get('stock.move').onchange_quantity(cr, uid, ids, prod_id, 1.00, product.uom_id.id, uos_id)['value']['product_uos_qty'],
        }
        if loc_id:
            result['location_id'] = loc_id
            
            quant_obj=self.pool.get('stock.quant')
            quant_ids=quant_obj.search(cr,uid,[("location_id","=",loc_id),("product_id","=",product.id)],context=None)
            if(len(quant_ids)>0):
                quants_product=quant_obj.read(cr,uid,quant_ids,context=None)
                result['qty_available']=0.0
                for quant_product in quants_product:
                    qty_available=quant_product["qty"]
                    result['qty_available']=result['qty_available'] + qty_available
        if loc_dest_id:
            result['location_dest_id'] = loc_dest_id
        
        return {'value': result}
        