import sys
import requests

def find_email_addresses(domain):
    #declare a set to avoid duplicates
    domains = set()
    api_key='edd5e17abdd4f38ee9e623d7bc6b036c52c4b5d2'
    resp = requests.get('https://api.emailhunter.co/v1/search?domain='+domain
        +'&api_key='+api_key);
    if resp.status_code != 200:
        raise ApiError('GET for domain failed')
    for item in resp.json()["emails"]:
        domains.add(item["value"])
    for i in domains:
        print(i)




#run as command line application
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide a domain only")
    else:
        find_email_addresses(sys.argv[1])