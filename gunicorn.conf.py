import multiprocessing

bind = "127.0.0.1:8080"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = '-'
errorlog = '-'
loglevel = 'info'
preload_app = True
user = "www-data"
group = "www-data"
capture_output = True
proc_name = "hnhiring"
