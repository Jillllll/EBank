#!/bin/env python
# _*_ coding=utf-8_*_
import EBank

todo_tup = ('Create a new account', 'Log into an existing account')
for i, element in enumerate(todo_tup, start=1):
    print i, todo_tup[i - 1]
todo_choice = raw_input('Welcome to JD Bank!What do you expect to do?')
while True:
    if todo_choice == '1':
        account_id = raw_input('Please input an account:')
        is_account_exist = EBank.check_account_exist(account_id)
        if is_account_exist is True:
            print ('Account already exists,please change to a different account.')
        else:
            account_password = raw_input('Please input password:')
            EBank.new_account(account_id, account_password)
            break

    elif todo_choice == '2':
        account_id = raw_input('Please input your account:')
        account_password = raw_input('Please input password:')
        log_account_check = EBank.log_account(account_id, account_password)
        if log_account_check is True:
            todo_tup2 = ('Show my account information', 'Withdraw with 5% interests', 'Check my bills')
            for i, element in enumerate(todo_tup2, start=1):
                print i, todo_tup2[i - 1]
            todo_choice2 = raw_input('Welcome %s!What do you expect to do?' % account_id)
            if todo_choice2 == '1':
                EBank.query(account_id)
                break
            elif todo_choice2 == '2':
                amount = input('How much do you need to withdraw?')
                withdraw_result = EBank.withdraw(account_id, amount)
                if withdraw_result is True:
                    EBank.bookkeeping_withdraw(account_id, amount)
                    break
                else:
                    break
            elif todo_choice2 == '3':
                EBank.check_bills(account_id)
                break
            else:
                print('Please input 1/2 or 3')
        else:
            print ('Wrong account or password')
    else:
        print ('Please input 1 or 2')

EBank.generate_bills()
