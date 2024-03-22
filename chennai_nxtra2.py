import pdfplumber
from Database_OperationsV1_NXTRA import insert_into_main_table

def chennai_main(path,status):
    print('Processing......')

    #path = r"D:\NXTRA\New folder\Chennai\Bharti Tower  EB bill - Dec'2023.pdf"
    with pdfplumber.open(path) as pdf:
        pg1 = pdf.pages[0]
        pg2 = pdf.pages[1]
        pg3 = pdf.pages[2]
        pg4 = pdf.pages[3]

        tmp = pg1.extract_tables()[0]
        words1 = pg1.extract_words()

        tmp2 = pg2.extract_tables()[1]


        words = pg3.extract_words()


        words = pg3.extract_words()
        lst2 = []
        for i in range(len(words)):
            lst2.append(words[i]['text']) 

        
        words = pg4.extract_words()
        lst3 = []
        for i in range(len(words)):
            lst3.append(words[i]['text'])
            


        tmp1 = pg3.extract_tables()[0]
    lst = []
    for i in range(len(words1)):
        lst.append(words1[i]['text'])



    #bill month
    try:
        a=0
        for i in lst:
            if 'for the Month of' == ' '.join(lst[a:a+4]):
                bill_month = ' '.join(lst[a+4:(a+4)+2])
                break
            a+=1
        print(bill_month)
    except Exception as invind:
        bill_month = ''

    try:
        a=0
        for i in lst:
            if 'Service No.' == ' '.join(lst[a:a+2]):
                cons_no = lst[a+2]
                break
            a+=1
        print(cons_no)
    except Exception as E:
        cons_no ='-'

    try:
        a=0
        for i in lst:
            if 'Bill No.' == ' '.join(lst[a:a+2]):
                bill_no = lst[a+2]
                break
            a+=1
        print(bill_no)
    except Exception as invind:
        bill_no ='-'
    #--------------------------------DEMAND CALCULATION PAGE 3-------------------------------------#

    
    
    try:
        a=0
        for i in lst3:
            if 'Net Industrial Consumption' == ' '.join(lst3[a:a+3]):
                totkvah = lst3[a+3]
                break
            a+=1
        print('\nTotal Units Consumed : ',totkvah )
    except Exception as e:
        totkvah ='-'

    try:
        a=0
        for i in lst:
            if 'Due Date' == ' '.join(lst[a:a+2]):
                due_date =lst[a+2]
                break
            a+=1
        print("\nDue Date: ",due_date)
    except Exception as E:
        due_date ='-'
    
    try:
        a=0
        for i in lst:
            if 'Meter Rent(Including 9 %SGST&9 %CGST)' == ' '.join(lst[a:a+5]):
                txble_amt = float(lst[a+5].replace(',',''))
                break
            a+=1

        print("\nTaxable Amount: ",txble_amt)
    except Exception as e:
        txble_amt ='-'

    try:
        a=0
        for i in lst:
            if 'Total Energy Charges' == ' '.join(lst[a:a+3]):
                tot_energy_chrgs = float(lst[a+3].replace(",",""))
                break
            a+=1
        print('\nEnergy charge : ',tot_energy_chrgs)
    except Exception as e:
        tot_energy_chrgs ='-'

    try:
        a=0
        for i in lst:
            if 'Demand Charges' == ' '.join(lst[a:a+2]):
                demand_chrg_rt = float(lst[a+2])
                demand_chrg = float(lst[a+6].replace(",",""))
                break
            a+=1
        print('\nDemand charge : ',demand_chrg,demand_chrg_rt)
    except Exception as e:
        demand_chrg_rt ='-'
        demand_chrg ='-'

    try:
        a=0
        for i in lst:
            if 'Total Demand and Energy Charges' == ' '.join(lst[a:a+5]):
                tot_dmnd_energy_chrg = float(lst[a+5].replace(",",""))
                break
            a+=1
        print("\n\nTotal Demand and Energy Charges : ",tot_dmnd_energy_chrg )
    except Exception as E:
        tot_dmnd_energy_chrg
    
    try:
        a=0
        for i in lst:
            if 'Meter Rent(Including 9 %SGST&9 %CGST)' == ' '.join(lst[a:a+5]):
                meter_rent = float(lst[a+5].replace(",",""))
                break
            a+=1
        print("\n\nMeter Rent : ",meter_rent)
    except Exception as e:
        meter_rent ='-'

    try:
        a=0
        for i in lst:
            if 'Self Generation Tax' == ' '.join(lst[a:a+3]):
                self_gen_tax = float(lst[a+3].replace(",",""))
                break
            a+=1
        print("\n\nSelf Generation Tax : ",self_gen_tax)
    except Exception as e:
        self_gen_tax ='-'
    
    try:
        a=0
        for i in lst:
            if 'Electricity Tax' == ' '.join(lst[a:a+2]):
                elec_tax = float(lst[a+2].replace(",",""))
                break
            a+=1
        print('\nTAX : ',elec_tax)
    except Exception as e:
        elec_tax ='-'
    
    try:
            
        a=0
        for i in lst:
            if "Adjustment Charges(Not Affecting) (Incl. 18% GST)" == ' '.join(lst[a:a+6]):
                if '(' in lst[a+6]:
                    adjustment_charges = -float(lst[a+6].split("(")[0].replace(",",""))
                if '+' in lst[a+6]:
                    adjustment_charges = float(lst[a+7].replace(",",""))
                else:
                    adjustment_charges = float(lst[a+6].replace(",",""))
                break
            a+=1
        print('\nGST : ',adjustment_charges)
    except Exception as e:
        adjustment_charges ='-'
    
    try:
        a=0
        for i in lst:
            if 'Tax collected at source' == ' '.join(lst[a:a+4]):
                tcs = float(lst[a+4].replace(",",""))
                break
            a+=1
        print('\nTCS : ',tcs )
    except Exception as e:
        tcs ='-'
    
    try:
        a=0
        for i in lst:
            if 'Net Amount Payable' == ' '.join(lst[a:a+3]):
                tcmba = float(lst[a+3].replace(",",""))
                break
            a+=1
        print('\nTotal amount: ',tcmba )
    except Exception as e:
        tcmba = '-'

    try:
        a=0
        for i in lst:
            if 'Amount Payable after due date & upto' == ' '.join(lst[a:a+7]):
                late_payement_charges = float(lst[a+8].replace(",",""))-tcmba
                break
            a+=1
        print('\n\nLate PAyment Charges : ',late_payement_charges)
    except Exception as e:
        late_payement_charges ='-'
    

    

    try:
        bill_name = tmp[0][1]
        print('\n\nBill Name: ',bill_name)
    except Exception as e:
        bill_name ='-'

        
    try:
        no_of_day = tmp1[2][4]
        print("NO of Days: ",no_of_day)
    except Exception as e:
        no_of_day = '-'
    
    try:
        contract_dmnd = tmp1[2][1]
        print('\n\n Contract Demand: ',contract_dmnd)
    except Exception as e:
        contract_dmnd ='-'
    
    try:
        invoice_generation_date = tmp[2][-2]
        print('\nInvoice generation date: ',invoice_generation_date)
    except Exception as e:
        invoice_generation_date = '-'
    
    
    try:
        start_date = tmp2[0][1]
        print('\n\n\n Start date: ',start_date)
    except Exception as e:
        start_date ='-'

    end_date = '-'
    supplier_name = "TamilNadu Generation and Distribution Corporation Ltd."
    due_Date_prompt_benefit ='-'
    prmpt_benefit_charges = '-'
    night_rebate,wheeling_charge,transmission_charge,incentive_amt,pf_surcharge,fuel_charge,elec_duty,arrear = '-','-','-','-','-','-','-','-'
    other_charge,tds = '-','-'


    insert_into_main_table('CHENNAI',cons_no,bill_no,totkvah,tcmba,due_date,due_Date_prompt_benefit,late_payement_charges,prmpt_benefit_charges,demand_chrg,tot_energy_chrgs,night_rebate,wheeling_charge,transmission_charge,incentive_amt,pf_surcharge,fuel_charge,elec_duty,arrear,meter_rent,other_charge,self_gen_tax,tcs,tds,elec_tax,adjustment_charges, path , status ,contract_dmnd,no_of_day , bill_name , bill_month , start_date ,end_date, invoice_generation_date , supplier_name)
