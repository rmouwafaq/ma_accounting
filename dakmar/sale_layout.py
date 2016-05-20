# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-Today OpenERP SA (<http://www.openerp.com>).
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
import openerp
from openerp.osv import osv, fields
from itertools import groupby
import openerp.addons.sale_layout.models.sale_layout as sale_layout

def grouplines_inh(self, ordered_lines, sortkey):
    """Return lines from a specified invoice or sale order grouped by category"""
    grouped_lines = []
    for key, valuesiter in groupby(ordered_lines, sortkey):
        group = {}
        group['lines'] = list(v for v in valuesiter)
        group['category'] =key 
        #if 'subtotal' in key and key.subtotal is True:
        group['subtotal'] = sum(line.price_subtotal for line in group['lines'])
        group['poid_brut'] = sum(line.poid_brut for line in group['lines'])
        group['poid_net'] = sum(line.quantity for line in group['lines'])
        group['nombre_caisse'] = sum(line.nombre_caisse for line in group['lines'])
        grouped_lines.append(group)

    return grouped_lines

sale_layout.grouplines = grouplines_inh


def groupplines(self, ordered_lines, sortkey):
    grouped_lines = []
    for key, valuesiter in groupby(ordered_lines, sortkey):
        group = {}
        group['lines'] = list(v for v in valuesiter)
        group['category'] =key 
        #if 'subtotal' in key and key.subtotal is True:
        group['subtotal'] = sum(line.product_uom_qty for line in group['lines'])
        group['nombre_caisse'] = sum(line.nombre_caisse for line in group['lines'])
        grouped_lines.append(group)

    return grouped_lines

class AccountInvoiceLine(osv.Model):
    _inherit = 'account.invoice.line'
    _order = ' product_categ, id '
    
    product_categ = openerp.fields.Char(related='product_id.categ_id.name',
                                            string='product category',store=True)

class AccountInvoice(osv.Model):
    _inherit = 'account.invoice'

    def sale_layout_lines(self, cr, uid, ids, invoice_id=None, context=None):
        """
        Returns invoice lines from a specified invoice ordered by
        sale_layout_category sequence. Used in sale_layout module.

        :Parameters:
            -'invoice_id' (int): specify the concerned invoice.
        """
        print 'hell'
        ordered_lines = self.browse(cr, uid, invoice_id, context=context).invoice_line
        # We chose to group first by category model and, if not present, by invoice name
        sortkey = lambda x: x.product_id.categ_id if x.product_id.categ_id else ''

        return grouplines_inh(self, ordered_lines, sortkey)

class stock_picking(osv.Model):
    _inherit = 'stock.picking'

    def grouplines(self, ordered_lines, sortkey):
        grouped_lines = []
        for key, valuesiter in groupby(ordered_lines, sortkey):
            group = {}
            group['lines'] = list(v for v in valuesiter)
            group['category'] =key 
            group['poid_brut'] = sum(line.poid_brut for line in group['lines'])
            group['poid_net'] = sum(line.product_qty for line in group['lines'])
            group['nombre_caisse'] = sum(line.nombre_caisse for line in group['lines'])
            grouped_lines.append(group)
    
        return grouped_lines
    
    def sale_layout_lines(self, cr, uid, ids, picking_id=None, context=None):

        ordered_lines = self.browse(cr, uid, picking_id, context=context).move_lines
        # We chose to group first by category model and, if not present, by invoice name
        sortkey = lambda x: x.product_id.categ_id if x.product_id.categ_id else ''

        return self.grouplines(ordered_lines, sortkey)

    def sale_layout_olines(self, cr, uid, ids, picking_id=None, context=None):

        ordered_lines = self.browse(cr, uid, picking_id, context=context).pack_operation_ids
        print "ordered_lines :",ordered_lines
        # We chose to group first by category model and, if not present, by invoice name
        sortkey = lambda x: x.product_id.categ_id if x.product_id.categ_id else ''

        return self.grouplines(ordered_lines, sortkey)

class stock_move(osv.Model):
    _inherit = 'stock.move'
    _order = ' product_categ, date_expected desc, id '
 
    product_categ = openerp.fields.Char(related='product_id.categ_id.name',
                                            string='product category',store=True)
