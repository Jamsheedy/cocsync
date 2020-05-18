from time import gmtime, strftime

def get_time():
    return strftime("%a, %d %b %Y %H:%M:%S", gmtime())