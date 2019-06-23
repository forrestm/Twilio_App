#!/usr/bin/env python3
# Needs to be executable and Crontab-ed

import yaml
from pathlib import Path
from datetime import date, timedelta, datetime

# Creates the current date object
CURRENT_DATETIME = date.today()

# Formats the date for filename
CURRENT_DATE = CURRENT_DATETIME.strftime("%b-%d-%Y")
CURRENT_DATE_VAR = CURRENT_DATETIME.strftime("%A-%m-%d")

# Creates the final file with extension string
CURRENT_DATE_YAML = CURRENT_DATE + ".yaml"

GROCERIES_WK_BUDGET = 100
OTHER_WK_BUDGET = 250

# Needs to be changed to correct path
# path = Path.home().joinpath('Documents', 'f-mo', 'Twilio_App', 'Weekly_Charges', f'{CURRENT_DATE_YAML}')

# def Received_Bank_text(body):
#     chase_list = body.split()
#     amount = chase_list[6][1:]
#     date = datetime.strptime(chase_list[-11], '%m/%d/%Y')
#     business = " ".join(chase_list[8:-12])

#     charge_date = date.strftime("%A-%m-%d")

#     with path.open(mode='r') as fid:
#         charges = yaml.safe_load(fid)

#     charges[charge_date].append(amount)

#     with path.open(mode='w') as fid:
#         yaml.safe_dump(charges, fid, default_flow_style=False)

class Budget(object):

    FILEPATH = Path.home().joinpath('Documents',
                                    'f-mo',
                                    'Twilio_App',
                                    'Weekly_Charges',
                                    f'{CURRENT_DATE_YAML}')
    def __init__(self, body):
        self.body = body

    def write_to(self, charges):
        self.charges = charges
        with self.FILEPATH.open(mode='w') as fid:
            yaml.safe_dump(charges, fid, default_flow_style=False)

    def read_from(self):
        with self.FILEPATH.open(mode='r') as fid:
            charges = yaml.safe_load(fid)
        return charges

    def Received_Bank_text(self):
        chase_list = self.body.split()
        amount = float(chase_list[6][1:])
        date = datetime.strptime(chase_list[-11], '%m/%d/%Y')
        business = " ".join(chase_list[8:-12])
        charge_date = date.strftime("%A-%m-%d")
        charges = self.read_from()
        charges[charge_date].append(amount)
        self.write_to(charges)
        return f'Lawd, you spent ${amount} at {business}?!'

    def Groceries_Yes(self):
        charges = self.read_from()
        grocery_charge = charges[CURRENT_DATE_VAR].pop(-1)
        charges['Groceries'].append(grocery_charge)
        current_groceries = GROCERIES_WK_BUDGET - sum(charges['Groceries'])
        self.write_to(charges)
        return f'You got ${current_groceries} left for groceries baby'

    def Undo(self):
        charges = self.read_from()
        undo_charge = charges[CURRENT_DATE_VAR].pop(-1)
        self.write_to(charges)
        return f'Undid ${undo_charge}'

    def Current_Amounts(self, grocery):
        self.grocery = grocery
        charges = self.read_from()
        if grocery:
            current_groceries = GROCERIES_WK_BUDGET - sum(charges['Groceries'])
            return f'You got ${current_groceries} left for groceries baby'
        else:
            current_budget = OTHER_WK_BUDGET - sum([sum(item) for key,item in charges.items()])
            return f'You got ${round(current_budget, 2)} left for the week sugar'

    def Help(self):
        return u'I am your personal helper \U0001F481'

    
    # def __str__(self):
    #     return f'Spent ${self.amount} at {self.business} on {self.charge_date}'
    
    # def __repr__(self):
    #     return f'Spent ${self.amount} at {self.business} on {self.charge_date}'



