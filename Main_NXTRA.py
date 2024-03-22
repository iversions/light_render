import os
import glob
import pdfplumber
from pathlib import Path
import configparser
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from office365.runtime.client_request_exception import ClientRequestException
from ast import literal_eval
from string import ascii_lowercase
from itertools import groupby
import pandas as pd
import pdfplumber
import Database_OperationsV1_NXTRA
import pdfplumber
from office365.sharepoint.files.move_operations import MoveOperations
from adani import adani_main
from amp import amp_main
from avada import avada_main
from chennai_nxtra2 import chennai_main
from mahavitrain_nxtra import mahavitran_main
from Mahavitran_DC import mahavitran_dc_main
from Database_OperationsV1_NXTRA import insert_problematic
from Database_OperationsV1_NXTRA import duplicate_bill_check


config_obj = configparser.ConfigParser()
config_obj.read('/code/config.ini')

sppaths = config_obj['spdl_path']
spparam = config_obj['spdoclib']
sprlpath = config_obj['sp_relative_path']
fol_loc = config_obj['folder_path']

spsite = spparam['rootsite']
spdoclib = spparam['site_url']
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
sprproot= sprlpath['root']
sprpproblem = sprlpath['problematic']
sprpduplicate = sprlpath['duplicate'] ###Add duplicate path

cons_no = ''
BILL = ''
bill_no = ''
ctx = ClientContext(spdoclib).with_credentials(ClientCredential(cid, cs))

                                             

def check_which_bill(path):
    global BILL, bill_no
    with pdfplumber.open(path) as pdf:
        pg1 = pdf.pages[0]
        text = pg1.extract_text()
        words1 = pg1.extract_words()
    lst = []
    for i in range(len(words1)):
        lst.append(words1[i]['text'])
    if 'Tata Power' in text:
        BILL = 'TATA'
        c=0
        for i in lst:
            if 'Bill No. :' == ' '.join(lst[c:c+3]):
                bill_no = lst[c+3]
                break
            c+=1 
    if 'Adani Electricity' in text or 'ADANI ELECTRICITY' in text:
        BILL = 'ADANI'
        q = 0
        for k in lst:
            if 'Bill No. :'  == ' '.join(lst[q:q+3]):
                bill_no = lst[q+3]
                layout = 1
                break
            q+=1
    if 'Last Rcpt Dt/No' in text:
        BILL = 'PUNE_MAHAVITRAN'
        a = 0
        for i in lst:
            if 'Last Rcpt Dt/No' in ' '.join(lst[a:a+3]):
                bill_no = lst[a+5]
                break
            a+=1
    if 'Last Receipt No./Date' in text:
        BILL = 'MAHAVITRAN'
        m=0
        for i in lst:
            if "BILL OF SUPPLY FOR THE MONTH OF" == ' '.join(lst[m:m+7]):
                bill_no = lst[m+8]  
                break
            m+=1

    if 'BESCOM' in text:
        BILL = 'BANGLORE'
        table1 = pg1.extract_tables()[0]
        bill_no = table1[1][2]

    if 'TamilNadu Generation' in text:
        BILL = 'CHENNAI'
        a=0
        for i in lst:
            if 'Bill No.' == ' '.join(lst[a:a+2]):
                bill_no = lst[a+2]
                break
            a+=1
    if 'NOIDA' in text:
        BILL = 'NOIDA'
        p=0
        for i in lst:
            if 'Bill No' in ' '.join(lst[p:p+2]):
                bill_no = lst[p+2]
                break
            p+=1
    if 'AVAADA' in text:
        BILL = 'AVADA'
        a=0
        for i in lst:
            if 'Invoice No./Date :' == ' '.join(lst[a:a+3]):
                bill_no = lst[a+3]
                break
            a+=1
    if 'AMPSOLAR' in text:
        BILL = 'AMP'
        table = pdf.pages[0].extract_tables()[0]
        bill_no = table[3][-1]
        
    return BILL,bill_no


def insert_processed_and_duplicate(path,status):
    if BILL == 'ADANI':
        adani_main(path,status)
    if BILL == 'PUNE_MAHAVITRAN':
        mahavitran_dc_main(path,status)
    if BILL == 'MAHAVITRAN':
        mahavitran_main(path,status)
    if BILL == 'CHENNAI':
        chennai_main(path,status)
    if BILL == 'AVADA':
        avada_main(path,status)
    if BILL == 'AMP':
        amp_main(path,status)


    #if BILL == 'TATA':
    #    exec(open(r'D:\Bill Extraction Files\Tata.py').read(), {'path': path , 'status':status})
    
    #if BILL == 'BANGLORE':
    #    exec(open(r'D:\Bill Extraction Files\Banglore2.py').read(), {'path': path , 'status':status} )
    
    #if BILL == 'NOIDA':
    #    exec(open(r'D:\Bill Extraction Files\Noida2.py').read(), {'path': path , 'status':status})
    


def move_to_folder_processed(folder):
    try:
        global sprppro
        file_from = ctx.web.get_folder_by_server_relative_url(folder).execute_query()
        file_to = file_from.move_to(sprppro).execute_query()
        print("'{0}' moved into '{1}'".format(folder, sprppro))
    except Exception as e:
        print(">>> ",e)
def try_get_folder(url):
    try:
        return ctx.web.get_folder_by_server_relative_url(url).get().execute_query()
    except ClientRequestException as e:
        if e.response.status_code == 404:
            return None
        else:
            raise ValueError(e.response.text)
        

def bill_main(sproot): 

    global sprppro, ctx
    try:
        root_folder = ctx.web.get_folder_by_server_relative_path(sproot)
        root_folder.expand(["Folders"]).get().execute_query()
    except Exception as E:
        print(E)
    metaurl = ''
    for folder in root_folder.folders:
        folder = try_get_folder(folder.serverRelativeUrl)
        files = folder.get_files(True).execute_query()
        for f in files:
            metaurl = f.properties['ServerRelativeUrl']
            finalurl = spsite+metaurl
            file_name = os.path.basename(finalurl)
            savefile = os.path.join(lsppath, file_name)

            with open(savefile,'wb') as local_file:
                p_file = ctx.web.get_file_by_server_relative_url(metaurl).download(local_file).execute_query()
            if '.pdf' in file_name or '.PDF' in file_name:
                BILL = ''
                print('pdf',file_name)
                BILL,bill_no = check_which_bill(savefile)
                if BILL == '':
                    status = 'PROBLEMATIC'
                    insert_problematic(savefile,status)
                else:
                    duplicate =  duplicate_bill_check(bill_no)
                    if duplicate == 1:
                        status = 'DUPLICATE'
                        insert_processed_and_duplicate(savefile,status)

                    if duplicate ==  0:
                        status = 'PROCCESSED'
                        insert_processed_and_duplicate(savefile,status)
            else:
                status = 'PROBLEMATIC'
                insert_problematic(savefile,status)
            try:
                os.remove(savefile)
            except Exception as e:
                print(e)
        move_to_folder_processed(folder.serverRelativeUrl)

bill_main(sproot)

    


    

