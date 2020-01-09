# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accounts(models.Model):
    cpt_id = models.AutoField(db_column='CPT_ID', primary_key=True)  # Field name made lowercase.
    t_cpt_num = models.CharField(db_column='T_CPT_NUM', unique=True, max_length=50, blank=True, null=True)  # Field name made lowercase.
    t_name = models.CharField(db_column='T_NAME', max_length=255)  # Field name made lowercase.
    n_solde_avail = models.FloatField(db_column='N_SOLDE_AVAIL')  # Field name made lowercase.
    n_solde_locked = models.FloatField(db_column='N_SOLDE_LOCKED')  # Field name made lowercase.
    t_type = models.CharField(db_column='T_TYPE', max_length=255)  # Field name made lowercase.
    t_banque = models.CharField(db_column='T_BANQUE', max_length=255)  # Field name made lowercase.
    d_inactive = models.DateField(db_column='D_INACTIVE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCOUNTS'


class Calendar(models.Model):
    cal_id = models.AutoField(db_column='CAL_ID', primary_key=True)  # Field name made lowercase.
    d_date = models.DateField(db_column='D_DATE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CALENDAR'


class Categories(models.Model):
    cat_id = models.AutoField(db_column='CAT_ID', primary_key=True)  # Field name made lowercase.
    t_cat_name = models.CharField(db_column='T_CAT_NAME', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CATEGORIES'


class CatAssign(models.Model):
    cat_assign_id = models.AutoField(db_column='CAT_ASSIGN_ID', primary_key=True)  # Field name made lowercase.
    t_desc = models.CharField(db_column='T_DESC', max_length=1000)  # Field name made lowercase.
    cat = models.ForeignKey(Categories, models.DO_NOTHING, db_column='CAT_ID')  # Field name made lowercase.
    cpt = models.ForeignKey(Accounts, models.DO_NOTHING, db_column='CPT_ID', blank=True, null=True)  # Field name made lowercase.
    d_start = models.DateField(db_column='D_START', blank=True, null=True)  # Field name made lowercase.
    d_end = models.DateField(db_column='D_END', blank=True, null=True)  # Field name made lowercase.
    n_val_min = models.FloatField(db_column='N_VAL_MIN', blank=True, null=True)  # Field name made lowercase.
    n_val_max = models.FloatField(db_column='N_VAL_MAX', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CAT_ASSIGN'


class CbOwner(models.Model):
    cbowner_id = models.AutoField(db_column='CBOWNER_ID', primary_key=True)  # Field name made lowercase.
    t_cb_num = models.CharField(db_column='T_CB_NUM', max_length=255)  # Field name made lowercase.
    t_cb_owner = models.CharField(db_column='T_CB_OWNER', max_length=255)  # Field name made lowercase.
    cpt = models.ForeignKey(Accounts, models.DO_NOTHING, db_column='CPT_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CB_OWNER'


class CbPlan(models.Model):
    cb_plan_id = models.AutoField(db_column='CB_PLAN_ID', primary_key=True)  # Field name made lowercase.
    n_year = models.IntegerField(db_column='N_YEAR')  # Field name made lowercase.
    n_month = models.IntegerField(db_column='N_MONTH')  # Field name made lowercase.
    d_start = models.DateField(db_column='D_START')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CB_PLAN'


class Operations(models.Model):
    op_id = models.AutoField(db_column='OP_ID', primary_key=True)  # Field name made lowercase.
    cpt = models.ForeignKey(Accounts, models.DO_NOTHING, db_column='CPT_ID')  # Field name made lowercase.
    t_op_type = models.CharField(db_column='T_OP_TYPE', max_length=50)  # Field name made lowercase.
    d_date = models.DateField(db_column='D_DATE')  # Field name made lowercase.
    t_desc = models.CharField(db_column='T_DESC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    t_bankop_key = models.CharField(db_column='T_BANKOP_KEY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    n_value = models.FloatField(db_column='N_VALUE')  # Field name made lowercase.
    cat = models.ForeignKey(Categories, models.DO_NOTHING, db_column='CAT_ID')  # Field name made lowercase.
    t_comment = models.CharField(db_column='T_COMMENT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    n_solde = models.FloatField(db_column='N_SOLDE', blank=True, null=True)  # Field name made lowercase.
    n_match_id = models.IntegerField(db_column='N_MATCH_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OPERATIONS'
