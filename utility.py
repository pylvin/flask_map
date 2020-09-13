
import math
from flask import flash

# Simple Pagination
class Paginate():
    def __init__(self,query,page,per_page):
        self.query = query
        self.page = page
        self.per_page = per_page
    def paginate(self):
        if self.page == 1:
            return self.query[:self.per_page]
        else:
            count = self.per_page*self.page
            return self.query[count-self.per_page:count]

    def has_next(self):
        count = self.per_page * (self.page+1)
        return len(self.query[count:]) !=0

    def pages_count(self):
        return math.ceil(len(self.query) / self.per_page)

def flash_errors(form):
    for k in form.errors:
        msg = ""
        for i in form.errors[k]:
            msg = msg.join(f' {i} ')
        flash(f'{k}{msg}')

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

