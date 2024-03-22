import pdfplumber
from datetime import datetime
from Database_OperationsV1_NXTRA import insert_into_main_table

def days(date1,date2):
    d1 = datetime.strptime(date1, "%d-%b-%Y")
    d2 = datetime.strptime(date2, "%d-%b-%Y")
    difference = relativedelta.relativedelta(d2, d1)
    return difference.days


def mahavitran_dc_main(path,status):
    print('Processing......')
    with pdfplumber.open(path) as pdf:
        pg1 = pdf.pages[0]
        words1 = pg1.extract_words()
        pg2 = pdf.pages[1]
        words2 = pg2.extract_words()
    lst = []

    for i in range(len(words1)):
        lst.append(words1[i]['text'])
    for i in range(len(words2)):
        lst.append(words2[i]['text'])


    table1 = pg1.extract_tables()[0]
    try:
        a = 0
        for i in lst:
            if 'Bill Month' in ' '.join(lst[a:a+2]):
                bill_month = lst[a+2]
                break
            a+=1

        print('\nBill Month : ',bill_month)
    except Exception as e:
        bill_month ='-'

    try:
        a = 0
        for i in lst:
            if 'Consumer Number' in ' '.join(lst[a:a+2]):
                cons_no = lst[a+2]
                break
            a+=1

        print('\nConsumer Number : ',cons_no)
    except Exception as e:
        cons_no ='-'

    try:
        a = 0
        for i in lst:
            if 'Last Rcpt Dt/No' in ' '.join(lst[a:a+3]):
                bill_no = lst[a+5]
                break
            a+=1

        print('\nBill Number : ',bill_no)
    except Exception as e:
        bill_no ='-'

    try:
        a = 0
        for i in lst:
            if 'Total Contract Demand (KVA)' in ' '.join(lst[a:a+4]):
                contract_dmnd = lst[a+4].split('MSEDCL')[0]
                break
            a+=1

        print('\nContract Demand : ',contract_dmnd)
    except Exception as e:
        contract_dmnd ='-'

    try:
        voltage_level = float(table1[8][-2])
        print('\nVoltage Level - ', voltage_level )
    except Exception as e:
        voltage_level ='-'

    try:
        tot_units_cons = int(table1[21][0].split(' ')[-1])
        print('\nTotal Units Consumed : ',tot_units_cons)
    except Exception as e:
        tot_units_cons ='-'

    try:
        due_date = table1[1][-3]
        print('\nDue Date : ',due_date)
    except Exception as e:
        due_date ='-'

    try:
        due_Date_prompt_benefit = table1[2][-3]
        print('\ndue Date for prompt benfit: ',due_Date_prompt_benefit)
    except Exception as e:
        due_Date_prompt_benefit ='-'

    try:
        late_pymt_penalty= table1[65][-3].replace(',','')
        print('\nLAte Payment Penalty Charges:  ',late_pymt_penalty)
    except Exception as e:
        late_pymt_penalty ='-'

    try:
        prmpt_benefit_charges = float(table1[1][-2].replace(',','')) - float(table1[2][-2].replace(',',''))
        print('\nPrompt Payment Benefit Charges: ',prmpt_benefit_charges)
    except Exception as e:
        prmpt_benefit_charges ='-'

    try:
        demand_chrg = float(table1[20][-3].replace(',',''))
        print('\nDemand charge : ',demand_chrg )
    except Exception as e:
        demand_chrg ='-'

    try:
        Energy_Charge = float(table1[21][-3].replace(',',''))
        print('\nEnergy charge : ',Energy_Charge)
    except Exception as e:
        Energy_Charge ='-'

    try:
        night_rebate = float(table1[22][-3].replace(',','').replace(' ',''))
        print('\nNight Rebate: ',night_rebate)
    except Exception as e:
        night_rebate ='-'

    try:
        wheeling_charge = round(float(table1[34][-3].replace(',','')) + float(table1[54][-3].replace(',','')) , 2)
        print('\nwheeling charge: ',wheeling_charge)
    except Exception as e:
        wheeling_charge ='-'

    try:
        if table1[35][-3] == '':
            transmission_charge1 = 0
        else:
            transmission_charge1 = float(table1[35][-3].replace(',',''))
    except Exception as e:
        transmission_charge ='-'

    try:
        if table1[55][-3] == '':
            transmission_charge2 = 0
        else:
            transmission_charge2 = float(table1[55][-3].replace(',',''))
    except Exception as e:
        transmission_charge2 ='-'

    try:
        transmission_charge = transmission_charge1 + transmission_charge2
        print('\nTransmission charge: ',transmission_charge)
    except Exception as e:
        transmission_charge ='-'
    try:
        incentive_amt = float(table1[49][-3])
        print('\nIncentive Amount : ',incentive_amt)
    except Exception as e:
        incentive_amt ='-'

    try:
        pf_surcharge = float(table1[26][-3].replace(',','').replace(' ',''))
        print('\nPF Surcharge: ',pf_surcharge)
    except Exception as e:
        pf_surcharge ='-'

    try:
        fuel_charge =float(table1[23][-3].replace(',',''))
        print('\nFuel Charge : ',fuel_charge )
    except Exception as e:
        fuel_charge ='-'

    try:
        elec_duty = float(table1[27][-3].replace(',',''))
        print('\nelectricty Duty : ',elec_duty)
    except Exception as e:
        elec_duty ='-'
    try:
        arrear = float(table1[62][-3].replace(',','').replace(' ',''))
        print('\nArrear Carried Over : ',arrear )
    except Exception as e:
        arrear ='-'

    try:
        other_charge =float(table1[56][-3].replace(',',''))
        print('\nOther Charge : ',other_charge )
    except Exception as e:
        other_charge ='-'

    try:
        tax =float(table1[28][-3].replace(',',''))
        print('\nTAX : ',tax )
    except Exception as e:
        tax ='-'

    try:
        tot_amount= float(table1[2][-2].replace(',',''))
        print('\nTotal amount: ',tot_amount)
    except Exception as e:
        tot_amount ='-'

    metering_charge = '-'
    self_gen_tax = '-'
    gst = '-'
    tcs,tds = '-','-'

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
        date = table1[16][0].split('TO')

        start_date = date[0].replace(" ","")
        end_date = date[1].replace(" ","")

        print('\nStart Date: ',start_date)
        print('\nEnd Date : ',end_date)
        no_of_day = days(start_date,end_date)
        print("\nNumber of Days: ",no_of_day)
    except Exception as e:
        start_date,end_date,no_of_day ='-','-','-'

    supplier_name = 'MAHARASHTRA STATE ELECTRICITY DISTRIBUTION Co. LTD.'
    invoice_generation_date = table1[0][-3]

    insert_into_main_table('PUNE_MAHAVITRAN',cons_no,bill_no,tot_units_cons,tot_amount,due_date,due_Date_prompt_benefit,late_pymt_penalty,prmpt_benefit_charges,demand_chrg,Energy_Charge,night_rebate,wheeling_charge,transmission_charge,incentive_amt,pf_surcharge,fuel_charge,elec_duty,arrear,metering_charge,other_charge,self_gen_tax,tcs,tds,tax,gst , path , status,contract_dmnd,no_of_day , bill_name , bill_month , start_date ,end_date, invoice_generation_date , supplier_name)
