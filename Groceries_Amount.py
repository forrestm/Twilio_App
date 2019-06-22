#!/usr/bin/env python3
# Needs to be executable and Crontab-ed

import yaml
from pathlib import Path
from datetime import date, timedelta

# Creates the current date object
CURRENT_DATETIME = date.today()

# Formats the date for filename
CURRENT_DATE = CURRENT_DATETIME.strftime("%b-%d-%Y")

# Creates the final file with extension string
CURRENT_DATE_YAML = CURRENT_DATE + ".yaml"

# Needs to be changed to correct path
path = Path.home().joinpath('Documents', 'f-mo', 'Twilio_App', 'Weekly_Charges', f'{CURRENT_DATE_YAML}')

inital_format = {(date.today() + timedelta(days=i)).strftime("%A-%m-%d"):[] for i in range(0,7)}
inital_format['Groceries'] = []

with path.open(mode='w') as fid:
    yaml.safe_dump(inital_format, fid, default_flow_style=False)


# just append to every "DAY MONTH-DAY" and it will work. Adding will be the same