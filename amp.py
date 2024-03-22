import pdfplumber
import pandas as pd
from Database_OperationsV1_NXTRA import insert_into_main_table

def amp_main(path,status):
    with pdfplumber.open(path) as pdf:
        pg1 = pdf.pages[0]
        words1 = pg1.extract_words()
        pg2 = pdf.pages[1]
        words2 = pg2.extract_words()   

    table = pdf.pages[0].extract_tables()[0]

    lst = [word['text'] for word in words1]
    lst2 = [word['text'] for word in words2]

    p = 0
    try:
        for j in lst:
            if 'M/s' == lst[p]:
                bill_name = ' '.join(lst[p+1:p+4])
                break
            p+=1
        print('\nName of EB bill: ',bill_name)
    except Exception as e:
        bill_name = '-'
    

    try:
        bill_no = table[3][-1]
        print('\nBill No : ',bill_no)
    except Exception as e:
        bill_no = '-'
    

    try:
        totkvah = float(table[14][0].replace(',',''))
        print('\nTotal Units Consumed: ',totkvah)
    except Exception as e:
        totkvah = '-'
    

    try:
        invoice_amount = float(table[19][-1].replace(',',''))
        print('\nInvoice Payment Amount : ',invoice_amount)
    except Exception as e:
        invoice_amount = '-'
    

    try:
        invoice_generation_date = table[10][-2]
        print('\nInvoice Generation Date: ',invoice_generation_date)
    except Exception as e:
        invoice_generation_date = '-'
    

    try:
        due_date = table[11][-2]
        print('\nDue Date: ',due_date)
    except Exception as e:
        due_date = '-'
    

    try:
        Energy_charges = float(table[14][-1].replace(',',''))
        print('\nEnergy Charges: ',Energy_charges)
    except Exception as e:
        Energy_charges = '-'
    

    try:
        arrear = float(table[17][-1].replace(',',''))
        print('\nArrear: ',arrear)
    except Exception as e:
        arrear = '-'

    supplier_name = 'AMPSOLAR EVOLUTION PRIVATE LIMITED'
    cons_no = '-'
    due_Date_prompt_benefit,late_payement_charges,prmpt_benefit_charges,demand_chrg,night_rebate,wheeling_chrg,transmission_charge,incentive_amt,pf_surcharge,fuel_charge,elec_duty,meter_rent,other_charge,self_gen_tax,tcs,tds,tax,adjustment_charges ,contract_dmnd,no_of_day , bill_month , start_date ,end_date = '-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'

    insert_into_main_table('AMP',cons_no,bill_no,totkvah,invoice_amount,due_date,due_Date_prompt_benefit,late_payement_charges,prmpt_benefit_charges,demand_chrg,Energy_charges,night_rebate,wheeling_chrg,transmission_charge,incentive_amt,pf_surcharge,fuel_charge,elec_duty,arrear,meter_rent,other_charge,self_gen_tax,tcs,tds,tax,adjustment_charges , path , status, contract_dmnd,no_of_day , bill_name , bill_month , start_date ,end_date, invoice_generation_date , supplier_name)
