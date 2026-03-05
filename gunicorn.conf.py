import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
loglevel = "info"
accesslog = "/var/log/gunicorn/meftp_access.log"
errorlog = "/var/log/gunicorn/meftp_error.log"