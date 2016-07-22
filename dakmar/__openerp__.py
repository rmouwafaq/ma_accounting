# -*- coding: utf-8 -*-
##############################################################################
#
#    Author:  Author Guewen Baconnier
#    Copyright 2012-2014 Camptocamp SA
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

{'name': 'dakmar ',
 'version': '1.0',
 'author': 'AgilORG',
 'maintainer': 'AgilORG',
 'category': 'Warehouse',
 'complexity': "normal",
 'depends': ['base', 'sale', 'sale_layout', 'purchase', 'stock', 'delivery', 'report'],
 'description': """
==========================

module specifique pour DAKMAR
""",
 'website': '',
 'data': ['security/ir.model.access.csv',
          'views/bordereau_view.xml',
          'views/bon_reception_view.xml',
          'views/account_invoice_view.xml',
          'views/report_stockpicking.xml',
          'views/report_invoice.xml',
          'views/report_invoice_provider.xml',
          'views/dakmar_report.xml',
          'views/layouts.xml',
          'views/report_saleorder.xml',
          'views/sale_view.xml',
          'wizard/stock_transfer_details.xml',
          'views/sale_layout_template.xml',

          ],
  'qweb':[],
  
 'installable': True,
 'auto_install': False,
 'license': 'AGPL-3',
}
