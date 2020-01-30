# Basics
from django.shortcuts import render
from .models import Accounts, Operations, CbOwner
import re
import pandas as pd
# Decorators
from django.contrib.auth.decorators import login_required
# import
from django.conf import settings
from django.core.files.storage import FileSystemStorage


@login_required
def summary(request):
    pagetitle = "Summary"
    accounts = Accounts.objects.filter(d_inactive__isnull=True).order_by('t_type', 't_name')
    return render(request, 'cpts/summary.html', {'title': pagetitle, 'mydatas': accounts})


@login_required
def importofx(request):
    pagetitle = "Import Ofx"
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        result = ofx_to_db(filename)
        # TODO manage if ofx file to db not working

        uploaded_file_url = fs.url(filename)
        return render(request, 'cpts/importofx.html', {'title': pagetitle, 'uploaded_file_url': uploaded_file_url})
    return render(request, 'cpts/importofx.html', {'title': pagetitle})


# Functions:
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


def add_operations(operations):
    for op in operations:
        # CHECK IF OPERATION ALREADY EXISTS IN DB
        try:
            oldop = Operations.objects.get(t_bankop_key=op.bankid)
        except:
            print("op %s already existing" % op.bankid)
        else:
            # IF NOT ADD NEW LINE IN OPERATIONS
            newop = Operations(cpt_id=op.cpt_id,
                               t_op_type=op.op_type,
                               d_date=op.ddate,
                               t_desc=op.desc,
                               t_bankop_key=op.bankid,
                               n_value=op.nval
                               )
            newop.save()
    return 0


def ofx_to_db(myfilename):
    with open('media/' + myfilename, 'r') as f:
        myofx = f.readlines()

    accounts, operations = get_op_and_accounts_updates(myofx)

    print(operations)
    x = add_operations(operations)
    print(accounts)

    # TODO CHECK / APPEND / UPDATE OPERATIONS AND ACCOUNTS FROM IMPORT RESULT
    # THEN CHECK IF EXISTS / APPEND EACH OPERATION TO OPERATION TABLE
    # THEN UPDATE ACCOUNT NSOLDE FOR EACH ACCOUNT

    # Returned value should be number of lines added in operations / nb of line updated in accounts
    # or error message
    return True
