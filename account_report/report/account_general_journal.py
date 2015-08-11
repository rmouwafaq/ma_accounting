# -*- coding: utf-8 -*-

import time
from openerp.osv import osv
from openerp.addons.account.report.account_central_journal import journal_print
from openerp.osv import fields
from datetime import datetime
from time import gmtime, strftime
from math import ceil
from openerp.addons.account.report.account_general_journal import journal_print



class journal_general_MA(journal_print):

    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        self.lines_journal={}
        super(journal_general_MA, self).__init__(cr, uid, name, context=context)
        self.period_ids = []
        self.journal_ids = []
        self.localcontext.update( {
            'date_jour1':self.date_jour1,
            'grouped_periods':self.grouped_periods,
            'lines_tab':self.lines_tab,
            'journals':self.journals
            
            
        })

    def date_jour1(self):
        my_date = strftime("%Y-%m-%d", gmtime())
        return my_date
    
    def grouped_periods(self,period_id):
        
        lines=self.lines(period_id)

        for line in lines:
            journal_id=line['code']
            b=0
            if self.lines_journal.has_key(journal_id):
                line_journal=self.lines_journal[journal_id]
                if(line['code']==line_journal['code']):
                    line_journal['credit']=line_journal['credit']+line['credit']
                    line_journal['debit']=line_journal['debit']+line['debit']
                    b=1
            if(b==0):
                self.lines_journal[journal_id]=line
        print self.lines_journal
    def journals(self,docs):
        lines=self.lines_journal.values()
        
        nbr_bloc=12
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
#         else:
#             self.lines_journal[journal_id]=lines
#             print self.lines_journal[journal_id] 
             
#   

 
                
            
              
    def lines_tab(self,journal_id):
        lines=self.lines_journal[journal_id]
        print "tab",lines
         
        
        nbr_bloc=12
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
                         
                         
    
    


class report_generaljournal(osv.AbstractModel):
    _name = 'report.account.report_generaljournal'
    _inherit = 'report.abstract_report'
    _template = 'account.report_generaljournal'
    _wrapped_report_class = journal_general_MA

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
