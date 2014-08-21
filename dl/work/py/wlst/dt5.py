#############################################################################
#
# @author Copyright (c) 2010 - 2011 by Middleware Magic, All Rights Reserved.
#
#############################################################################

from java.io import FileInputStream
import java.lang
import os
import sys

propInputStream = FileInputStream("domains.properties")
configProps = Properties()
configProps.load(propInputStream)

adminUrl = configProps.get("server.url")
adminUser = configProps.get("admin.username")
adminPassword = configProps.get("admin.password")
srchServerName = configProps.get("monitoring.server.name")
print 'number of args', len(sys.argv)
if len(sys.argv) > 1:
    srchServerName = sys.argv[1]

executeThread_Vs_HoggerThreadRatio = configProps.get("ExecuteThread_Vs_HoggerThreadRatio")
checkTimes_Number = configProps.get("checkTimes_Number")
checkInterval_in_Milliseconds = configProps.get("checkInterval_in_Milliseconds")
threadDumpTimes_Number = configProps.get("threadDumpTimes_Number")
threadDumpInterval_in_Milliseconds = configProps.get("threadDumpInterval_in_Milliseconds")
sendEmail_ThreadDump_Counter = configProps.get("sendEmail_ThreadDump_Counter")

i = 0
y = int(checkTimes_Number)
 
#############  This method is Taking the Thread Dumps and counting the unique stuck ones#################
def getStuckCount():
        serverCur=pwd()
	serverConfig()
	cd ('Servers/'+ monitoringServerName)
	print 'Taking Thread Dump : ', monitoringServerName
	redirect('/dev/null', 'false')
	zed = threadDump()
	redirect('/dev/null', 'true')
	cmd = "grep STUCK Thread_Dump_" + str(monitoringServerName) + ".txt |sort -u|wc -l"
	sc = os.popen(cmd)
	stuck_count = sc.readline()
	sc.close()
	cmd = "rm -f Thread_Dump_" + str(monitoringServerName) + ".txt"
	os.system(cmd)
	serverRuntime()
        cd(serverCur)
	return stuck_count
def getRunningServerNames():
    domainConfig()
    return cmo.getServers()

connect(adminUser,adminPassword,adminUrl)
urldict={}
outstr={}
serverlist=getRunningServerNames()
for svr in serverlist:
   sstr = svr.getName()
   if sstr.find(srchServerName) > -1:
      cd("/Servers/"+svr.getName())
      urldict[svr.getName()]='t3://'+get('ListenAddress')+':'+str(get('ListenPort'))

for x in urldict:
   if x == 'AdminServer':
      continue
   print urldict[x]
   try:
        connect(adminUser, adminPassword, urldict[x])
        serverRuntime()
        openSocks = cmo.getOpenSocketsCurrentCount();
        cd('serverRuntime:/ThreadPoolRuntime/ThreadPoolRuntime/')
        compReq = cmo.getCompletedRequestCount()
        status = str(cmo.getHealthState())
        hoggingThreads = cmo.getHoggingThreadCount()
        totalThreads = cmo.getExecuteThreadTotalCount()
        idleThrds = cmo.getExecuteThreadIdleCount()
        pending = cmo.getPendingUserRequestCount()
        qLen = cmo.getQueueLength()
        thruput = cmo.getThroughput()
        monitoringServerName = x
	stuck_count = getStuckCount()
        pstr=('%s: %s %s ' % (x, ((status.split(','))[1]).split(':')[1], ((status.split(','))[3]).split(':')[1]))
        outstr[x]=(pstr
            +'Tot: %d, ' % totalThreads
            +'Idl: %d, ' % idleThrds
            +'STUCK: %d, ' % stuck_count
            +'Hog: %d, ' % hoggingThreads
            +'Pen: %d, ' % pending
            +'OScks: %d, ' % openSocks
            +'SThrpt: %0.3f' % thruput)
   except:
        print 'Exception... Unable to connect to given Server', x
        pass

for x in outstr:
   print outstr[x]

