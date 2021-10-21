#! /usr/bin/python3

import time
import os
import sys
import requests as rq
import discordConfig
import json

# Access token (defined in discordConfig.py)
TOKEN = discordConfig.TOKEN
# Text channel ID
CH = discordConfig.CH

# Get global IP address
def get_ip():
    req = rq.get('http://inet-ip.info/ip')
    print(req.text)
    return req.text

# Send message to Discord server
def notify(addr):
    msg = "Global IP address has been changed.\n"
    msg += f"New IP address is {addr} ."

    header ={
        'authorization':f'Bot {TOKEN}',
        'content-type':'application/json'
    } 
    
    payload = {'content': msg}
    payload = json.dumps(payload)
    print(payload)
    print(header)

    url = f'https://discordapp.com/api/channels/{CH}/messages'

    rq.post(url, data=payload, headers=header)

# Check IP address once a minute
# If IP addr has been changed, send new addr to Discord
def main_routine():
    while True:
        try:
            # Get current IP address from the online service
            current_IP = get_ip()
            # Check already fetched IP address
            with open('./ipv4_addr', 'r') as f:
                old_IP = f.read()
            
            if current_IP != old_IP:
                # Update IP addr file
                with open('./ipv4_addr', 'w')as f:
                    f.write(current_IP)
                # Send new IP address to Discord server
                notify(current_IP)

        finally:
            time.sleep(600)

# Run this program as linux daemon
def daemonize():
    # FORK
    pid = os.fork()

    # In parent process
    if pid > 0:
        # Write child process's pid to file
        with open('/var/run/ipnotify.pid', 'w') as f:
            f.write(str(pid) + '\n')
            sys.exit()

    # In child process
    elif pid == 0:
        main_routine()

if __name__ == '__main__':
    while True:
        daemonize()
