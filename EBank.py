#!/bin/env python
# _*_ coding:utf-8_*_
import json
import time
import yaml


def new_account(account_id, account_password):
    account_file = open('bank_account.json', 'r')
    if len(account_file.read()) != 0:
        with open('bank_account.json', 'r') as f:
            account_dict = json.load(f)
        account_dict[account_id] = account_password
        with open('bank_account.json', 'w') as f:
            json.dump(account_dict, f)
        initialize_account(account_id)
    else:
        account_dict = {}
        account_dict[account_id] = account_password
        with open('bank_account.json', 'w') as f:
            json.dump(account_dict, f)
        initialize_account(account_id)


def check_account_exist(account_id):
    account_file = open('bank_account.json', 'r')
    if len(account_file.read()) != 0:
        with open('bank_account.json', 'r') as f:
            account_dict = json.load(f)
            if account_dict.has_key(account_id) is True:
                return True
            else:
                return False
    else:
        return False


def log_account(account_id, account_password):
    'log in an existing account,validity needed.'
    if check_account_exist(account_id) is True:
        with open('bank_account.json', 'r') as f:
            account_dict = json.load(f)
        if account_dict[account_id] == account_password:
            return True
        else:
            return False
    else:
        return False


def initialize_account(account_id):
    account_info_file = open('account_info.json', 'r')
    if len(account_info_file.read()) != 0:
        with open('account_info.json', 'r') as f:
            account_info_dict = json.load(f)
        account_info_dict[account_id] = 15000
        with open('account_info.json', 'w') as f:
            json.dump(account_info_dict, f)
    else:
        account_info_dict = {}
        account_info_dict[account_id] = 15000
        with open('account_info.json', 'w') as f:
            json.dump(account_info_dict, f)


def query(account_id):
    'query current account info.Log in needed.'
    with open('account_info.json', 'r') as f:
        account_info = json.load(f)
    print (
            'Here is your account info : Balance:%s;Bill:%s' % (
        account_info[account_id], 15000 - account_info[account_id]))


def withdraw(account_id, amount):
    'balance verification needed.'
    with open('account_info.json', 'r') as f:
        account_info_dict = json.load(f)
    if account_info_dict[account_id] - amount * 1.05 < 0:
        print "Sorry you have insufficient balance"
        return False
    else:
        account_info_dict[account_id] -= amount * 1.05
        print 'Withdrew successfully!'
        with open('account_info.json', 'w') as f:
            json.dump(account_info_dict, f)
        return True


def bookkeeping_withdraw(account_id, amount):
    'take every expense down'
    account_book = open('%s.json' % account_id, 'a+')
    if len(account_book.read()) != 0:
        with open('%s.json' % account_id, 'r') as f:
            account_book_dict = json.load(f)
        bookkeeping_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        account_book_dict[bookkeeping_time] = [' withdrew: ', amount, 'with interest: ', amount * 0.05]
        with open('%s.json' % account_id, 'w') as f:
            json.dump(account_book_dict, f)
        return True
    else:
        account_book_dict = {}
        bookkeeping_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        account_book_dict[bookkeeping_time] = [' withdrew: ', amount, 'with interest: ', amount * 0.05]
        with open('%s.json' % account_id, 'w') as f:
            json.dump(account_book_dict, f)
        return True


def check_bills(account_id):
    with open('%s.json' % account_id, 'r') as f:
        bill_dict = yaml.load(f)
    print bill_dict
    return True


def generate_bills():
    'genernate a bill list every 30th of a month'
    localtime = time.localtime(time.time())
    if localtime[2] == 30:
        with open('account_info.json', 'r') as f:
            account_info_dict = yaml.load(f)
        for keys, values in account_info_dict.items():
            if values < 15000:
                print 'Account %s bills:' % keys, 15000 - values
                with open('bills.json', 'w') as f:
                    json.dump(account_info_dict[keys], f)
    return True


def spend(account_id, password, amount):
    'for external requests.Balance verification needed.'
    account_id = raw_input('Pleas input an account:')
    password = raw_input('Please input password:')
    if log_account(account_id, password) is True:
        with open('account_info.json', 'r') as f:
            account_id_dict = json.load(f)
        if account_id_dict[account_id] - amount >= 0:
            account_id_dict[account_id] -= amount
            with open('account_info.json', 'w') as f:
                json.dump(account_id_dict, f)
            return True
        else:
            return False
    else:
        print('Wrong account or password!')
        return False


def payback(account_id, amount):
    'pay back bills,add up the balance.'
    with open('account_info.json', 'r') as f:
        account_info_dict = json.load(f)
    balance = account_info_dict[account_id]
    if balance + amount <= 15000:
        account_info_dict[account_id] += amount
        with open('account_info.json', 'w') as f:
            json.dump(account_info_dict, f)
        return True
    else:
        print('Payback amount is bigger than your debt.Payback fails.')
        return False
