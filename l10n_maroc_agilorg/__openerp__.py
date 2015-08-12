# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2015 agilorg  (http://www.agilorg.com/).
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

{
    'name' : 'Maroc - Accounting',
    'version' : '1.0',
    'author' : 'Agilorg',
    'category' : 'Localization/Account Charts',
    'description': """
This is the base module to manage the accounting chart for Maroc.
=================================================================

Ce Module charge le modèle du plan de comptes standard Marocain et permet de
générer les états comptables aux normes marocaines (Bilan, CPC (comptes de
produits et charges), balance générale à 6 colonnes, Grand livre cumulatif...).
""",
    'website': 'http://www.agilorg.com',
    'depends' : ['base', 'account'],
    'data' : [
        'security/ir.model.access.csv',
        'account_type.xml',
        'Agilorg_Pcg_Normal.xml',
        'Agilorg_Pcg_Simplifié.xml',
        'l10n_ma_tax_simple.xml',
        'l10n_ma_wizard.xml',    
        'l10n_ma_tax.xml',
        
        
        
    ],
    'demo' : [],
    'auto_install': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

