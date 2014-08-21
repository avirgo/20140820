#############################################################################
#
# @author Copyright (c) 2010 - 2011 by Middleware Magic, All Rights Reserved.
#
#############################################################################

from java.io import FileInputStream
import java.lang
import os

propInputStream = FileInputStream("domains.properties")
configProps = Properties()
configProps.load(propInputStream)

adminUrl = configProps.get("server.url")
adminUser = configProps.get("admin.username")
adminPassword = configProps.get("admin.password")
monitoringServerName = configProps.get("monitoring.server.name")

executeThread_Vs_HoggerThreadRatio = configProps.get("ExecuteThread_Vs_HoggerThreadRatio")
checkTimes_Number = configProps.get("checkTimes_Number")
checkInterval_in_Milliseconds = configProps.get("checkInterval_in_Milliseconds")
threadDumpTimes_Number = configProps.get("threadDumpTimes_Number")
threadDumpInterval_in_Milliseconds = configProps.get("threadDumpInterval_in_Milliseconds")
sendEmail_ThreadDump_Counter = configProps.get("sendEmail_ThreadDump_Counter")

i = 0
y = int(checkTimes_Number)

#############  This method would send the Alert Email with Thread Dump  #################
def sendMailThreadDump():
	print '*********  ALERT MAIL HAS BEEN SENT  ***********'
	os.system("/bin/mailx -s  'ALERT: CHECK Thread Dumps as Hogger Thread Count Exceeded the Limit' anthony.virgo@pearson.com < All_ThreadDump.txt &")
	print '*********  ALERT MAIL HAS BEEN SENT  ***********'
	print ''

#############  This method is checking the Hogger Threads Ratio  #################
def alertHoggerThreads(executeTTC , hoggerTC):
	print 'Execute Threads : ', executeTTC
	print 'Hogger Thread Count : ', hoggerTC
	print 'executeThread_Vs_HoggerThreadRatio :', executeThread_Vs_HoggerThreadRatio
	if hoggerTC != 0:
		ratio=(executeTTC/hoggerTC)
		print 'Ratio : ' , ratio
		if (int(ratio) <= int(executeThread_Vs_HoggerThreadRatio)):
			print ' !!!! ALERT !!!! Stuck Threads are on its way.....'
			print ''
			message =  'ExecuteThreads Count= ' + str(executeTTC) + '   HoggingThreads= '+ str(hoggerTC) +'   ExecuteThreads/HoggingThreads Ratio= '+ str(ratio)
			cmd = "echo " + message +" > rw_file"
			os.system(cmd)
			genrateThreadDump()
		else:
			print '++++++++++++++++++++++++++'
			print 'Everything is working fine'
			print '++++++++++++++++++++++++++'
	else:
		print '++++++++++++++++++++++++++'
		print 'Everything is working fine'
		print '++++++++++++++++++++++++++'

#############  This method is Taking the Thread Dumps #################
def genrateThreadDump():
	b = int(sendEmail_ThreadDump_Counter)
	a = 0
	p = 0
	q = int(threadDumpTimes_Number)
        serverCur=pwd()
	serverConfig()
	cd ('Servers/'+ monitoringServerName)
	while (p < q):
		if a < b:
			print 'Taking Thread Dump : ', p
			threadDump()
			cmd = "cat Thread_Dump_" + str(monitoringServerName) + ".txt >> All_ThreadDump.txt"
			os.system(cmd)
			print 'Thread Dump Collected : ', p ,' now Sleeping for ', int(threadDumpInterval_in_Milliseconds) , ' Seconds ...'
			print ''
			Thread.sleep(int(checkInterval_in_Milliseconds))
			print 'done sleeping'
			b = b - 1
		p = p + 1
		print a,b,p,q
	sendMailThreadDump()
	cmd = "rm -f All_ThreadDump.txt"
	os.system(cmd)
	serverRuntime()
        cd(serverCur)
 
def getRunningServerNames():
    domainConfig()
    return cmo.getServers()

connect(adminUser,adminPassword,adminUrl)
urldict={}
outstr={}
serverlist=getRunningServerNames()
for svr in serverlist:
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
        print pwd()
        alertHoggerThreads(totalThreads, hoggingThreads)
        print pwd()
	ECODE="\t"
        pstr=x+": "
        outstr[x]=(pstr+ ((status.split(','))[1]).split(':')[1] + ((status.split(','))[3]).split(':')[1]  +ECODE
            +'Tott: ' + str(totalThreads)+ECODE
            +'Idlt: ' + str(idleThrds)+ECODE
            +'Hogt: ' + str(hoggingThreads)+ECODE
            +'Pend: ' + str(pending)+ECODE
            +'OpnScks: ' + str(openSocks)+ECODE
            +'SThrpt: ' +str(thruput)+ECODE)
   except:
        print 'Exception... Unable to connect to given Server', x
        pass

for x in outstr:
   print outstr[x]

