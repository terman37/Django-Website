# Basics
import re
import os
import pandas as pd
# imports Django
from ..models import Accounts, Operations, CbOwner

# TODO: filter operation like '%BD2B%' from BP, not validated. and adjust SOLDE


def extract_from_line(line):
    # update line to be a list
    tag = ''
    ctag = ''
    val = ''
    sline = line.strip()
    if len(sline) > 0 and sline[0] == "<":
        mysplit = re.split('[<,>]{1}', sline)
        mysplit = list(filter(lambda x: x != '', mysplit))
        tag = mysplit[0]
        if tag[0] == '/':
            tag = ''
            ctag = mysplit[0]
        if len(mysplit) > 1:
            val = mysplit[1]
    return tag, val, ctag


def get_op_and_accounts_updates(myofx):
    # initialization
    cpt_name = ''
    op_type = 'STD'
    ddate = ''
    desc = ''
    memo = ''
    bankid = ''
    nval = 0
    nsolde = 0
    cptid = 0

    flag_CB = False
    operations = []
    accounts = []

    for idx, line in enumerate(myofx):
        # EXTRACT INFORMATOINS FROM READ LINE
        tag, val, ctag = extract_from_line(line)
        # print("tag: %s, val: %s, ctag: %s" % (tag, val, ctag))

        # FILTER TAGS TO DEFINE VALUES
        if tag == 'CREDITCARDMSGSRSV1':
            flag_CB = True
        if tag == '/CREDITCARDMSGSRSV1':
            flag_CB = False

        if tag == 'ACCTID':
            cpt = val
            if flag_CB:
                cpt_name = cpt[0:6] + '******' + cpt[-4:]
                cptid = CbOwner.objects.get(t_cb_num=cpt_name).cpt_id
            else:
                cpt_name = cpt
                cptid = Accounts.objects.get(t_cpt_num=cpt).cpt_id

        if tag == 'DTPOSTED':
            ddate = val[0:4] + '-' + val[4:6] + '-' + val[6:]
        if tag == 'TRNAMT':
            nval = float(val)
        if tag == 'FITID':
            bankid = val
        if tag == 'NAME':
            desc = val
        if tag == 'MEMO':
            memo = val
        if tag == 'BALAMT':
            if flag_CB:
                nsolde = 0
            else:
                nsolde = float(val)

        # CLOSING TAGS : END OF OPERATIONS --> ADD NEW LINE IN OPERATIONS
        if ctag == '/STMTTRN':
            # DESCRIPTION FINAL CONSTRUCT
            if desc != '':
                desc += '-' + memo
            else:
                desc = memo
            if flag_CB:
                desc = 'CB-' + desc
            # BANKID CONSTRUCT
            if flag_CB:
                bankid = 'CB-' + cpt_name + ' - ' + bankid
            else:
                bankid = cpt_name + ' - ' + bankid

            operations.append([cptid, op_type, ddate, desc, bankid, nval])
            # reset values
            op_type = 'STD'
            ddate = 0
            desc = ''
            memo = ''
            bankid = ''
            nval = 0
            nsolde = 0

        # CLOSING TAGS : END OF ACCOUNT --> ADD NEW LINE IN ACCOUNT
        if ctag == '/LEDGERBAL':
            accounts.append([cptid, nsolde])

    colname = ["cptid", "op_type", "ddate", "desc", "bankid", "nval"]
    operations = pd.DataFrame(data=operations, columns=colname)

    colname = ["cptid", "nsolde"]
    accounts = pd.DataFrame(data=accounts, columns=colname)
    return accounts, operations


def add_operations(operations):
    counter = 0
    for idx, op in operations.iterrows():
        # CHECK IF OPERATION ALREADY EXISTS IN DB
        try:
            oldop = Operations.objects.get(t_bankop_key=op.bankid)
            print(oldop)
        except Exception as e:
            print(e)
            # IF NOT ADD NEW LINE IN OPERATIONS
            newop = Operations(cpt_id=op.cptid,
                               t_op_type=op.op_type,
                               d_date=op.ddate,
                               t_desc=op.desc,
                               t_bankop_key=op.bankid,
                               n_value=op.nval,
                               cat_id=34
                               )
            newop.save()
            counter += 1
        # else:
        #     print("op %s already existing" % op.bankid)

    return counter


def update_account(accounts):
    for idx, acc in accounts.iterrows():
        try:
            cpt = Accounts.objects.get(cpt_id=acc.cptid)
            cpt.n_solde_avail = acc.nsolde
            cpt.save()
        except Exception as e:
            print("cannot find account id ", e)


def ofx_to_db(myfilename):
    with open('media/' + myfilename, 'r', encoding="latin_1") as f:
        myofx = f.readlines()

    accounts, operations = get_op_and_accounts_updates(myofx)

    x = add_operations(operations)
    print("%d rows added to OPERATIONS in db" % x)

    update_account(accounts)
    print("file name:", myfilename)
    os.remove('media/' + myfilename)

    return True
