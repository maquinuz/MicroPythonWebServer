# Content Callback functions.
# They should receive parameters and return a HTML formatted string
# By convention they start with cb_

import ujson
import gc
import time
from main import get_config, set_config

def cb_status():
    try:
        config = get_config()
    except:
        return '<h2>No Status</h2>'

    content  = '<h2>Status %s</h2>' % config['chipid']
    content += '<p>MacAddress %s' % config['macaddr']
    content += '<p>Address %s' % config['address']
    content += '<p>Free Memory %d (alloc %d)</div>' % (gc.mem_free(), gc.mem_alloc())
    return content

def cb_setplace(place):
    try:
        config = get_config()
    except:
        config = {}

    config['place'] = place
    set_config(config)

def cb_setwifi(ssid, pwd):
    if len(ssid) < 3 or len(pwd) < 8:
        return '<h2>WiFi too short: not set</h2>'
    try:
        config = get_config()
    except:
        config = {}

    config['ssid'] = ssid
    config['pwd'] = pwd
    set_config(config)

def cb_temperature(pin):
    #from ds18b20 import readtemp
    #temp, count, sensor = readtemp()
    temp, count, sensor = ['','','']
    content  = '<h1><a href="/">' + title + ': ' +temp+ 'C</a></h1>'
    content += '<p>Reading #' + count + ' @ ' + sensor
    content += '</p></div>'
    return content

def cb_temperature_json(pin):
    #from ds18b20 import readtemp
    #temp, count, sensor = readtemp()
    try:
        config = get_config()
    except:
        config['address'] = ''
        config['macaddr'] = ''
    print('CONFIG ', config)

    temp, count, sensor = ['','','']
    temptable = {}
    temptable["temp"] = temp
    temptable["mac"] = config['macaddr']
    temptable["server"] = config['address']
    temptable["count"] = str(count)
    temptable["date"] = time.time()
    return ujson.dumps(temptable)

def httpheader(code, extension, title, refresh):
   codes = {'200':" OK", '400':" Bad Request", '404':" Not Found", '302':" Redirect"}
   try:
       HTTPStatusString = code + codes[code]
   except:
       HTTPStatusString = "501 Internal Server Error"

   # A few MIME types. Keep list short. If you need something that is missing, let's add it.
   mt = {'html': "text/html", 'json': "application/json" }
   try:
       MimeType = mt[extension]
   except:
       MimeType = "text/plain"

   header = "HTTP/1.1 " + HTTPStatusString + "\r\nServer: tempserver\r\nContent-Type: " + MimeType + "\r\nCache-Control: private, no-store\r\n" + "Connection: close\r\n\r\n"
   if extension == 'html' :
       header += '<!DOCTYPE html>\n'
       header += '<html lang="en">\n<head>\n<title>Temp ' + title + '</title>\n'
       header += refresh
       header += '<meta name="generator" content="esp8266-server">\n<meta charset="UTF-8">\n'
       header += '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
       header += '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>\n'
       header += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">\n'
       header += '<style media="screen" type="text/css">\n'
       header += 'body {font-family: Georgia,serif;}\n.jumbotron {padding:10px 10px;}\n</style>\n'
       header += '</head>\n<body>\n'
       header += '<div class="container-fluid">\n<div class="jumbotron">\n'
   return header

def httpfooter():
    footer  = '</div>'
    footer += '<footer class="footer"><div class="container">'
    footer += '<a href="/">[ index</a> | '
    footer += '<a href="/j">json </a> | '
    footer += '<a href="/setname/?name=myplace">set place</a> | '
    footer += '<a href="/setwifi/?ssid=myssid&pwd=mypass">set wifi</a> | '
    footer += '<a href="/status">status</a> | '
    footer += '<a href="/reinit">reinit</a> | '
    footer += '<a href="/help">help</a>]'
    footer += '</div></footer>'
    footer += '</body></html>'
    return footer
