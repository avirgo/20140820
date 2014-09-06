import httplib
from xml.dom.minidom import parseString
import argparse
import ConfigParser
import sys

conf_parser = argparse.ArgumentParser(
        description=__doc__, # printed with -h/--help
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
conf_parser.add_argument("-c", "--conf_file",
                        help="Specify config file", metavar="FILE")
conf_parser.add_argument("org",
                        help="Specify 'org' section in config file", type=str, default="Defaults")

args, rem = conf_parser.parse_known_args()
if args.conf_file:
    config = ConfigParser.SafeConfigParser()
    config.read([args.conf_file])
    dict(config.items(args.org))
    defs = dict(config.items(args.org))
else:
    sys.exit(1)

print defs
parser = argparse.ArgumentParser( )
parser.set_defaults(**defs)
parser.add_argument("--basicauth")
parser.add_argument("--server")
z = parser.parse_args(rem)
print z.server
print z.basicauth


conn = httplib.HTTPSConnection(z.server)
bastr = "Basic {0}".format(str(z.basicauth))
print bastr
headers={"Authorization": "Basic {0}".format(str(z.basicauth)), "Accept": "application/*+xml;version=5.1"}
r0=conn.request("POST","/api/sessions",headers=headers)
r1=conn.getresponse()
print r1.status, r1.reason
d1=r1.read()
h1=r1.getheaders()
auheaders={}
for h in h1: 
  if h[0] == 'x-vcloud-authorization':
    #print h[1]
    auheaders={h[0]: h[1]}

auheaders['Accept'] = headers['Accept']

dom0 = parseString(d1)
for link in dom0.getElementsByTagName('Link'):
  if link.getAttribute('type') == 'application/vnd.vmware.vcloud.org+xml':
    orghref = link.getAttribute('href')
 
orgroot="/api/org/" + str(orghref.split('/')[-1])
c2=conn.request("GET",orgroot,headers=auheaders)
r2=conn.getresponse()
print orgroot, r2.status, r2.reason
d2=r2.read()
h2=r2.getheaders()
dom1 = parseString(d2)
for link in dom1.getElementsByTagName('Link'):
  if link.getAttribute('type') == 'application/vnd.vmware.vcloud.vdc+xml':
    vdchref = link.getAttribute('href')

vdcroot="/api/vdc/" + str(vdchref.split('/')[-1])
c3=conn.request("GET",vdcroot,headers=auheaders)
r3=conn.getresponse()
print vdcroot, r3.status, r3.reason
d3=r3.read()
h3=r3.getheaders()
dom2 = parseString(d3)
for link in dom2.getElementsByTagName('Link'):
  if link.getAttribute('rel') == 'edgeGateways':
    edgehref = link.getAttribute('href')

print edgehref
t3 = edgehref.split('/')[3:]
t3.insert(0, '')
edgeroot="/".join(t3)
c4=conn.request("GET",edgeroot,headers=auheaders)
r4=conn.getresponse()
print edgeroot, r4.status, r4.reason
d4=r4.read()
h4=r4.getheaders()
dom3 = parseString(d4)
print d4
ddom3 = dom3.firstChild
print ddom3.toxml()
ddom3 = ddom3.firstChild
print ddom3.toxml()
while ddom3:
  if ddom3.nodeName == 'EdgeGatewayRecord':
    print ddom3.toxml()
    print "#%s#\n" % (ddom3.nodeName)
    print ddom3.nodeValue
    break
  ddom3 = ddom3.nextSibling

edgegwhref = ddom3.getAttribute('href')
t4 = edgegwhref.split('/')[3:]
t4.insert(0,'')
edgegwroot = "/".join(t4)
c5 = conn.request("GET", edgegwroot,headers=auheaders)
r5 = conn.getresponse()
print edgeroot, r5.status, r5.reason
d5 = r5.read()
h5 = r5.getheaders()
dom5 = parseString(d5)
# print d5

print " ---- "
print " ---- "
print " ---- "

ddom5 = dom5.firstChild
print ddom5.toxml()
while ddom5:
  print ddom5.nodeName
  if ddom5.nodeName == 'Configuration':
#    print ddom5.toxml()
    break
  ddom5 = ddom5.nextSibling

print " ---- "
print " ---- "
print " ---- "

dd5a = ddom5
while dd5a:
  print dd5a.nodeName
  dd5a = dd5a.nextSibling
