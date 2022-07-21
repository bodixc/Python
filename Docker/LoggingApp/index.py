from yaml import safe_load
from datetime import datetime
from time import sleep
import os

config_file = "config/config.yaml"
log_file = "logs/write.log"
user = os.popen('echo $user').read()

def CheckConfig(delay):
    try:
        config = safe_load(open(config_file))
    except:
        raise FileNotFoundError('No such config file!')
    try:
        delay = config['delayInSec']
    except:
        raise ValueError('Not found this parameter')
    if ((type(delay) != int) & (type(delay) != float)):
        raise TypeError('Parameter delayInSec in config.yaml isn\'t int or float type!')
    return delay
 
delay = CheckConfig(None)

def WriteLog(msg: str):
    f = open(log_file, 'a')
    f.writelines(msg)
    f.close()

WriteLog(f"\n\tDelay: {delay} sec\n")
os.system(f"echo '\tDelay: {delay} sec'")

while True:
    old_delay = delay
    delay = CheckConfig(None)
    if delay != old_delay:
        delay_msg = f"\n\tDelay: {delay} sec"
        WriteLog('\t' + delay_msg + '\n')
        os.system(f"echo '{delay_msg}'")
    date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    log_msg = f'[{date}] Hi {user}'
    WriteLog(log_msg)
    os.system('echo -n "."')
    sleep(delay)
