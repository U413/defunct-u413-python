#!/usr/bin/python

print "Content-type: text/plain"
print
try:
    import cgitb
    cgitb.enable()
    import cgi
    form=cgi.FieldStorage()

    print 'Code:',form['code'].value
except:pass
