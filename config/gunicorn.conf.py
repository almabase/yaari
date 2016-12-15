import multiprocessing

name = "yaari"
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1

debug = False
daemon = False

backlog = 1000
proc_name = "yaari"
tmp_upload_dir = "/tmp"


timeout = 30000
