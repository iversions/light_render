import pdfplumber
import pandas as pd
from datetime import datetime
from dateutil import relativedelta
from Database_OperationsV1_NXTRA import insert_into_main_table
def date_Format(date_str1):
    try:
        date_obj1 = datetime.strptime(date_str1, '%d-%b-%y')
    except ValueError:
        try:
            date_obj1 = datetime.strptime(date_str1, '%d/%m/%Y')
        except ValueError:
            print('Invalid date format for date_str1')
            exit()

    common_format = '%d-%m-%Y'
    formated_date = date_obj1.strftime(common_format)


    return formated_date


def mahavitran_main(path,status):
    print('Processing......')
    with pdfplumber.open(path) as pdf:
        #pdf = pdfplumber.open(path)
        pg1 = pdf.pages[0]
        words1 = pg1.extract_words()
        pg2 = pdf.pages[1]
        words2 = pg2.extract_words()
        pg3 = pdf.pages[2]
        words3 = pg3.extract_words()
        pg4 = pdf.pages[3]
        words4 = pg4.extract_words()

    z = 1


    lst = []
    tmp = pg4.extract_tables()[0]

    table2 = pg2.extract_tables()[0]



    end_date = table2[2][0].split()[-1].replace(" ",'')
    start_date = table2[3][0].split()[-1].replace(" ",'')

    print('\nStart Date: ',start_date)
    print('\nEnd Date : ',end_date)

    lst2 = []
    for i in range(len(words2)):
        lst2.append(words2[i]['text'])


    for i in range(len(words1)):
        lst.append(words1[i]['text'])
    for i in range(len(words2)):
        lst.append(words2[i]['text'])
    for i in range(len(words3)):
        lst.append(words3[i]['text'])
    for i in range(len(words4)):
        lst.append(words4[i]['text'])


    #Late PAyment Charges


    date_diff = datetime.strptime(table2[2][0].split(' ')[1], '%d/%m/%Y')  - datetime.strptime(table2[3][0].split(' ')[1], '%d/%m/%Y')
    no_of_days = date_diff.days
    print('\nNumber Of Bill Days: ',no_of_days)

    try:
        m=0
        for i in lst:
            if "BILL OF SUPPLY FOR THE MONTH OF" == ' '.join(lst[m:m+7]):
                bill_month = lst[m+7]
                bill_no = lst[m+8]  
                break
            m+=1
        print(bill_month)
        print(bill_no)
    except Exception as e:
        bill_month , bill_no ='-'

    try:
        a = 0
        for i in lst:
            if 'Consumer Name' in ' '.join(lst[a:a+2]):
                bill_name = ' '.join(lst[a+2:a+5])
                break
            a+=1
        print('\nBill Name : ',bill_name)
    except Exception as e:
        bill_name ='-'

    try:
        p = 0
        for j in lst:
            if "Consumer No. :" == ' '.join(lst[p:p+3]):
                cons_no = lst[p+3]
                break
            p+=1
        print(cons_no)
    except Exception as e:
        cons_no ='-'


    amounts = pg1.extract_tables()[1]

    try:
        invoice_payment_amount = float(amounts[0][-1].replace(',',''))
        print('\n\n\nInvoice Payment Amount : ' ,invoice_payment_amount)
    except Exception as e:
        invoice_payment_amount ='-'

    try:
        paid_after = float(amounts[3][-1].replace(',',''))
        late_payement_charges = paid_after - invoice_payment_amount
        print('\nLate Payment Charges : ',late_payement_charges)
    except Exception as e:
        late_payement_charges ='-'

    try:
        v = 0
        for n in lst:
            if "Total Consumption"  == ' '.join(lst[v:v+2]):
                totkvah = lst[v+3]
                break
            v+=1
        print('\nTotal Units Consumed : ',totkvah)
    except Exception as e:
        totkvah ='-'

    try:
        due_date = date_Format(amounts[1][1].split()[-1])
        print('\nDue date for payment : ',due_date)
    except Exception as e:
        due_date ='-'

    try:
        due_date_for_benifit = date_Format(amounts[2][1].split()[-1])
        print('\nDue date for availing prompt payment benefit : ',due_date_for_benifit)
    except Exception as e:
        due_date_for_benifit ='-'

    try:
        y=0
        for i in lst:
            if 'Demand Charges' == ' '.join(lst[y:y+2]):
                demand_chrg = float(lst[y+2].replace(',',''))
                break
            y+=1

        print('\nDemand charge : ',demand_chrg )
    except Exception as E:
        demand_chrg ='-'

    try:
        k=0
        for i in lst:
            if 'Energy Charges' == ' '.join(lst[k:k+2]):
                Energy_charges = float(lst[k+2].replace(",",''))
                break
            k+=1

        print('\nEnergy charge : ',Energy_charges)
    except Exception as e:
        Energy_charges ='-'

    try:
        v = 0
        for n in lst:
            if "Wheeling Charge @"  == ' '.join(lst[v:v+3]):
                wheeling_chrg = float(lst[v+4].replace(',',''))
                break
            v+=1
        print('\nwheeling charge: ',wheeling_chrg )
    except Exception as e:
        wheeling_chrg ='-'

    try:
        x = 0
        for n in lst:
            if "FAC @"  == ' '.join(lst[x:x+2]):
                fac_charges = float(lst[x+4].replace(',',''))
                break
            x+=1

        print('\nFuel Charge : ',fac_charges )
    except Exception as e:
        fac_charges ='-'

    try:
        p=0
        for i in lst2:
            if 'Electricity Duty' == ' '.join(lst2[p:p+2]):
                elec_duty = float(lst2[p+2].replace(',',''))
                break
            p+=1
        print('\nelectricty Duty : ',elec_duty )
    except Exception as e:
        elec_duty ='-'

    try:
        g=0
        for n in lst:
            if "Tax Collection at Source"  == ' '.join(lst[g:g+4]):
                tcs = lst[g+4]
                break
            g+=1

        print('\nTCS : ',tcs)
    except Exception as e:
        tcs ='-'

    try:
        p=0
        for i in lst:
            if 'Tax on Sale @' == ' '.join(lst[p:p+4]):
                tose_chrg = float(lst[p+6].replace(',',''))
                break
            p+=1

        print('\nTAX : ',tose_chrg)
    except Exception as e:
        tose_chrg ='-'


    try:
        tds = float(tmp[4][2].replace(',',''))
        print('\nTDS : ',tds)
    except Exception as e:
        tds ='-'


    try:
        a= 0 
        for i in lst:
            if 'Delay Payment Charges Rs.' == ' '.join(lst[a:a+4]):
                delay_payment_chrg = lst[a+4]
                break
            a+=1
        print('\nDelay Payment Charges Rs. ', delay_payment_chrg)
    except Exception as e:
        delay_payment_chrg='-'

    try:
        g=0
        for n in lst:
            if "Total Bill Amount (Rounded) Rs."  == ' '.join(lst[g:g+5]):
                tbar = float(lst[g+5].replace(',',''))
                break
            g+=1

        print('\nTotal amount: ',tbar )
    except Exception as e:
        tbar ='-'

    try:
        g=0
        for n in lst:
            if "TOD Tariff EC"  == ' '.join(lst[g:g+3]):
                if lst[g+3] == '-':
                    tod_charges = -float(lst[g+4].replace(',',''))
                else:
                    tod_charges = float(lst[g+3].replace(',',''))
                break
            g+=1

        print('\nNight Rebate: ',tod_charges)
    except Exception as e:
        tod_charges ='-'

    try:
        p=0
        for i in lst:
            if 'Bulk Consumption Rebate' == ' '.join(lst[p:p+3]):
                pf_surchrg_rbt =  float(''.join(lst[p+3:(p+5)]).replace(',',''))
                break
            p+=1

        print('\nPF Surcharge: ',pf_surchrg_rbt)
    except Exception as e:
        pf_surchrg_rbt ='-'

    try:
        g=0
        for n in lst:
            if "Incremental Consumption Rebate"  == ' '.join(lst[g:g+3]):
                if lst[g+3] == '$$':
                    if lst[g+4] == '-':
                        incentive_amt = -(float(lst[g+5].replace(',','')))
                    else:
                        incentive_amt = float(lst[g+4].replace(',',''))
                else:
                    if lst[g+3] == '-':
                        incentive_amt = -(float(lst[g+4].replace(',','')))
                    else:
                        incentive_amt = float(lst[g+3].replace(',',''))
                break
            g+=1

        print('\nincentive amount : ',incentive_amt)
    except Exception as e:
        incentive_amt ='-'

    try:
        prompt_charge = tmp[2][2]
        print('\nPrompt payment benefit charges : ',prompt_charge,'\n\n')
    except Exception as e:
        prompt_charge ='-'


    arrear,metering_charge,other_charge,self_gen_tax = '-','-','-','-'
    transmission_charge = '-'
    gst = '-'
    contract_dmnd ='-'
    invoice_generation_date ='-'
    supplier_name ='-'
    insert_into_main_table('MAHAVITRAN',cons_no,bill_no,totkvah,invoice_payment_amount,due_date,due_date_for_benifit,late_payement_charges,prompt_charge,demand_chrg,Energy_charges,tod_charges,wheeling_chrg,transmission_charge,incentive_amt,pf_surchrg_rbt,fac_charges,elec_duty,arrear,metering_charge,other_charge,self_gen_tax,tcs,tds,tose_chrg,gst , path , status, contract_dmnd,no_of_days , bill_name , bill_month , start_date ,end_date, invoice_generation_date , supplier_name)