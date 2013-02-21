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
    <h2>Other Files:</h2>
    <ul>
$OTHER_LIST
    </ul>
</body>
</html>
''')

path_to_link = lambda path : path.replace(os.environ['HOME']+'/public_html/', 'http://www.hep.wisc.edu/~mverzett/')

create_main_list_element = lambda  x: '        <li><a href="%s/">%s</a></li>\n' % (x, x)
create_pic_list_element  = lambda  x: \
    ('          <tr><td style="width: 640px;">%s</td></tr>\n' + \
     '          <tr><td style="width: 640px;"><A href=%s><IMG src="%s" width="640" align="center" border="0"></A></td></tr>\n' +\
     '          <tr><td style="width: 640px;" height="20"></td></tr>\n'   ) % (x, x, x)
create_file_list_element = lambda  x: '        <li><a href="%s">%s</a></li>\n' % (x, x)

