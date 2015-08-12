# -*- coding: utf-8 -*-

import time
from openerp.osv import osv
from openerp.addons.account.report.account_central_journal import journal_print
from openerp.osv import fields
from datetime import datetime
from time import gmtime, strftime
from math import ceil


class journal_central_MA(journal_print):

    def __init__(self, cr, uid, name, context=None):
        self.page_nbr1=0
        self.nbr_pages=1
        self.page_nbr=0
        self.page_nbrx=0
        

        if context is None:
            context = {}
        self.b=0
        self.sum_debit_journal=0.0
        self.sum_credit_journal=0.0
        self.lines_journal={}
        self.list_lines=[]
        super(journal_central_MA, self).__init__(cr, uid, name, context=context)
        self.period_ids = []
        self.journals_ids = []
        self.localcontext.update({
            'date_jour1':self.date_jour1,
            'lines_tab':self.lines_tab,
            'grouped_periods':self.grouped_periods,
            #'get_list':self.get_list,
            'get_number_pages':self.get_number_pages,
            'check_exist_journal':self.check_exist_journal,
            'total_pages':self.total_pages,
            'get_page':self.get_page,
            'somme_debit_page':self.somme_debit_page,
            'somme_credit_page':self.somme_credit_page,
            'check_end_page':self.check_end_page,
            'somme_debit_journal':self.somme_debit_journal,
            'somme_credit_journal':self.somme_credit_journal
            
                                })
    #la methode qui permet de afficher la somme total apres la fin de chaque periode  
    def check_end_page(self):
        self.page_nbrx=self.page_nbrx+1
        if(self.page_nbrx==self.nbr_pages):
            self.page_nbrx=0
            self.nbr_pages=0
            return  True
        return False
    #la methode qui permet de afficher la date d'aujourd'hui
    def date_jour1(self):
        my_date = strftime("%Y-%m-%d", gmtime())
        return my_date
   
#     def get_list(self):
#         if(self.b==0):
#             self.b=1
#      
        
    def check_exist_journal(self,journal_id):
        if(journal_id in self.journals_ids):
            
            
            return False
        else:
            self.journals_ids.append(journal_id)
            
            
            return True
    # la methode qui permet de grouper tt les compte par journal  et period    
    def grouped_periods(self,period_id,journal_id):
        lines=self.lines(period_id,journal_id)
        
        if(self.lines_journal.has_key(journal_id)):
            for line in lines:
                b=0
                for line_journal in self.lines_journal[journal_id]:
                    if(line['code']==line_journal['code']):
                        line_journal['credit']=line_journal['credit']+line['credit']
                        line_journal['debit']=line_journal['debit']+line['debit']
                        b=1
                        break
                if(b==0):    
                    self.lines_journal[journal_id].append(line)
                    print self.lines_journal
        else:
            self.lines_journal[journal_id]=lines
        
    
        
           
    #la methode qui permet de lire nombre fixe pour chaque page 
    def lines_tab(self,journal_id):
        lines=self.lines_journal[journal_id]
         
        
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
        
        
         
    #la methode qui permet de calcule la somme debit  total pour chaque page
    def somme_debit_page(self,lines_page):
        somme_debit=0.0
        for line_journal in lines_page:
            
            somme_debit=somme_debit+line_journal['debit']
            
        self.sum_debit_journal=self.sum_debit_journal+somme_debit
            
        return somme_debit
    #la methode qui permet de calcule la somme debit   total pour chaque journal    
    def somme_debit_journal(self):
        sum_dedit= self.sum_debit_journal
        self.sum_debit_journal=0.0
        return sum_dedit
    #la methode qui permet de calcule la somme credit total pour chaque page     
    def somme_credit_page(self,lines_page):
        somme_credit=0.0
        for line_journal in lines_page:
            
            somme_credit=somme_credit+line_journal['credit']
        self.sum_credit_journal=self.sum_credit_journal+somme_credit    
        
        return somme_credit
    
    
    #la methode qui permet de calcule la somme credit total pour chaque journal    
    def somme_credit_journal(self):
        sum_credit= self.sum_credit_journal
        self.sum_credit_journal=0.0
        return sum_credit     


    #la methode qui permet de numerotation total      
    def total_pages(self):
        total_records=0
        nbr_bloc=12
        nbr_pages=0
        for journal,lines in self.lines_journal.iteritems():
            total_records=len(lines)
            nbr_pages=nbr_pages+int(ceil(float(total_records/float(nbr_bloc))))
        
        
        return nbr_pages
            
          
    def get_number_pages(self):
        return self.page_nbr1 
    #incrementation des pages 1,2,3 
    def get_page(self):
        self.page_nbr=self.page_nbr+1
#             self.page_nbrx=self.page_nbrx+1
        return self.page_nbr    


    


class report_agedpartnerbalance(osv.AbstractModel):
    _name = 'report.account.report_centraljournal'
    _inherit = 'report.abstract_report'
    _template = 'account.report_centraljournal'
    _wrapped_report_class = journal_central_MA

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
