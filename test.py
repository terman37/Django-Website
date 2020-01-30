import re
import pandas as pd

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
    op_type = 'std'
    ddate = ''
    desc = ''
    memo = ''
    bankid = ''
    nval = 0
    nsolde = 0

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
                # TODO find cpt_id FROM CB OWNER
                cpt_name = cpt[0:6] + '******' + cpt[-4:]
                cptid = 0
            else:
                # TODO retreive cpt id from cpt_name
                cpt_name = ''
                cptid = 0

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
                bankid = 'CB-' + cpt_name + '-' + bankid
            else:
                bankid = cpt_name + '-' + bankid

            operations.append([cptid, op_type, ddate, desc, bankid, nval])
            # reset values
            op_type = 'std'
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


def ofx_to_db(myfilename):
    with open(myfilename, 'r') as f:
        myofx = f.readlines()

    accounts, operations = get_op_and_accounts_updates(myofx)

    print((operations))
    print((accounts))

    # TODO CHECK / APPEND / UPDATE OPERATIONS AND ACCOUNTS FROM IMPORT RESULT
    # THEN CHECK IF EXISTS / APPEND EACH OPERATION TO OPERATION TABLE
    # THEN UPDATE ACCOUNT NSOLDE FOR EACH ACCOUNT

    # Returned value should be number of lines added in operations / nb of line updated in accounts
    # or error message
    return True


ofx_to_db('.vs/CM-20200122.ofx')