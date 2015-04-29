import os

host = os.environ['HOSTNAME']
public_html = ''
root_dir = ''
web_home = ''
#Site-dependent information
if 'wisc' in host:
    public_html = '/afs/hep.wisc.edu/home/%s/public_html/' % os.environ['USER']
    root_dir = 'public_html'
    web_home = 'http://www.hep.wisc.edu/~mverzett'
elif 'cern.ch' in host:
    initial = os.environ['USER'][0]
    public_html = '/afs/cern.ch/user/%s/%s/www/' % (initial, os.environ['USER'])
    root_dir = 'www'
    web_home = 'https://mverzett.web.cern.ch/mverzett'
elif 'fnal.gov' in host:
    public_html = os.path.join(os.environ['HOME'],'public_html')
    root_dir = 'public_html'
    web_home = 'http://home.fnal.gov/~%s' % os.environ['USER']
else:
    raise ValueError("Site %s not recongnised!" % host)

