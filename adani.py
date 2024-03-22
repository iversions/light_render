import pdfplumber
from datetime import datetime
from Database_OperationsV1_NXTRA import insert_into_main_table

def days(date1,date2):
    d1 = datetime.strptime(date1, "%d.%m.%Y")
    d2 = datetime.strptime(date2, "%d.%m.%Y")
    difference = relativedelta.relativedelta(d2, d1)
    return difference.days
def remove_NONE(table):
  lst = []
  for sub_list in table:
    tmp_lst = [item for item in sub_list if item is not None and item != '\n']
    lst.append(tmp_lst)

  return lst

print('Processing......')

#path = r'D:\NXTRA\New folder\adani\CHANDIVALI DC.PDF'
#path = r'D:\NXTRA\New folder\adani\SANTACRUZ _CLS_DEC-23.PDF'
def adani_main(path,status):
  with pdfplumber.open(path) as pdf:
    pg1 = pdf.pages[0]
    words1 = pg1.extract_words()
    pg2 = pdf.pages[1]
    words2 = pg2.extract_words()   


    table = pdf.pages[1].extract_tables()[0]

    table1 = pg1.extract_tables()[1]

    tmp = pg1.extract_tables()[-1][0]

  lst = [word['text'] for word in words1]
  lst2 = [word['text'] for word in words2]

  try:
    p = 0
    for j in lst:
      if 'Account No.:' == ' '.join(lst[p:p+2]):
          cons_no = lst[p+2]
          break
      p+=1
    print(cons_no)
  except Exception as e:
    cons_no = '-'
  
  try:
    q = 0
    for k in lst:
      if 'Name:'  == ' '.join(lst[q:q+1]):
          bill_name = ' '.join(lst[q+1:q+4])
          break
      q+=1

    print('\nName of EB bill: ',bill_name)
  except Exception as e:
    bill_name ='-'
  

  supplier_name = 'ADANI ELECTRICITY MUMBAI LTD'
  print('\nSupplier Name: ',supplier_name)

  

  try:
    q = 0
    for k in lst:
      if 'Bill No. :'  == ' '.join(lst[q:q+3]):
          bill_no = lst[q+3]
          break
      q+=1

    print('\nBill No : ',bill_no)
  except Exception as e:
    bill_no = '-'
  
  try:
    q = 0
    for k in lst:
      if 'Bill Month :'  == ' '.join(lst[q:q+3]):
          bill_month = lst[q+3]
          break
      q+=1
    print('\nBill month : ',bill_month)
  except Exception as e:
    bill_month ='-'



  date = table[1][0].split(':')[1].split('to')
  start_date = date[0].replace(" ","")
  end_date = date[1].replace(" ","")

  print('\nStart Date: ',start_date)
  print('\nEnd Date : ',end_date)
  no_of_day = days(start_date,end_date)
  print("\nNumber of Days: ",no_of_day)

  
  lst1 = remove_NONE(table1)
  totkvah = float(lst1[1][0].replace(',',''))
  print("\nUnits Consumed: ",totkvah)


  try:
    q = 0
    for k in lst:
      if 'Round sum payable :'  == ' '.join(lst[q:q+4]):
          invoice_amount = float(lst[q+4].replace(',','').replace('-',''))
          break
      q+=1
    print('\nInvoice Amount: ',invoice_amount)
  except Exception as e:
    invoice_amount ='-'
  
  try:
    q = 0
    for k in lst:
      if 'Bill Date:'  == ' '.join(lst[q:q+2]):
          invoice_generation_date = lst[q+2]
          break
      q+=1
    print('\nInvoice Generation Date: ',invoice_generation_date)
  except Exception as e:
    invoice_generation_date ='-'

  
  if float(tmp[2].split(' ')[-1].replace(',','')) == 0: 
    late_payement_charges = 0
  else:
    late_payement_charges = invoice_amount - float(tmp[2].split(' ')[-1].replace(',',''))
  print('\nLate Payment Charges: ',late_payement_charges)

  payment_Amount_with_beneifit = invoice_amount

  payment_Amount_with_late_payment = float(tmp[2].split(' ')[-1].replace(',',''))


  print("\nPayment amount with prompt payment benefit : ",payment_Amount_with_beneifit)

  print("\nPayment amount with late payment penalty charges : ",payment_Amount_with_late_payment)


  print('\n\n\n')
  #Sheet 2

  try:
    t=0
    for l in lst:
      if 'Contract Demand:' == ' '.join(lst[t:t+2]):
          contract_dmnd = float(lst[t+2].replace(',',''))
          break
      t+=1
    print('\nContract Demand: ',contract_dmnd)
  except Exception as e:
    contract_dmnd ='-'

  demand_chrg = float(lst1[4][6].replace(",",""))
  print('\nDemand Charge: ',demand_chrg)

  Energy_charges = float(lst1[7][6].replace(',',''))
  print('\nEnergy Charges: ',Energy_charges)


  wheeling_chrg = float(lst1[15][6].replace(",",""))
  print('\nWheeling Charges: ',wheeling_chrg)

  elec_duty = float(lst1[24][6].replace(",",""))
  print('\nelectricty Duty: ',elec_duty,'\n')

  try:
    toda_unit = float(lst1[8][3].replace(",",""))
    toda_chrg = float(lst1[8][6].replace(",",""))

    if lst1[8][2] == '':
        tod_A = toda_chrg/toda_unit
    if lst1[8][2] != '':
        tod_A = float(lst1[8][2].replace(",",""))
    print(tod_A,toda_unit,toda_chrg)
  except IndexError as e:
    tod_A,toda_unit,toda_chrg = '','','',''  #;print(e)
  except TypeError as e:
    tod_A,toda_unit,toda_chrg = '','','',''  #;print(e)
  except SyntaxError as e:
    tod_A,toda_unit,toda_chrg = '','','',''  #;print(e)
  except ValueError as e:
    tod_A,toda_unit,toda_chrg = '','','',''  #;print(e)
  except UnboundLocalError as e:
    tod_A,toda_unit,toda_chrg = '','','',''  #;print(e)
  except NameError as e:
    tod_A,toda_unit,toda_chrg = '','','',''  #;print(e)
  except Exception as e:
    print(type(e),e)  
    tod_A,toda_unit,toda_chrg = '','','',''

  todb_unit = float(lst1[9][3].replace(",",""))
  todb_chrg = float(lst1[9][6].replace(",",""))

  if lst1[9][2] == '':
      tod_B = todb_chrg/todb_unit
  if lst1[9][2] != '':
      tod_B = float(lst1[9][2].replace(",",""))
  print(tod_B,todb_unit,todb_chrg)

  #----TODC----#
  try:
    todc_unit = float(lst1[10][3].replace(",",""))
    todc_chrg = float(lst1[10][6].replace(",",""))

    if lst1[8][2] == '':
      tod_C = todc_chrg/todc_unit
    if lst1[8][2] != '':
      tod_C = float(lst1[10][2].replace(",",""))
    print(tod_C,todc_unit,todc_chrg)
  except IndexError as e:
    tod_C,todc_unit,todc_chrg = '','','','' #;print(e)
  except TypeError as e:
    tod_C,todc_unit,todc_chrg = '','','','' #;print(e)
  except SyntaxError as e:
    tod_C,todc_unit,todc_chrg = '','','','' #;print(e)
  except ValueError as e:
    tod_C,todc_unit,todc_chrg = '','','','' #;print(e)
  except UnboundLocalError as e:
    tod_C,todc_unit,todc_chrg = '','','','' #;print(e)
  except NameError as e:
    tod_C,todc_unit,todc_chrg = '','','','' #;print(e)
  except Exception as e:
    #print(type(e),e)
    tod_C,todc_unit,todc_chrg = '','','',''

  try:
    todd_unit = float(lst1[11][3].replace(",",""))
    todd_chrg = float(lst1[11][6].replace(",",""))

    if lst1[8][2] == '':
      tod_D = todd_chrg/todd_unit
    if lst1[8][2] != '':
      tod_D = float(lst1[11][2].replace(",",""))
    
    print(tod_D,todd_unit,todd_chrg)
  except IndexError as e:
    tod_D,todd_unit,todd_chrg = '','','','' #;print(e)
  except TypeError as e:
    tod_D,todd_unit,todd_chrg = '','','','' #;print(e)
  except SyntaxError as e:
    tod_D,todd_unit,todd_chrg = '','','','' #;print(e)
  except ValueError as e:
    tod_D,todd_unit,todd_chrg = '','','','' #;print(e)
  except UnboundLocalError as e:
    tod_D,todd_unit,todd_chrg = '','','','' #;print(e)
  except NameError as e:
    tod_D,todd_unit,todd_chrg = '','','','' #;print(e)
  except Exception as e:
    print(type(e),e)
    tod_D,todd_unit,todd_chrg = '','','',''


  night_rebate = toda_chrg+todb_chrg+todc_chrg+todd_chrg

  print('\nNight Rebate: ',night_rebate)
        
                            
  other_charge = float(lst1[28][6].replace(",",""))
  print('\nOther Charges: ',other_charge,'\n')

  tax = float(lst1[25][6].replace(",",""))
  print('\nTAX: ',tax,'\n')

  due_date,due_Date_prompt_benefit ,prmpt_benefit_charges , transmission_charge,incentive_amt,pf_surcharge,fuel_charge , arrear,meter_rent , self_gen_tax,tcs,tds , adjustment_charges = '-','-','-','-','-','-','-','-','-','-','-','-','-'
  insert_into_main_table('ADANI',cons_no,bill_no,totkvah,invoice_amount,due_date,due_Date_prompt_benefit,late_payement_charges,prmpt_benefit_charges,demand_chrg,Energy_charges,night_rebate,wheeling_chrg,transmission_charge,incentive_amt,pf_surcharge,fuel_charge,elec_duty,arrear,meter_rent,other_charge,self_gen_tax,tcs,tds,tax,adjustment_charges , path , status, contract_dmnd,no_of_day , bill_name , bill_month , start_date ,end_date, invoice_generation_date , supplier_name)
