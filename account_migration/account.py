from openerp.osv import fields,osv

class account_journal(osv.osv):
    
    
    _inherit='account.journal'
   
    _columns={ 
    'code_id':fields.char('code_id',size=128),
                }
    
class account_move_line(osv.osv):
    
    _inherit='account.move.line'
    
    _columns={
              
        'import_move_id':fields.char('import_move_id',size=128),
        'type':fields.char('type',size=128),
        'let':fields.char('type',size=128),
           
              }
    
  