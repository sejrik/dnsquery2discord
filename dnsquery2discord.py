import requests
import time
import re

WEBHOOK_URL = 'https://discord.com/api/webhooks/'  
LOG_FILE = '/var/log/named/named.log'

def tail_log(file_path, delay=1.0):
    with open(file_path, 'r') as f:
        
        f.seek(0, 2)

        while True:
            line = f.readline()
            if not line:
                time.sleep(delay)
                continue

            
            match = re.search(r'client @\S+ (\S+)#.*\((\S+)\): query:', line)
            if not match:
                continue
            ip_address = match.group(1)
            requested_dns = match.group(2)

            
            message = f'```IP address {ip_address} requested DNS {requested_dns}```'
            payload = {'content': message}
            requests.post(WEBHOOK_URL, json=payload)

if __name__ == '__main__':
    tail_log(LOG_FILE)
