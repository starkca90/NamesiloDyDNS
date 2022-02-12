# NamesiloDyDNS
Dynamic DNS for Namesilo

## Requirements:
Create the following system environment variables:

| Key          | Description                                     | Example                            |
|--------------|-------------------------------------------------|------------------------------------|
| NAMESILO_KEY | API Key from api-manager                        | xyz123                             |
| BASE_DOMAIN  | The domain being requested                      | caseystark.com                     |
| A_RECORDS    | Space seperated list of A records to be updated | test.caseystark.com caseystark.com |

## Tested With
Tested with Python 3.9.10
