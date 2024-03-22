# from core_function import corefc
# from corefunction import corefc
#from checkdt import checkdate
from pathlib import Path
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from office365.runtime.auth.token_response import TokenResponse
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from office365.runtime.client_request_exception import ClientRequestException
from ast import literal_eval
from string import ascii_lowercase
from itertools import groupby
import configparser

import os
from office365.sharepoint.attachments.creation_information import (
    AttachmentCreationInformation,
)



config_obj = configparser.ConfigParser()
config_obj.read('D:\Bill Extraction Files\config.ini')

sppaths = config_obj['spdl_path']
spparam = config_obj['spdoclib']
sprlpath = config_obj['sp_relative_path']
fol_loc = config_obj['folder_path']

spsite = spparam['rootsite']
spdoclib = spparam['site_url']
splistname = spparam['list_name']
spusername = spparam['uname']
sppassword = spparam['upass']
cid = spparam['cid']
cs = spparam['cs']

sproot = sppaths['root']
spprocessed = sppaths['processed']
spproblematic = sppaths['problematic']
spduplicate = sppaths['duplicate'] ###Add duplicate path

lsppath = fol_loc['spdl']

sprppro = sprlpath['processed']
sprpproblem = sprlpath['problematic']
sprpduplicate = sprlpath['duplicate'] ###Add duplicate path

try:
    ctx = ClientContext(spdoclib).with_credentials(ClientCredential(cid, cs))
    list_title = splistname
    tasks_list = ctx.web.lists.get_by_title(list_title)

except Exception as e:
    if e.response.status_code == 404:
        print(None)
    else:
        print(e.response.text)

def duplicate_bill_check(bill_no):
    paged_items = tasks_list.items.get().execute_query()
    for index, item in enumerate(paged_items): 
        if bill_no == item.properties.get("bill_no"):
            print(item.properties.get('RequestNo'))
            return 1
    return 0


def insert_problematic(path,status):

    try:
        items = tasks_list.items.get().execute_query()
        idlist =[]
        for item in items:  # type:ListItem
            idlist.append(item.properties.get("RequestNo"))
        last_req = idlist[-1]
        last_req = last_req.split('-')
        last_req = literal_eval(last_req[1])
        new_req = f'REQ-{last_req+1}'

    except Exception as te:
        new_req = 'REQ-1'
    
    try:
        task_item =  tasks_list.add_item(
            {
                'RequestNo' : str(new_req),
                'status' : str(status)
            }
        ).execute_query()

        with open(path, "rb") as fh:
            file_content = fh.read()
            attachment_file_info = AttachmentCreationInformation(
                os.path.basename(path), file_content
            )
        attachment = task_item.attachment_files.add(attachment_file_info).execute_query()
        print('Inserted in List')
        print(attachment.server_relative_url)

    except Exception as e:
        if e.response.status_code == 404:
            print(None)
        else:
            print(e.response.text)        


def insert_into_main_table(title,cons_no,bill_no,totkvah,tcmba,due_date,due_Date_prompt_benefit,late_payement_charges,prmpt_benefit_charges,demand_chrg,tot_energy_chrgs,night_rebate,wheeling_charge,transmission_charge,incentive_amt,pf_surcharge,fuel_charge,elec_duty,arrear,meter_rent,other_charge,self_gen_tax,tcs,tds,elec_tax,adjustment_charges , path , status ,  contract_dmnd,no_of_day , bill_name , bill_month , start_date ,end_date, invoice_generation_date , supplier_name): 
    try:
        items = tasks_list.items.get().execute_query()
        idlist =[]
        for item in items:  # type:ListItem
            idlist.append(item.properties.get("RequestNo"))
        last_req = idlist[-1]
        last_req = last_req.split('-')
        last_req = literal_eval(last_req[1])
        new_req = f'REQ-{last_req+1}'

    except Exception as te:
        new_req = 'REQ-1'
    
    try:
        task_item = tasks_list.add_item(
            {
                'RequestNo' : str(new_req),
                'bill_no' : str(bill_no),
                'ConsumerNo' : str(cons_no),
                'Title' : str(title),
                'N_Tot_Unit_consm' : str(totkvah),
                'N_Inv_amt' : str(tcmba),
                'N_Late_Payment_PC' : str(late_payement_charges),
                'N_Due_Date' : str(due_date),
                'N_Due_dt_prom_ben' : str(due_Date_prompt_benefit),
                'N_Prom_pay_BC' : str(prmpt_benefit_charges),
                'N_Demand_FC' :str(demand_chrg),
                'N_Energy_Charges' : str(tot_energy_chrgs),
                'N_Night_rebate' : str(night_rebate),
                'N_Wheeling_Charges' : str(wheeling_charge),
                'N_Transmission_Chrg' : str(transmission_charge),
                'N_Incentive_amount' : str(incentive_amt),
                'N_Pf_Surcharge_Rebate' : str(pf_surcharge),
                'N_Fuel_Charges' : str(fuel_charge),
                'N_Electricity_Duty' : str(elec_duty),
                'N_Arrear_Carried_Over' : str(arrear),
                'N_Metering_Charge' : str(meter_rent),
                'N_Other_Charge' : str(other_charge),
                'N_Self_generation_tax' :str(self_gen_tax),
                'N_TCS' : str(tcs),
                'N_TDS' : str(tds),
                'N_TAX' : str(elec_tax),
                'N_GST' : str(adjustment_charges),
                'N_cntrct_dmd' : str(contract_dmnd),
                #'N_Max_dmd' : str(),
                'N_no_days' : str(no_of_day),
                'N_bill_name' :str(bill_name),
                'N_bill_month' : str(bill_month),
                'N_start_dt' : str(start_date),
                'N_end_dt' : str(end_date),
                'N_invoice_date' : str(invoice_generation_date),
                'N_supplier_name'  :str(supplier_name),
                'status' : str(status)
            }
        ).execute_query()

        print('Inserted in List')
        with open(path, "rb") as fh:
            file_content = fh.read()
            attachment_file_info = AttachmentCreationInformation(
                os.path.basename(path), file_content
            )
        attachment = task_item.attachment_files.add(attachment_file_info).execute_query()
        print(attachment.server_relative_url)

    except Exception as e:
        if e.response.status_code == 404:
            print(None)
        else:
            print(e.response.text) 
      










