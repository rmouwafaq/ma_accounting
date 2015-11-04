import time
from openerp.osv import osv
from datetime import datetime
from time import gmtime, strftime
from math import ceil
from openerp.addons.account.report.account_general_ledger import general_ledger

 
 
class grand_livre(general_ledger):
    
    def __init__(self, cr, uid, name, context=None):
        self.nbr_pages=1
        self.page_nbr=0
        self.report_balance=0.0
        self.page_nbrx=0
        self.page_nbr1=136
        if context is None:
            context = {}
        super(grand_livre, self).__init__(cr, uid, name, context=context)
        
        self.report_debit=0.0
        self.report_credit=0.0
        self.query = ""
        self.tot_currency = 0.0
        self.period_sql = ""
        self.sold_accounts = {}
        self.sortby = 'sort_date'
        self.localcontext.update({
                'get_number_page':self.get_number_pages,
                'get_page':self.get_page,
                'check_end_page':self.check_end_page,
                'total_pages':self.total_pages,
                'date_jour':self.date_jour,
                'solde_progressive':self.solde_prog,
                'account_size':self.get_account_size,
                'reportd':self.report_d,
                'reportc':self.report_c,
                'reset_data_report':self.reset_data_report,
                'get_report_debit':self.get_report_debit,
                'get_report_credit':self.get_report_credit,
                'get_report_balance':self.get_report_credit,
#                 'balance':self.get_balance
                
            
                
                })
    
    def check_end_page(self):
            self.page_nbrx=self.page_nbrx+1
            if(self.page_nbrx==self.nbr_pages):
                self.page_nbrx=0
                self.nbr_pages=0
                return  True
            return False
                
    def get_number_pages(self):
            print self.page_nbr1
            return self.page_nbr1
    def get_page(self):
            self.page_nbr=self.page_nbr+1
            self.page_nbrx=self.page_nbrx+1
            return self.page_nbr
        
    def total_pages(self,account):
        tab_lines=[]
        tab=[]
        nbr_bloc=15
        lines=self.lines(account)
        if(len(lines)<nbr_bloc):
            nbr_bloc=len(lines)
            nbr_pages=ceil(float(len(lines))/float(nbr_bloc))
            self.nbr_pages=int(nbr_pages)
            self.page_nbr1 = self.page_nbr1 + self.nbr_pages
            return self.page_nbr1
        
    def get_account_size(self,account):
        tab_lines=[]
        tab=[]
        nbr_bloc=15
        lines=self.lines(account)
        if(len(lines)<nbr_bloc):
            nbr_bloc=len(lines)
        nbr_pages=ceil(float(len(lines))/float(nbr_bloc))
        self.nbr_pages=int(nbr_pages)
        print "nbr1",self.nbr_pages
        #self.page_nbr1=self.nbr_pages
        #print "nbr3",self.page_nbr1
        for p in range(0,self.nbr_pages):
                tab=[]
                limit_tab=(p*nbr_bloc)+nbr_bloc
                if(p==self.nbr_pages-1):
                    limit_tab=len(lines)
                
                for j in range((p*nbr_bloc),limit_tab):
                    tab.append(lines[j])
                
                tab_lines.append(tab)
        print "nbr2",len(tab_lines)
        return tab_lines
    
    def reset_data_report(self):
        self.report_debit=0.0
        self.report_credit=0.0
        self.report_balance=0.0
        
    def get_report_debit(self):
        if(self.report_debit>0.0):
            return self.report_debit
        else:
            return 0.0
        
    def get_report_credit(self):
        if(self.report_credit>0.0):
            return self.report_credit
        else:
            return 0.0
        
    def get_report_balance(self):
        if(self.report_balance>0.0):
            return self.report_balance
        else:
            return 0.0
    
    def report_d(self,get_account_size):
        sum_debit=0.0
        report=self.get_report_debit()
        for account in get_account_size:
            sum_debit=sum_debit+account['debit']
        self.report_debit=sum_debit
        sum_debit=report+sum_debit
        return sum_debit
    


    def report_c(self,get_account_size):
        sum_credit=0.0
        report=self.get_report_credit()
        for tab in get_account_size:
            sum_credit=sum_credit+tab['credit']
        self.report_credit=sum_credit
        sum_credit=report+sum_credit
        return sum_credit
             
        
    def get_balance(self,get_account_size): 
        solde=0.0
        report=self.get_report_balance()
        for acc in get_account_size:
            solde=solde+(acc['debit']-acc['credit'])
        self.report_balance=solde
        solde=report+solde
        return solde    
   
    def solde_prog(self,debit,credit):
       
        balance= debit - credit
        return balance
                   
    
    def date_jour(self):
        my_date = strftime("%Y-%m-%d", gmtime())
        print my_date
        return my_date
    
        
    

class report_generalledger(osv.AbstractModel):
    _name = 'report.account.report_generalledger'
    _inherit = 'report.abstract_report'
    _template = 'account.report_generalledger'
    _wrapped_report_class = grand_livre