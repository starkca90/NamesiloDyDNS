import chevron
from dotenv import load_dotenv
import os
import requests
import tldextract
import xml.etree.ElementTree as ET

load_dotenv()

RECORD_IP_ADDRESS_URL = chevron.render(
    'https://www.namesilo.com/api/dnsListRecords?version={{ version }}&type=xml&key={{ api_key }}&domain={{ domain }}',
    {
        'version': '1',
        'api_key': os.getenv('NAMESILO_KEY'),
        'domain': os.getenv('BASE_DOMAIN')
    })

# Get the current public IP
CURRENT_IP_ADDRESS_URL = 'http://whatismyip.akamai.com/'
current = requests.get(CURRENT_IP_ADDRESS_URL).content.decode('utf8')

print('Current IP address from akamai: %s' % current)

# Get all records from Namesilo
r = requests.get(RECORD_IP_ADDRESS_URL, allow_redirects=True)
xml = ET.fromstring(r.content)

interested_records = os.getenv('A_RECORDS').split(' ')

# Iterate through each record looking for specified record(s)
for record in xml.iter('resource_record'):

    # Only interested in A records, if it's not an A record, keep moving
    record_type = record.find('type').text
    if record_type != 'A':
        continue

    # read host, value, and record_id from current record in xml
    host = record.find('host').text
    value = record.find('value').text
    record_id = record.find('record_id').text

    # if host one we care about, process further
    if host in interested_records:
        print(chevron.render('{{ host }} record IP address: {{ current_ip }}', {
            'host': host,
            'current_ip': value
        }))

        # if record IP address matches CURRENT_IP_ADDRESS_URL, do nothing
        if value == current:
            print('Current IP address matches namesilo record')

        # IP addresses don't match, let's update it
        else:
            print('IP addresses do not match, generating URL to update')

            new_URL = ''

            # Namesilo's API requires the subdomain to be passed in, determine if we have one
            domain_elements = tldextract.extract(host)
            if domain_elements.subdomain:
                # There is a subdomain present
                new_URL = chevron.render('https://www.namesilo.com/api/dnsUpdateRecord?version={{ version }}'
                                         '&type=xml&key={{ api_key }}&domain={{ domain }}&rrid={{ record }}'
                                         '&rrhost={{ subdomain }}&rrvalue={{ public_ip }}&rrttl=3600', {
                                             'version': '1',
                                             'api_key': os.getenv('NAMESILO_KEY'),
                                             'domain': os.getenv('BASE_DOMAIN'),
                                             'record': record_id,
                                             'subdomain': domain_elements.subdomain,
                                             'public_ip': current
                                         })

            else:
                # No subdomain, modifying root record
                new_URL = chevron.render('https://www.namesilo.com/api/dnsUpdateRecord?version={{ version }}'
                                         '&type=xml&key={{ api_key }}&domain={{ domain }}&rrid={{ record }}'
                                         '&rrvalue={{ public_ip }}&rrttl=3600', {
                                             'version': '1',
                                             'api_key': os.getenv('NAMESILO_KEY'),
                                             'domain': os.getenv('BASE_DOMAIN'),
                                             'record': record_id,
                                             'public_ip': current
                                         })

            # place the record_id in the url
            print(new_URL)

            # send request to URL
            print(requests.get(new_URL).content)
