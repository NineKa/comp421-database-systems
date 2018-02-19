import pickle
import random
import time

COMMON_FEMALE_NAMES_FILE = 'common-female-names.pickle'
COMMON_MALE_NAMES_FILE = 'common-male-names.pickle'
COMMON_SURNAMES_FILE = 'common-surnames.pickle'

def synthesize_male_name():
    male_names_handle = open(COMMON_MALE_NAMES_FILE, 'rb')
    surnames_handle = open(COMMON_SURNAMES_FILE, 'rb')
    male_names = pickle.load(male_names_handle)
    surnames = pickle.load(surnames_handle)
    male_names_handle.close()
    surnames_handle.close()
    return (random.choice(male_names), random.choice(surnames))

def synthesize_female_name():
    female_names_handle = open(COMMON_FEMALE_NAMES_FILE, 'rb')
    surnames_handle = open(COMMON_SURNAMES_FILE, 'rb')
    female_names = pickle.load(female_names_handle)
    surnames = pickle.load(surnames_handle)
    female_names_handle.close()
    surnames_handle.close()
    return (random.choice(female_names), random.choice(surnames))

def synthesize_date(start, end):
    DATE_FORMAT = '%Y-%m-%d'
    start_time = time.mktime(time.strptime(start, DATE_FORMAT))
    end_time = time.mktime(time.strptime(end, DATE_FORMAT))
    selected_time = start_time + random.random() * (end_time - start_time)
    return time.strftime(DATE_FORMAT, time.localtime(selected_time))

