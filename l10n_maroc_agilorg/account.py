from openerp.osv import fields,osv

class account_chart_template(osv.osv):
    
    
    _inherit='account.chart.template'
   
    _defaults = {
        
        'code_digits':8,
        
    }