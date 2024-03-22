import pdfplumber
from datetime import datetime
from dateutil import relativedelta
from Database_OperationsV1_NXTRA import insert_into_main_table

def days(date1,date2):
    d1 = datetime.strptime(date1, "%d.%m.%Y")
    d2 = datetime.strptime(date2, "%d.%m.%Y")
    difference = relativedelta.relativedelta(d2, d1)
    return difference.days



def avada_main(path,status):
    print('Processing......')

    #path = r'D:\NXTRA\New folder\adani\CHANDIVALI DC.PDF'
    #path = r'D:\NXTRA\New folder\AVADA\Bharti Tower-Non Board.pdf'
    with pdfplumber.open(path) as pdf:
        pg1 = pdf.pages[0]
        words1 = pg1.extract_words()
        pg2 = pdf.pages[1]
        words2 = pg2.extract_words()
        invc4 = [[item.replace(u'\n', ' ') if isinstance(item, str) else item for item in items] for items in pg1.extract_tables()[0]]   
    lst = [word['text'] for word in words1]
    
    try:
        for i in invc4:
            for j in i:
                if j is not None:
                    if 'Buyer Name :' in j:
                        bill_name = j.split('Address')[0].split(':')[1]
        print('\nBill Name: ', bill_name)
    except Exception as e:
        bill_name ='-'

    try:
        a=0
        for i in lst:
            if 'Billing Period :' == ' '.join(lst[a:a+3]):
                start_date = lst[a+3]
                end_date = lst[a+5]
                break
            a+=1

        date_object = datetime.strptime(start_date, '%d.%m.%Y')
        bill_month = f"{date_object.strftime('%b')}-{date_object.year}"
        no_of_day = days(start_date,end_date)


        print("\nStart Date: ",start_date)
        print('\n End Date: ',end_date)
        print('\nNo Of Days: ',no_of_day)
        print('\nBill Month: ',bill_month)
    except Exception as e:
        start_date,end_date,no_of_day,bill_month = '-','-','-','-'

    try:
        a=0
        for i in lst:
            if 'Invoice No./Date :' == ' '.join(lst[a:a+3]):
                bill_no = lst[a+3]
                invoice_generation_date = lst[a+5]
                break
            a+=1
        print('\nInvoice number: ',bill_no)
        print('\nInvoice Date: ',invoice_generation_date)
    except Exception as e:
        bill_no ='-','-'
    
    try:
        totkvah = float(invc4[-6][2].replace(' ','').replace(',',''))
        print('\nUnits Consumed: ',totkvah)
    except Exception as e:
        totkvah ='-'

    try:
        invoice_amount = float(invc4[-3][0].split()[-2].replace(',',''))
        print('\nInvoice Amount: ',invoice_amount)
    except Exception as e:
        invoice_amount ='-'

    try:
        a=0
        for i in lst:
            if 'Payment Due Date :' == ' '.join(lst[a:a+4]):
                due_date = lst[a+4]
                break
            a+=1
        print('\nDue Date: ',due_date)
    except Exception as e:
        due_date ='-'

    try:
        a=0
        for i in lst:
            if 'Customer Code :' == ' '.join(lst[a:a+3]):
                cons_no = lst[a+3]
                break
            a+=1
    except Exception as e:
        cons_no ='-'

    Energy_charges = invoice_amount
    supplier_name = 'AVAADA CLEAN TNPROJECT PRIVATE LIMITED'
    due_Date_prompt_benefit,late_payement_charges,prmpt_benefit_charges,demand_chrg ='-','-','-','-'
    night_rebate,wheeling_chrg,transmission_charge,incentive_amt,pf_surcharge,fuel_charge,elec_duty,arrear,meter_rent,other_charge,self_gen_tax,tcs,tds,tax,adjustment_charges = '-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'
    contract_dmnd = '-'

    insert_into_main_table('AVAADA',cons_no,bill_no,totkvah,invoice_amount,due_date,due_Date_prompt_benefit,late_payement_charges,prmpt_benefit_charges,demand_chrg,Energy_charges,night_rebate,wheeling_chrg,transmission_charge,incentive_amt,pf_surcharge,fuel_charge,elec_duty,arrear,meter_rent,other_charge,self_gen_tax,tcs,tds,tax,adjustment_charges , path , status, contract_dmnd,no_of_day , bill_name , bill_month , start_date ,end_date, invoice_generation_date , supplier_name)
