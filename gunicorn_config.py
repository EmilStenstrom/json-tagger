import os


bind = "0.0.0.0:%s" % os.environ.get("PORT", "8000")
accesslog = '-'
access_log_format = \
    "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s [%(D)s μs]"
