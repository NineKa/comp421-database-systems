from datetime import datetime, timedelta
import time

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
    MIN_AGE_DIFF_NON_TWIN_CHILDREN = 1
    TWIN_PROBABILITY = 0.1
    MAX_TWIN_SIZE = 3
    MAX_RANDOM_FAMILY_SIZE = 5

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
        father_dob_ts = datetime.strptime(father_dob, '%Y-%m-%d')
        mother_dob_ts = datetime.strptime(mother_dob, '%Y-%m-%d')
        min_children_dob = (father_dob_ts if father_dob_ts > mother_dob_ts else mother_dob_ts) + \
                           timedelta(days=MIN_AGE_GAP_PARENTS_CHILDREN*365)
        max_children_dob = (father_dob_ts if father_dob_ts > mother_dob_ts else mother_dob_ts) + \
                           timedelta(days=MAX_AGE_GAP_PARENTS_CHILDREN*365)
        if max_children_dob > (datetime.now() - timedelta(days=MIN_AGE*365)):
            max_children_dob = datetime.now() - timedelta(days=MIN_AGE*365)
        print(min_children_dob)
        print(max_children_dob)
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
                children_dob = synthesize_date(
                    time.strftime('%Y-%m-%d', min_children_dob.timetuple()),
                    time.strftime('%Y-%m-%d', max_children_dob.timetuple()))
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
        
    return synthesize_children_date_of_birth(5, father_dob, mother_dob)
