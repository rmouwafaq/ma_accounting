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

{'name': 'samarkand',
 'version': '1.2',
 'author': 'AgilORG',
 'maintainer': 'AgilORG',
 'category': 'Purchase',
 'complexity': "normal",  # easy, normal, expert
 'depends': ['base','purchase','account',
             'product','point_of_sale'
             ],
 'description': """
Description
==========================

Allow Multiple EAN13 on products.
A list of EAN13 is available for each product with a priority, so a
main ean13 code is defined.
""",
 'website': 'http://www.agilorg.com',
 'data': [
          'views/purchase_order_view.xml',
          'views/stock_view.xml',
          'reports/report_purchasequotation.xml',
          'reports/report_relevefactures.xml',
          'samarkand_report.xml',
          'wizard/releve_factures_view.xml',
          ],
 'qweb':[],

 'installable': True,
 'auto_install': False,
 'license': 'AGPL-3',
}