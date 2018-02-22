from datetime import datetime, timedelta
import time
import pickle
import random

from utils import *

def synthesize_solo_customer_record():
    MIN_AGE = 15
    MAX_AGE = 70
    PERCENTAGE_MALE_CUSTOMER = 0.5

    name = None
    gender = None
    if random.random() < PERCENTAGE_MALE_CUSTOMER:
        name = synthesize_male_name()
        gender = 'MALE'
    else:
        name = synthesize_female_name()
        gender = 'FEMALE'
    
    min_date_of_birth = time.strftime(
        '%Y-%m-%d',
        (datetime.now() - timedelta(days=MAX_AGE*365)).timetuple())
    max_date_of_birth = time.strftime(
        '%Y-%m-%d',
        (datetime.now() - timedelta(days=MIN_AGE*365)).timetuple())
    date_of_birth = synthesize_date(min_date_of_birth, max_date_of_birth)

    return (name[0], name[1], gender, date_of_birth)

def synthesize_family_customer_records(size=None):
    MIN_AGE = 5
    MAX_AGE = 70
    MIN_AGE_PARENTS = 27
    MIN_AGE_GAP_PARENTS_CHILDREN = 25
    MAX_AGE_GAP_PARENTS_CHILDREN = 45
    MAX_AGE_DIFF_PARENTS = 5
    TWIN_PROBABILITY = 0.1
    MAX_TWIN_SIZE = 3
    MAX_RANDOM_FAMILY_SIZE = 5
    CHILDREN_MALE_PROBABILITY = 0.5

    assert (size is None) or (size >= 2)
    
    def synthesize_parent_date_of_birth():
        min_parent_age_index = (datetime.now() - timedelta(days=(MAX_AGE - MAX_AGE_DIFF_PARENTS) * 365)).timetuple()
        max_parent_age_index = (datetime.now() - timedelta(days=(MIN_AGE_PARENTS + MAX_AGE_DIFF_PARENTS) * 365)).timetuple()
        parent_age_index = datetime.strptime(synthesize_date(
            time.strftime('%Y-%m-%d', min_parent_age_index),
            time.strftime('%Y-%m-%d', max_parent_age_index)), '%Y-%m-%d')
        min_parent_age = (parent_age_index - timedelta(days=MAX_AGE_DIFF_PARENTS * 365)).timetuple()
        max_parent_age = (parent_age_index + timedelta(days=MAX_AGE_DIFF_PARENTS * 365)).timetuple()
        father_dob = synthesize_date(
            time.strftime('%Y-%m-%d', min_parent_age),
            time.strftime('%Y-%m-%d', max_parent_age))
        mother_dob = synthesize_date(
            time.strftime('%Y-%m-%d', min_parent_age),
            time.strftime('%Y-%m-%d', max_parent_age))
        return (father_dob, mother_dob)

    def synthesize_children_date_of_birth(num=0, father_dob=None, mother_dob=None):
        assert (not (father_dob is None)) and (not (mother_dob is None))
        assert num < (MAX_AGE_GAP_PARENTS_CHILDREN - MIN_AGE_GAP_PARENTS_CHILDREN)
        father_dob_ts = datetime.strptime(father_dob, '%Y-%m-%d')
        mother_dob_ts = datetime.strptime(mother_dob, '%Y-%m-%d')
        min_children_dob = (father_dob_ts if father_dob_ts > mother_dob_ts else mother_dob_ts) + \
                           timedelta(days=MIN_AGE_GAP_PARENTS_CHILDREN*365)
        max_children_dob = (father_dob_ts if father_dob_ts > mother_dob_ts else mother_dob_ts) + \
                           timedelta(days=MAX_AGE_GAP_PARENTS_CHILDREN*365)
        if max_children_dob > (datetime.now() - timedelta(days=MIN_AGE*365)):
            max_children_dob = datetime.now() - timedelta(days=MIN_AGE*365)
        children_dobs = []
        while num > 0:
            if (num >= 2) and (random.random() < TWIN_PROBABILITY):
                children_dob = synthesize_date(
                    time.strftime('%Y-%m-%d', min_children_dob.timetuple()),
                    time.strftime('%Y-%m-%d', max_children_dob.timetuple()))
                twin_size = random.randint(2, num if num < (MAX_TWIN_SIZE + 1) else (MAX_TWIN_SIZE + 1))
                children_dobs = children_dobs + [children_dob] * twin_size
                num = num - twin_size
            else:
                existed_ts = list(map(lambda x : datetime.strptime(x, '%Y-%m-%d'), children_dobs))
                children_dob = None
                valid_date = False
                while not valid_date:
                    children_dob = synthesize_date(
                        time.strftime('%Y-%m-%d', min_children_dob.timetuple()),
                        time.strftime('%Y-%m-%d', max_children_dob.timetuple()))
                    children_ts = datetime.strptime(children_dob, '%Y-%m-%d')
                    valid_date = True
                    for existed_dob in existed_ts:
                        if (children_ts > existed_dob) and \
                           (children_ts < (existed_dob + timedelta(days=365))):
                            valid_date = False
                        if (children_ts < existed_dob) and \
                           (children_ts > (existed_dob - timedelta(days=365))):
                            valid_date = False
                children_dobs.append(children_dob)
                num = num - 1
        return children_dobs


    family_names = []
    father_name = synthesize_male_name()
    mother_name = synthesize_female_name()
    min_parent_dob = time.strftime(
        '%Y-%m-%d',
        (datetime.now() - timedelta(days=MAX_AGE*365)).timetuple())
    max_parent_dob = time.strftime(
        '%Y-%m-%d',
        (datetime.now() - timedelta(days=(MAX_AGE-2*MAX_AGE_DIFF_PARENTS)*365)).timetuple())
    father_dob, mother_dob = synthesize_parent_date_of_birth()
    family_names.append((father_name[0], father_name[1], 'MALE', father_dob))
    family_names.append((mother_name[0], father_name[1], 'FEMALE', mother_dob))

    num_children = random.randint(0, MAX_RANDOM_FAMILY_SIZE - 2) if (size is None) else (size - 2)
    children_dobs = synthesize_children_date_of_birth(num_children, father_dob, mother_dob)
    for children_dob in children_dobs:
        children_name = None
        children_gender = None
        if random.random() < CHILDREN_MALE_PROBABILITY:
            children_name = (synthesize_male_name()[0], father_name[1])
            children_gender = 'MALE'
        else:
            children_name = (synthesize_female_name()[0], father_name[1])
            children_gender = 'FEMALE'
        children_record = (children_name[0], children_name[1], children_gender, children_dob)
        family_names.append(children_record)
            
    return family_names

def synthesize_customer_table():
    NUM_TOTAL_RECORD = 500
    FAMILY_PERCENTAGE = 0.6
    START_OF_CUSTOMER_ID = 10

    num_family_customer = int(NUM_TOTAL_RECORD * FAMILY_PERCENTAGE)
    num_solo_customer = NUM_TOTAL_RECORD - num_family_customer

    family_customers = []
    while num_family_customer > 0:
        synthesized_family = None
        if num_family_customer < 5:
            if (num_family_customer < 2):
                num_family_customer = 0
                num_solo_customer = num_solo_customer + num_family_customer
                break
            synthesized_family = synthesize_family_customer_records(num_family_customer)
        else:
            synthesized_family = synthesize_family_customer_records(None)
        num_family_customer = num_family_customer - len(synthesized_family)
        family_customers.append(synthesized_family)

    solo_customers = []
    while num_solo_customer > 0:
        solo_customers.append([synthesize_solo_customer_record()])
        num_solo_customer = num_solo_customer - 1

    customers = family_customers + solo_customers
    random.shuffle(customers)
    serialized_customer_file = open('customer.pickle', 'wb')
    pickle.dump(customers, serialized_customer_file)
    serialized_customer_file.close()

    customer_id = START_OF_CUSTOMER_ID
    records = []
    for customer in customers:
        if len(customer) == 1:
            records.append((customer_id, customer[0][0], customer[0][1],
                            customer[0][2], customer[0][3]))
            customer_id = customer_id + 1
        else:
            for record in customer:
                records.append((customer_id, record[0], record[1], record[2], record[3]))
                customer_id = customer_id + 1
    return records

if __name__ == '__main__':
    FORMAT = "INSERT INTO customer values(%d, '%s', '%s', '%s', '%s') ;"
    customers = synthesize_customer_table()
    commands = []
    for customer in customers:
        commands.append(FORMAT%(customer[0], customer[1], customer[2],
                                customer[3], customer[4]))
    for command in commands:
        print(command)
