import subprocess
import argparse
from datetime import datetime
import requests, json, random, time

address = "127.0.0.1:5000"

parser = argparse.ArgumentParser(description='Display WLAN signal strength.')
parser.add_argument(dest='interface', nargs='?', default='wlp0s20f3',
                    help='wlan interface (default: wlp0s20f3)')
args = parser.parse_args()


def rand_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )

while True:
    cmd = subprocess.Popen('iwconfig %s' % args.interface, shell=True,
                           stdout=subprocess.PIPE)                
    for line in cmd.stdout:
        line = line.decode("utf-8")
        if 'Link Quality' in line:
            start = line.rfind('=')
            level = line[start+1:start+4]   
        elif 'Access Point:' in line:
            mac = line[line.index('Access Point:') + len('Access Point:')+1:]
            mac = mac[:17]
        elif 'Not-Associated' in line:
            print ('No signal')
    rand = random.randint(0, 3)
    if rand == 3:
        mac = rand_mac().upper()
        level = random.randint(-70, -30)
    data = {'mac':mac, 'level':level, 'time':str(datetime.now())} 
    headers = {'Content-Type': 'application/json'}
    print(data)
    url_post = 'http://{}/api/bledata/upload'.format(address)
    response = requests.post(url_post, headers=headers, json=data)
    print(f"RESPONSE STATUS: {response.status_code}")

    time.sleep(1)