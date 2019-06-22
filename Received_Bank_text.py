#!/usr/bin/env python3
# Needs to be executable and Crontab-ed

import yaml
from pathlib import Path
from datetime import date, timedelta, datetime

# Creates the current date object
CURRENT_DATETIME = date.today()

# Formats the date for filename
CURRENT_DATE = CURRENT_DATETIME.strftime("%b-%d-%Y")

# Creates the final file with extension string
CURRENT_DATE_YAML = CURRENT_DATE + ".yaml"

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
        self.chase_list = self.body.split()
        self.amount = float(self.chase_list[6][1:])
        self.date = datetime.strptime(self.chase_list[-11], '%m/%d/%Y')
        self.business = " ".join(self.chase_list[8:-12])
        self.charge_date = self.date.strftime("%A-%m-%d")

    def write_to(self, charges):
        self.charges = charges
        with self.FILEPATH.open(mode='w') as fid:
            yaml.safe_dump(charges, fid, default_flow_style=False)

    def read_from(self):
        with self.FILEPATH.open(mode='r') as fid:
            charges = yaml.safe_load(fid)
        return charges

    def Received_Bank_text(self):
        charges = self.read_from()
        charges[self.charge_date].append(self.amount)
        self.write_to(charges)
    
    def __str__(self):
        return f'Spent ${self.amount} at {self.business} on {self.charge_date}'
    
    def __repr__(self):
        return f'Spent ${self.amount} at {self.business} on {self.charge_date}'



