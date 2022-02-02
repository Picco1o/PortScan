import os
import sys
import time
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

parser = argparse.ArgumentParser(description='some args')
parser.add_argument('-i', '--ip', required=True, help='ip')
parser.add_argument('-p', '--port', required=True, help='port, eg: 80 or 80,443,8080,8443 or 80-1000')
parser.add_argument('-t', '--thread', help='scan threads', default=5, type=int)
args = parser.parse_args()
ip = args.ip
port = args.port
executor = ThreadPoolExecutor(max_workers=args.thread)
# socket default timeout 
socket.setdefaulttimeout(1)

def scan(ip, port, log):
    # default IPv4 TCP
    # socket.AF_INET6 IPv6 socket.SOCK_DGRAM UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        res = s.connect_ex((ip, int(port)))
        if res == 0:
            print(ip + ':' + str(port) + ' OPEN')
            log.write(ip + ':' + str(port) + ' OPEN\n')
        else:
            print(ip + ':' + str(port) + ' CLOSE')
            log.write(ip + ':' + str(port) + ' CLOSE\n')
    except socket.gaierror:
        print(ip + ':' + str(port) + ' ADDERSS ERROR')
        log.write(ip + ':' + str(port) + ' ADDERSS ERROR\n')
    finally:
        s.close()

def all_task(ip, start, end, log):
    for i in range(start, end + 1):
        task = executor.submit(scan, ip, i, log)
        yield task

def start(ip, port):
    start_time = time.time()
    log = open("{}/{}.txt".format('result', time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())), 'a+')
    if ',' in port:
        for future in as_completed([executor.submit(scan, ip, int(i), log) for i in port.split(',')]):
            future.result()
    elif '-' in port:
        start = int(port.split('-')[0])
        end = int(port.split('-')[-1])
        if start > end:
            print('PORT ERROR !')
            sys.exit()
        for future in as_completed(all_task(ip, start, end, log)):
            future.result()
    else:
        scan(ip, port, log)
    print('use time：{:.2f}s'.format(time.time()-start_time))
    log.write('use time：{:.2f}s'.format(time.time()-start_time))
    log.close()

def main():
    if not os.path.exists('result'):
        os.mkdir('result')
    start(ip, port)

if __name__ == '__main__':
    main()
