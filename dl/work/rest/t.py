import httplib
from xml.dom.minidom import getDOMImplementation, parseString

conn = httplib.HTTPSConnection("lo3-mystack.pearson.com")
headers={"Authorization": "Basic YW50aG9ueS52aXJnb0BwZWFyc29uLmNvbUB1a2Ntcy1wb2M6VG9ueV9WaXJnMDI=", "Accept": "application/*+xml;version=5.1"}
r0=conn.request("POST","/api/sessions",headers=headers)
r1=conn.getresponse()
print r1.status, r1.reason
d1=r1.read()
h1=r1.getheaders()
print d1
#print h1['x-vcloud-authorization']
print h1
auheaders={}
for h in h1: 
  if h[0] == 'x-vcloud-authorization':
    print h[1]
    auheaders={h[0]: h[1]}

auheaders['Accept'] = headers['Accept']

print auheaders
dom0 = parseString(d1)

