#-*-coding:utf-8 -*-
import base64 
   
from openerp.osv import fields,osv

class account_migre(osv.osv_memory):
    
    _name='account.migre'
    _description="to migrate"
   
    _columns={
             'file': fields.binary('File', size=128),
             'company_id':fields.many2one('res.company','Company',required=True),
             'file_journal':fields.binary('Journal File', size=128),
             'file_ecriture':fields.binary('ecriture file',size=128),
             'grouped_by_period':fields.boolean('grouper par périod'),
             }
    
    #la methode principale qui permet de migrer(plan comptable,journaux,ecriture)
    def migration_plan_comptable(self,cr,uid,ids,context=None):
        
        obj_account = self.browse(cr,uid,ids[0])
        self.comp_id=obj_account.company_id.id
        
        cp_odoo=self.lire_plan_odoo(cr,uid,ids,context=None)
        if obj_account.file:
            cp_source=self.lire_compte_source(cr,uid,obj_account,context=None)
            self.compare_account(cr,uid,cp_source,cp_odoo,context=None)
            
        if obj_account.file_journal:
            journal_source=self.lire_jornal_source(cr,uid,obj_account,context=None)
            journal_odoo=self.save_journal(cr,uid,journal_source,context=None)
        
        if obj_account.file_ecriture: 
            if obj_account.grouped_by_period:
                ecriture_source =self.lire_ecriture_comptable(cr,uid,obj_account,context=None)
                ecriture_source =self.verification_solde(cr,uid,ecriture_source,context)
                self.save_ecriture(cr,uid,ecriture_source,context=None)
            else:
                
                ecriture_source =self.lire_ecriture_comptable(cr,uid,obj_account,context=None)
                print "ecriture_source=",ecriture_source
                list_ecriture=[]
                b=0
                for move,move_lines in ecriture_source.iteritems():
                    print "entrer",move
                    for line in move_lines:
                        print "line",line
                        debit = line['debit']
                        credit =line['credit']
                        
                        if b == 0:
                            sommedebit=0
                            sommecredit=0
                            b=1
                        sommedebit+=debit
                        sommecredit+=credit
                        list_ecriture.append(line)
                        sommeD=abs(sommedebit)
                        sommeC=abs(sommecredit)
                        if round(sommeD,2)==round(sommeC,2):
                            print"sommmmmme"
                            print "sommedebit",sommedebit,"sommecredit",sommecredit
                            ecriture_data={}
                            ecriture_data[move]=list_ecriture
                            
                            self.save_ecriture(cr,uid,ecriture_data,context=None)
                            list_ecriture=[]
                            b=0
                            
                        
                        
        
          
        
   
    def verification_solde(self,cr,uid,ecriture_source,context=None):
        list_keys=[]
        
        for es_key,es_val in ecriture_source.iteritems():
            debit=0.0
            credit=0.0
           
            for rec in es_val:
                debit=debit+rec['debit']
                credit=credit+rec['credit']
            print "key",es_key,debit,credit
            diff=abs(debit-credit)
            if round(diff,2)>0:
                list_keys.append(es_key)
               
                
        for key in list_keys:
            ecriture_source.pop(key)
            print "suppr",key
            
        
        
              
                 
        return ecriture_source        
                
        
    #la methode qui permet de lire le plan comptable sur odoo        
    def lire_plan_odoo(self,cr,uid,ids,context=None):
        cp_odoo=dict()
        account_obj=self.pool.get('account.account')
        ids=account_obj.search(cr,uid,[('company_id','=',self.comp_id)],offset=0, limit=None, order=None,context=context,count=False)
        records=account_obj.read(cr,uid,ids,['id','code','name','parent_id'],context)
        for res in records:
            resdict={'id':res['id'],
                     'code':res['code'],
                     'name':res['name']}
            cp_odoo[res['code']]=resdict
       
        return cp_odoo        
    
    #la methode qui permet de lire les jornaux sur un fichier csv
    def lire_jornal_source(self,cr,uid,obj_account,context=None):
        journal_source=dict()
        bin_file_data=str(base64.decodestring(obj_account.file_journal))
        bin_file_data_list=bin_file_data.split('\n')
        bin_file_data_list.pop(0)
        bin_file_data_list.pop(len(bin_file_data_list)-1)
        for row in bin_file_data_list:
            row_data=row.split(',')
            name=(row_data[1].replace('"','')).strip()
            code=(row_data[2].replace('"','')).strip()
            code_id=(row_data[0].replace('"','')).strip()
            journal_source[code]=[code_id,name]
        return journal_source
    
    #la methode qui permet de enregistrer les journaux sur odoo
    def save_journal(self,cr,uid,journal_source,context=None):
    
        account_journal=self.pool.get('account.journal')
        ids=account_journal.search(cr,uid,[('company_id','=',self.comp_id)],offset=0, limit=None, order=None,context=context,count=False)
        records=account_journal.read(cr,uid,ids,['code'],context)
        journal_odoo=[]
        for rec in records:
            journal_odoo.append(rec['code'])
        for code in journal_source.keys():
            vals={}
            if code not in journal_odoo:
                vals={'code':code,'code_id':journal_source[code][0],'name':journal_source[code][1],'type':'sale','company_id':self.comp_id}
                account_journal.create(cr,uid,vals,context=context)
        return journal_odoo
    
    def lire_ecriture_comptable(self,cr,uid,obj_account,context=None):
        ecriture_source=dict()
        account_period=self.pool.get('account.period')
        bin_file_data=str(base64.decodestring(obj_account.file_ecriture))
        bin_file_data_list=bin_file_data.split('\n')
        bin_file_data_list.pop(0)
        bin_file_data_list.pop(len(bin_file_data_list)-1)
        account_journal=self.pool.get('account.journal')
        keys_to_compare=[]

        for row in bin_file_data_list:
            row_data=row.split(',')
            move_id=row_data[0].replace('"','')
            
            journal_id=row_data[1].replace('"','')
            aj_ids=account_journal.search(cr,uid,[('code_id','=',journal_id)],offset=0, limit=None, order=None,context=context,count=False)
            journal_id=aj_ids[0]
            date=(row_data[2].replace('"','')).strip()
            period_ids=account_period.search(cr,uid,[('company_id','=',self.comp_id),('date_start','<=',date),('date_stop','>=',date)],offset=0, limit=None, order=None,context=context,count=False)
            
            account=(row_data[3].replace('"','')).strip()
            debit=float((row_data[4].replace('"','')).strip())
            credit=float((row_data[5].replace('"','')).strip())
            type=(row_data[6].replace('"','')).strip()
            name=(row_data[7].replace('"','')).strip()
            piece=(row_data[8].replace('"','')).strip()
            let=(row_data[9].replace('"','')).strip()
            keys=[]
            for period_id in period_ids:
                keys.append((journal_id,period_id))
                
                
                if ecriture_source.has_key((journal_id,period_id)):
                    ecriture_source[(journal_id,period_id)].append({'move_id':move_id,
                                                                    'journal_id':journal_id,
                                                              'period_id':period_id,
                                                              'account':account,
                                                              'date':date,
                                                              'debit':debit,
                                                              'credit':credit,
                                                              'name':name,
                                                              'type':type,
                                                              'piece':piece,
                                                              'let':let
                                                              })
                     
                    
                
                else:
                
                    ecriture_source[(journal_id,period_id)]=[]
                    ecriture_source[(journal_id,period_id)].append({'move_id':move_id,
                                                                    'journal_id':journal_id,
                                                              'period_id':period_id,
                                                              'account':account,
                                                              'date':date,
                                                              'debit':debit,
                                                              'credit':credit,
                                                              'name':name,
                                                              'type':type,
                                                              'piece':piece,
                                                              'let':let
                                                              })
                    
            if(len(period_ids)>1):
                if(keys not in keys_to_compare):
                    keys_to_compare.append(keys)
#  exemple :keys_to_compare=[ [(91,14),(91,15)] , [(71,14),(71,15)] ]    
        print "keys_to_compare==",keys_to_compare
        for keys in keys_to_compare:
            if(len(ecriture_source[keys[0]])==len(ecriture_source[keys[1]])):
                ecriture_source.pop(keys[1])
            else:
                ecriture_source.pop(keys[0])
        return ecriture_source





    def save_ecriture(self,cr,uid,ecriture_source,context=None):
        account_move=self.pool.get('account.move')
        account_move_line = self.pool.get('account.move.line')
        account_account = self.pool.get('account.account')
        for move,move_lines in ecriture_source.iteritems():
            print "move",move
            for line1 in move_lines:
                account_move_id=account_move.create(cr,uid,vals={'journal_id':move[0],
                                                                 'period_id':move[1],
                                                                 'name':line1['piece'],
                                                                 'state':'posted'
                                                                 },context=context)
                 
            #print "move_ids",account_move_id
            for line in move_lines:
                account_id=account_account.search(cr,uid,[('company_id','=',self.comp_id),('code','=',line['account'])],offset=0, limit=None, order=None,context=context,count=False)[0]
                print "account_id",account_id
                vals={'journal_id':int(line['journal_id']),'date':line['date'],
                      'period_id':line['period_id'],'type':line['type'],
                      'account_id':account_id,'debit':line['debit'],'credit':line['credit'],
                      'name':line['name'],'import_move_id':move,'let':line['let'],'company_id':self.comp_id,'move_id':account_move_id,'state':'valid'}
                account_move_line.create(cr,uid,vals,context=context)
                cr.commit()
                
     #la methode qui permet de lire  les compte  sur un fichier csv
    def lire_compte_source(self,cr,uid,obj_account,context=None):
        cp_source={}
        
        bin_file_data=str(base64.decodestring(obj_account.file))
        bin_file_data_list=bin_file_data.split('\n')
        bin_file_data_list.pop(len(bin_file_data_list)-1)
        for row in bin_file_data_list:
            row_data=row.split(',')
            compte = ((row_data[0]).replace('"','')).strip()
            libcompte = ((row_data[1]).replace('"','')).strip()
            cp_source[compte]=libcompte
        code_id=(row_data[0].replace('"','')).strip()
        return   cp_source 
    #la comparaison du compte entre fichier source et odoo 
    def compare_account(self,cr,uid,cp_source,cp_odoo,context=None):
                
        for compte in cp_source.keys():
            libcompte=cp_source[compte]
            if not cp_odoo.has_key(compte):
                for j in xrange(4,1,-1):
                    parent_compte=compte[:j]
                    if  cp_odoo.has_key(parent_compte):
                        value=cp_odoo[parent_compte]
                        id =value['id']
                        type=self.create_type(compte)
                        self.create_compte(cr,uid,val={'code':compte,'name':libcompte,'parent_id':id,'type':type},context=None)
                        break
                    else:
                        print "parent inexistant",compte
                           
            else:    
                print "compte existe",compte      
        
        
    def create_type(self,parent_compte):
        if parent_compte == "3421":
            type='receivable'
        
        elif parent_compte == "441":
            type='payable'
        else:
            type='other'
            
            return type
    
     #la methode qui permet de sauvegarder les compte sur odoo      
    def create_compte(self,cr,uid,val,context=None):
        pool_account=self.pool.get('account.account')
        user = self.pool.get('account.account').browse(cr,uid,uid,context=context).user_type.id
        val.update({'company_id':self.comp_id,'user_type':user})
        compte_id=pool_account.create(cr,uid,val,context=None)
        cr.commit()
        return compte_id
        
    
        
 
            
                 
            
          
    