# How to use:
# Copy a csv that has one column of names into the same folder as this python program.
# Name the csv names.csv
# Run the python program.
# It should create a csv called contact_info.csv as an output.

# Improvements to be implemented:
#     Handling error 404
#     Handling exception 429
#     Moving away from google search and to an official API

import requests
import csv
import random
from bs4 import BeautifulSoup

# Add the API Keys for rocketreach in the following list as strings:
apikeys = []

def find_by_linkedin(linkedin):
    url = 'https://api.rocketreach.co/v1/api/lookupProfile'

    # Randomly pick an api key from the list
    apikey = random.choice(apikeys)

    params = {
        'api_key' : apikey,
        'li_url' : linkedin
    }

    r = requests.get(url = url, params = params)

    print(r.status_code)

    if r.status_code == 429:
        # This means you hit a rate limit. Try this function again!
        print(apikey + " has run out of api calls! Trying a new key.")
        print("We are trying to get information for " + linkedin + ".")
        return find_by_linkedin(linkedin)
        # This will get stuck in an infinite recursion if we don't have enough api calls.

    user_info = r.json()
    #return user_info

    clean_user_info = user_info[0].copy()

    # Takes all the links and adds them directly to the user profile.
    if clean_user_info['links']:
        for site, profile in clean_user_info['links'].items():
            # Take the key and value and add it directly to clean_user_info
            clean_user_info[site] = profile
    return clean_user_info

def find_by_name_company(name, company):
    url = 'https://api.rocketreach.co/v1/api/lookupProfile'

    # Randomly pick an api key from the list
    apikey = random.choice(apikeys)

    params = {
        'api_key' : apikey,
        'name' : name,
        'current_employer' : company
    }

    r = requests.get(url = url, params = params)

    print(r.status_code)

    if r.status_code == 429:
        # This means you hit a rate limit. Try this function again!
        print(apikey + " has run out of api calls! Trying a new key.")
        return find_by_name_company(name, company)
        # This will get stuck in an infinite recursion if we don't have enough api calls.

    user_info = r.json()
    #return user_info

    clean_user_info = user_info[0].copy()

    # Takes all the links and adds them directly to the user profile.
    if clean_user_info['links']:
        for site, profile in clean_user_info['links'].items():
            # Take the key and value and add it directly to clean_user_info
            clean_user_info[site] = profile
    return clean_user_info

def get_LinkedIn (name):
    URL = 'https://www.google.com/search'
    name = name.replace(' ', '''" "''')
    print('''"''' + name + '''"''' + ''' "Harvard" "Linkedin"''')
    params = {
        'q' : '''"''' + name + '''"''' + ''' "Harvard" "Linkedin"'''
    }
    # print('''"''' + name + '''"''' + ''' "Harvard" "Linkedin"''')
    r = requests.get(url = URL, params = params)
    soup = BeautifulSoup(r.content,'html.parser')

    possible_urls = []

    for link in soup.findAll('cite'):
        if "https://www.linkedin.com/in/" in link.get_text():
            possible_urls.append(link.get_text())

    # print(possible_urls)

    if len(possible_urls) > 0:
        return possible_urls[0]
    else:
        return None

# Display how many api keys you have
print("You have " + str(len(apikeys)) + " api keys.")

# Read the csv file with the names in it.
# The csv file must be called names.csv
Names = []
with open('names.csv') as f:
    rows = csv.reader(f)
    for row in rows:
        if row[0].lower() != 'name' and row[0].lower() != '﻿name'.lower():
            Names.append(row[0])
        # print (row[0])  # Only print the column in the row

# Populate the contact list with the linkedin urls we find
contactList = []
for name in Names:
    print(name)
    linkedInURL = get_LinkedIn(name)
    if linkedInURL:
        # This if statement is so that we don't populate it with any empty urls.
        contactList.append(linkedInURL)

print(contactList)

# output a file called contact_info.csv with all the gathered contact info.
with open('contact_info.csv', 'w') as csvfile:
    fieldnames = ['name', 'current_work_email', 'current_personal_email', 'current_employer', 'current_title', 'location', 'linkedin', 'github', 'facebook', 'twitter', 'googleplus', 'quora', 'stackoverflow']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval = '', extrasaction = 'ignore')

    writer.writeheader()
    for contact in contactList:
        clean_user_info = find_by_linkedin(contact)
        writer.writerow(clean_user_info)
