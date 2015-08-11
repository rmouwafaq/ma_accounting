# -*- coding: utf-8 -*-


import time
from openerp.osv import osv
from openerp.addons.account.report.account_journal import journal_print
from openerp.osv import fields
from datetime import datetime
from time import gmtime, strftime
from math import ceil

class journal_printMA(journal_print):
        
        
        def __init__(self, cr, uid, name, context=None):
            self.nbr_pages=1
            self.page_nbr=0
            self.page_nbrx=0
            self.page_nbr1=0
            if context is None:
                context = {}
            super(journal_printMA, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({
                'somme_debit':self.somme_debit,
                'somme_credit':self.somme_credit,
                'lines_tab':self.lines_tab,
                'date_jour':self.date_jour,
                'get_number_page':self.get_number_pages,
                'get_page':self.get_page,
                'check_end_page':self.check_end_page,
                'total_pages':self.total_pages,
                
                })
            
        def check_end_page(self):
            self.page_nbrx=self.page_nbrx+1
#             print "nbr,",self.nbr_pages
            if(self.page_nbrx==self.nbr_pages):
#                 print "compare",self.page_nbrx+1,self.nbr_pages
                self.page_nbrx=0
                self.nbr_pages=0
                return  True
            return False
                
        def get_number_pages(self):
            return self.page_nbr1
        def get_page(self):
            self.page_nbr=self.page_nbr+1
#             self.page_nbrx=self.page_nbrx+1
            return self.page_nbr
            
        def lines_tab(self,period_id,journal_id=False):
            
            lines=self.lines(period_id,journal_id)
            nbr_bloc=15
            nbr_pages=ceil(float(len(lines))/float(nbr_bloc))
            
            self.nbr_pages=int(nbr_pages)
           
            tab_lines=[]
            for p in range(0,self.nbr_pages):
                tab=[]
                limit_tab=(p*nbr_bloc)+nbr_bloc
                if(p==self.nbr_pages-1):
                    limit_tab=len(lines)
                for j in range((p*nbr_bloc),limit_tab):
                    tab.append(lines[j])
                    
                tab_lines.append(tab)
               
            return tab_lines
        
        
        def total_pages(self,period_id,journal_id=False):
            
            lines=self.lines(period_id,journal_id)
            nbr_bloc=15
            nbr_pages=int(ceil(float(len(lines))/float(nbr_bloc)))
            self.page_nbr1 = self.page_nbr1 + nbr_pages
            return self.page_nbr1
            
            
        
        def somme_debit(self,lines_tab):
            somme_debit=0.0
            for line in lines_tab:
                somme_debit= somme_debit + line.debit
                
            return somme_debit
        
        def somme_credit(self,lines_tab):
            somme_credit=0.0
            for line in lines_tab:
                somme_credit= somme_credit + line.credit
            return somme_credit
        
      
        def date_jour(self):
            my_date = strftime("%Y-%m-%d", gmtime())
            return my_date
        
        
            
            
              
  

class report_journal(osv.AbstractModel):
    _name = 'report.account.report_journal'
    _inherit = 'report.abstract_report'
    _template = 'account.report_journal'
    _wrapped_report_class = journal_printMA


class report_salepurchasejournal(osv.AbstractModel):
    _name = 'report.account.report_salepurchasejournal'
    _inherit = 'report.abstract_report'
    _template = 'account.report_salepurchasejournal'
    _wrapped_report_class = journal_printMA

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: