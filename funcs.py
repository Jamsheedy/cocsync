from time import localtime, strftime

def get_time():
    return strftime("%a, %d %b %Y %H:%M:%S", localtime())

def simple_time():
    return strftime("%m/%d/%Y %I:%M %p", localtime()) + ' EST'

