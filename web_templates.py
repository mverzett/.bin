import os
from string import Template

page_template = Template('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <title>$PATH</title>
</head>
<body class="index">
  <div id="header">
    <A href="http://www.hep.wisc.edu/~mverzett/">Home</A>  <A href="http://www.hep.wisc.edu/~mverzett/$PARENT">Parent Dir</A>
  </div>
  <hr>
  <div id="title">
    <h1>$PATH Content</h1>
  </div>
  <hr>
    <h2>Directories:</h2>
    <ul>
$DIR_LIST
    </ul>
    <h2>Pics:</h2>
    <table style="text-align: left; " border="1" cellpadding="2" cellspacing="1">
      <tbody>
$PIC_LIST
      </tbody>
    </table>
    <h2>Tables:</h2>
$TABLES
    <h2>Other Files:</h2>
    <ul>
$OTHER_LIST
    </ul>
</body>
</html>
''')

path_to_link = lambda path : path.replace(os.environ['HOME']+'/public_html/', 'http://www.hep.wisc.edu/~mverzett/')

create_main_list_element = lambda  x: '        <li><a href="%s/">%s</a></li>\n' % (x, x)
def create_pic_list_element(*args, **kwargs):
    size = str(kwargs['size']) if 'size' in kwargs else '640'
    wraps      = '          <tr>%s</tr>\n'
    first_line = ( ('<td style="width: '+size+'px;">%s</td>')*len(args) ) % args
    first_line = wraps % first_line

    second_line = ''.join([('<td style="width: '+size+'px;"><A href=%s><IMG src="%s" width="'+size+'" align="center" border="0"></A></td>') % ( arg, arg ) for arg in args])
    second_line = wraps % second_line

    third_line = ('<td style="width: '+size+'px;" height="20"></td>')*len(args)
    third_line = wraps % third_line
    return ''.join([first_line, second_line, third_line])

create_file_list_element = lambda  x: '        <li><a href="%s">%s</a></li>\n' % (x, x)
create_tab_list_element  = lambda  name, content: \
    ('        <h3><a href="%s">%s</a></h3>\n' % (name,name.split('.')[0]) + \
     '        <pre>\n' +\
     content +\
     '        </pre>\n')
