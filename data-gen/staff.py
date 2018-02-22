from datetime import datetime, timedelta
import time
import pickle
import random

from utils import *

def synthesize_staff_record():
    PERCENTAGE_MALE_STAFF = 0.5
    MIN_STAFF_AGE = 25
    MAX_STAFF_AGE = 50

    name = None
    if random.random() < PERCENTAGE_MALE_STAFF:
        name = synthesize_male_name()
    else:
        name = synthesize_female_name()

    min_date_of_birth = time.strftime(
        '%Y-%m-%d',
        (datetime.now() - timedelta(days=MAX_STAFF_AGE*365)).timetuple())
    max_date_of_birth = time.strftime(
        '%Y-%m-%d',
        (datetime.now() - timedelta(days=MIN_STAFF_AGE*365)).timetuple())
    date_of_birth = synthesize_date(min_date_of_birth, max_date_of_birth)
    return (name[0], name[1], date_of_birth)

def synthesize_staff_table():
    NUM_TOTAL_RECORD = 200
    START_OF_STAFF_ID = 10

    staffs = []
    for index in range(0, NUM_TOTAL_RECORD):
        record = synthesize_staff_record()
        staffs.append((index + START_OF_STAFF_ID, record[0], record[1], record[2]))

    serialized_staff_file = open('staff.pickle', 'wb')
    pickle.dump(staffs, serialized_staff_file)
    serialized_staff_file.close()
        
    return staffs

if __name__ == '__main__':
    FORMAT = "INSERT INTO staff values(%d, '%s', '%s', '%s') ;"
    staffs = synthesize_staff_table()
    commands = []
    for staff in staffs:
        commands.append(FORMAT%(staff[0], staff[1], staff[2], staff[3]))
    for command in commands:
        print(command)
