import time

from openerp.osv import osv
from openerp.osv import fields
from datetime import datetime
from time import gmtime, strftime
from math import ceil
from openerp.addons.account.report.account_balance import account_balance

class account_balance_conforme(account_balance):
    
    def __init__(self, cr, uid, name, context=None):
        self.nbr_pages=1
        self.page_nbr=0
        self.page_nbrx=0
        self.page_nbr1=0
        self.sum_parent_account={}
        if context is None:
                context = {}
        super(account_balance_conforme, self).__init__(cr, uid, name, context=context)
        
        self.sum_debit = 0.00
        self.sum_credit = 0.00
        self.date_lst = []
        self.date_lst_string = ''
        self.result_acc = []
        self.localcontext.update({
                'get_page':self.get_page,    
                'get_number_page':self.get_number_pages, 
                'check_end_page':self.check_end_page, 
                'date_jour':self.date_jour,
                   'get_report_debit' : self.get_report_debit,
                   'get_report_credit': self.get_report_credit,
                   'get_movement_debit':self.get_movement_debit,
                   'get_movement_credit':self.get_movement_credit,
                    'get_cumuls_debit':self.get_cumuls_debit,
                    'get_cumuls_credit':self.get_cumuls_credit,
                    'get_balance':self.get_balance,
                   'account_size':self.get_account_size
                 })
    def check_end_page(self):
            self.page_nbrx=self.page_nbrx+1
             
            if(self.page_nbrx==self.nbr_pages):
               
                self.page_nbrx=0
                self.nbr_pages=0
                return  True
            return False
                
    def get_number_pages(self):
            return self.page_nbr1
        
    def get_page(self):
            self.page_nbr=self.page_nbr+1
            return self.page_nbr
        
#     def total_pages(self,data_form):
#             
#             lines=self.lines(data_form)
#             nbr_bloc=10
#             nbr_pages=int(ceil(float(len(lines))/float(nbr_bloc)))
#             self.page_nbr1 = self.page_nbr1 + nbr_pages
#             return self.page_nbr1
        
    def get_account_size(self,data_form):
        tab_lines=[]
        tab=[]
        nbr_bloc=13
        lines=self.lines(data_form)
        if(len(lines)>0):
            
            if(len(lines)<nbr_bloc):
                nbr_bloc=len(lines)
            
            nbr_pages=ceil(float(len(lines))/float(nbr_bloc))
            self.nbr_pages=int(nbr_pages)
            self.page_nbr1=self.nbr_pages
            for p in range(0,self.nbr_pages):
                    tab=[]
                    limit_tab=(p*nbr_bloc)+nbr_bloc
                    if(p==self.nbr_pages-1):
                        limit_tab=len(lines)
                    
                    for j in range((p*nbr_bloc),limit_tab):
                        line_courant=lines[j]
                        tab.append(line_courant)
                        
                        if(line_courant['type']=="view"):
                            print "+ ",line_courant
                            if( not self.sum_parent_account.has_key(line_courant['id'])):
                                new_line={
                                          'rep_debit':0.0,
                                          'rep_credit':0.0,
                                           'mov_debit':0.0,
                                           'mov_credit':0.0,
                                          'cumuls_debit':0.0,
                                          'cumuls_credit':0.0,
                                          'child_ids':line_courant['child_ids']
                                          }
                                self.sum_parent_account[line_courant['id']]=new_line
                        else:
                            print "      >>",line_courant
                            line_debit=line_courant['debit']
                            line_credit=line_courant['credit']
                            if(self.sum_parent_account.has_key(line_courant['parent_id'][0])):
                                parent_line=self.sum_parent_account[line_courant['parent_id'][0]]
                                parent_line['child_ids'].remove(line_courant['id'])
#                                 parent_line['mov_debit']=parent_line['mov_debit']+line_debit
#                                 parent_line['mov_credit']=parent_line['mov_credit']+line_credit
                                
                    tab_lines.append(tab)
            for id,line in self.sum_parent_account.iteritems():
                self.cr.execute("select sum(aml.debit),sum(aml.credit) from  account_move_line aml ,account_account ac  where aml.account_id=ac.id and aml.journal_id=14 and aml.period_id = %s and ac.parent_id= %s",
                    (data_form['period_from'],id))  
                                 
                sum_report=self.cr.fetchone()
                print "debit",sum_report
                if sum_report[0] != None:
                    line['rep_debit']=line['rep_debit']+sum_report[0]
                    
                if sum_report[1] != None:    
                    line['rep_credit']=line['rep_credit']+sum_report[1]
                self.cr.execute("select sum(aml.debit),sum(aml.credit) from  account_move_line aml ,account_account ac  where aml.account_id=ac.id  and aml.period_id between %s and  %s and aml.journal_id!=14 and ac.parent_id= %s",
                    (data_form['period_from'],data_form['period_to'],id)) 
                sum_mov= self.cr.fetchone() 
                if sum_mov[0] != None:
                    line['mov_debit']=line['mov_debit']+sum_mov[0]  
                if sum_mov[1] != None:
                    line['mov_credit']=line['mov_credit']+sum_mov[1]    
            reverse_parent_ids=list(reversed(sorted(self.sum_parent_account.keys())))
            for id in reverse_parent_ids:
                line=self.sum_parent_account[id]
                for child_id in line['child_ids']:
                    
                    if(self.sum_parent_account.has_key(child_id)):
                        print "id in =",child_id
                        child_line=self.sum_parent_account[child_id]
                        line['rep_debit']=line['rep_debit']+child_line['rep_debit']
                        line['rep_credit']=line['rep_credit']+child_line['rep_credit']
                        line['mov_debit']=line['mov_debit']+child_line['mov_debit']
                        line['mov_credit']=line['mov_credit']+child_line['mov_credit']
                    else:
                        print "id not in =",child_id
        return tab_lines
    def date_jour(self):
        my_date = strftime("%Y-%m-%d", gmtime())
        print my_date
        return my_date     
                    
    def get_report_debit(self, form,account):
            if(account['type'] != 'view'):
                if form['filter'] == 'filter_period':
                    self.cr.execute("select sum(debit) from  account_move_line where period_id = %s and journal_id=14 and account_id=%s",
                            (form['period_from'],account['id']))                       
                    return self.cr.fetchone()[0] or 0.0 
            else:
                if form['filter'] == 'filter_period':
                    parent_line=self.sum_parent_account[account['id']]
                    return parent_line['rep_debit']
            
                     
    def get_report_credit(self,form, account): 
            if(account['type'] != 'view'):
                if form['filter'] == 'filter_period':
                    self.cr.execute("select sum(credit) from  account_move_line  where period_id <= %s and journal_id=14 and  account_id=%s"
                                ,(form['period_from'],account['id'])) 
            
                    return self.cr.fetchone()[0] or 0.0
            else:
                    parent_line=self.sum_parent_account[account['id']]
                    return parent_line['rep_credit']
#             
#            
    def get_movement_debit(self,form,account):
            if(account['type'] != 'view'):
#                 print ">>> ",account
                if form['filter'] == 'filter_period':
                    self.cr.execute("select sum(debit) from account_move_line where  period_id between %s and  %s and journal_id!=14 and account_id=%s",
                                    (form['period_from'],form['period_to'],account['id']))
                
                return self.cr.fetchone()[0] or 0.0
            else:
                
                    parent_line=self.sum_parent_account[account['id']]
                    return parent_line['mov_debit']
                 
    def get_movement_credit(self,form,account):
       
            if(account['type'] != 'view'):
                if form['filter'] == 'filter_period':
                    self.cr.execute("select sum(credit) from account_move_line where  period_id between %s and  %s and journal_id!=14 and account_id=%s",
                                (form['period_from'],form['period_to'],account['id']))
                    return self.cr.fetchone()[0] or 0.0 
            else:
                    parent_line=self.sum_parent_account[account['id']]
                    return parent_line['mov_credit']
                
    def get_cumuls_debit(self,form,account):
        sum_report_debit=self.get_report_debit(form,account)
        sum_mov_debit=self.get_movement_debit(form,account)
        cumuls_debit=sum_report_debit+sum_mov_debit
        return cumuls_debit
     
    def get_cumuls_credit(self,form,account):
        sum_report_credit=self.get_report_credit(form,account)
        sum_mov_credit=self.get_movement_credit(form,account)
        cumuls_credit=sum_report_credit+sum_mov_credit
        return cumuls_credit
     
    
    def get_balance(self,form,account):
        sum_debit=self.get_cumuls_debit(form,account)
        sum_credit=self.get_cumuls_credit(form,account)
        balance=sum_debit-sum_credit
     
        return balance
                                  
class report_trialbalance(osv.AbstractModel):
    _name = 'report.account.report_trialbalance'
    _inherit = 'report.abstract_report'
    _template = 'account.report_trialbalance'
    _wrapped_report_class = account_balance_conforme
    
    