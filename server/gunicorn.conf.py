import multiprocessing
import os

debug = True
loglevel = 'debug'
bind = '127.0.0.1:8001' # bind with nginx

if not os.path.exists("temp") or not os.path.exists("temp/logs"):
    os.mkdir("temp")
    os.mkdir("temp/logs")

pidfile = './temp/logs/gunicorn_pid.pid'
logfile = './temp/logs/gunicorn_log.log'

workers = 1 # multiprocessing.cpu_count() * 2 + 1
threads = 1 # 4 # worker threads
reload = True # reboot when the code change 