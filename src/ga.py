'''
Created on Dec 7, 2012

@author: bary
'''

import gdata.gauth
import httplib2
import datetime
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OOB_CALLBACK_URN
from oauth2client.file import Storage
from oauth2client.tools import run
from gdata.service import Query
import json
import numpy as np
import csv
import math
import random
import scipy.spatial.distance as spsd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier as rf
from matplotlib import mpl,pyplot

class GAconnector:
    '''
    classdocs
    '''

    def __init__(self,CLIENT_SECRETS,SCOPE,TOKEN_FILE_NAME):
        '''
        Constructor
        '''

        # A helpful message to display if the CLIENT_SECRETS file is missing.
        MISSING_CLIENT_SECRETS_MESSAGE = 'Client Secrets file is missing'

        # The Flow object to be used if we need to authenticate.
        FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
        scope=SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE)
        
        #redirect_uri=OOB_CALLBACK_URN
        
        # 1. Create an http object
        http = httplib2.Http()

        # 2. Authorize the http object
        # In this tutorial we first try to retrieve stored credentials. If
        # none are found then run the Auth Flow. This is handled by the
        # prepare_credentials() function defined earlier in the tutorial
        credentials = self.prepare_credentials(TOKEN_FILE_NAME,FLOW)  #FIX
        http = credentials.authorize(http)  # authorize the http object

        # 3. Build the Analytics Service Object with the authorized http object
        self.service = build('analytics', 'v3', http=http)
        #print self.service
        #print self.service.data()
        #print self.service.data().ga()
        
        #Check
        
        #self.profile_id=self.get_specified_webproperty_id(webpropertyid)
        
        #self.get_specified_webproperty_id(webpropertyid)
        
        self.webproperties_list =self.service.management().webproperties().list(accountId='~all').execute()
        print self.webproperties_list
        
    def prepare_credentials(self,TOKEN_FILE_NAME,FLOW):
        # Retrieve existing credendials
        storage = Storage(TOKEN_FILE_NAME)
        credentials = storage.get()

        # If existing credentials are invalid and Run Auth flow
        # the run method will store any new credentials
        if credentials is None or credentials.invalid:
            credentials = run(FLOW, storage) #run Auth Flow and store credentials

        return credentials
    
    def get_first_profile_id(self):
        accounts = self.service.management().accounts().list().execute()

        if accounts.get('items'):
            firstAccountId = accounts.get('items')[0].get('id')
            webproperties = self.service.management().webproperties().list(accountId=firstAccountId).execute()

            if webproperties.get('items'):
                firstWebpropertyId = webproperties.get('items')[0].get('id')
                profiles = self.service.management().profiles().list(
                                                        accountId=firstAccountId,
                                                        webPropertyId=firstWebpropertyId).execute()

                if profiles.get('items'):
                    return profiles.get('items')[0].get('id')

        return None
    
    #Modify
    def get_specified_webproperty_id(self,webpropertyid):
        accounts = self.service.management().accounts().list().execute()

        if accounts.get('items'):
            firstAccountId = accounts.get('items')[0].get('id')
            webproperties = self.service.management().webproperties().list(accountId=firstAccountId).execute()

            if webproperties.get('items'):
                firstWebpropertyId = webproperties.get('items')[webpropertyid].get('id')
                profiles = self.service.management().profiles().list(
                                                        accountId=firstAccountId,
                                                        webPropertyId=firstWebpropertyId).execute()

                if profiles.get('items'):
                    self.profile_id=profiles.get('items')[0].get('id')

        #return None
    
    def get_top_keywords(self):
        """Executes and returns data from the Core Reporting API.

        This queries the API for the top 25 organic search terms by visits.

      Args:
        service: The service object built by the Google API Python client library.
        profile_id: String The profile ID from which to retrieve analytics data.

      Returns:
        The response returned from the Core Reporting API.
      """
        return self.service.data().ga().get(
                ids='ga:' + self.profile_id,
                start_date='2013-01-26',
                end_date='2013-02-25',
                metrics='ga:visits',
                dimensions='ga:source',
                sort='-ga:visits',
                filters='ga:medium==organic',
                start_index='1',
                max_results='25').execute()
                
    def getuniquevisitorsbyregion(self):
        return self.service.data().ga().get(
                ids='ga:' + self.profile_id,
                start_date='2013-01-26',
                end_date='2013-02-25',
                metrics='ga:visits',
                dimensions='ga:region,ga:pagePath',
                sort='-ga:visits',
                start_index='1',
                max_results='10000').execute()
                
    def getuniquevisitorsforchanneloverperiod(self,startdate,enddate,channel):
        return self.service.data().ga().get(
                ids='ga:' + self.profile_id,
                start_date=startdate,
                end_date=enddate,
                metrics='ga:newVisits',
                dimensions='ga:country,ga:pagePath',
                sort='-ga:newVisits',
                start_index='1',
                filters='ga:pagePath=~'+channel,
                max_results='10000').execute()
                
    def gettotalvisitorsforchanneloverperiod(self,startdate,enddate,channel):
        return self.service.data().ga().get(
                ids='ga:' + self.profile_id,
                start_date=startdate,
                end_date=enddate,
                metrics='ga:visitors',
                dimensions='ga:country,ga:pagePath',
                sort='-ga:visitors',
                start_index='1',
                filters='ga:pagePath=~'+channel,
                max_results='10000').execute()
    
    #Same as above, but filtering by a country            
    def gettotalvisitorsforchanneloverperiodincountry(self,startdate,enddate,channel,country):
        return self.service.data().ga().get(
                ids='ga:' + self.profile_id,
                start_date=startdate,
                end_date=enddate,
                metrics='ga:visitors',
                dimensions='ga:country,ga:pagePath',
                sort='-ga:visitors',
                start_index='1',
                filters='ga:pagePath=~'+channel+';ga:country=='+country,
                max_results='10000').execute()
                
    def getuniquevisitorsforchannelbyhourofday(self,region,startdate,enddate,channel,weekday):
        return self.service.data().ga().get(
                ids='ga:' + self.profile_id,
                start_date=startdate,
                end_date=enddate,
                metrics='ga:newVisits',
                dimensions='ga:country,ga:hour',
                sort='-ga:newVisits',
                start_index='1',
                filters='ga:dayOfWeek=='+str(weekday)+';ga:pagePath=~'+channel+';ga:country=='+region+';ga:pagePath!@clips;ga:pagePath!@on_demand',
                max_results='10000').execute()
    
    def gettotalvisitorsforchannelbyhourofday(self,region,startdate,enddate,channel,weekday):
        return self.service.data().ga().get(
                ids='ga:' + self.profile_id,
                start_date=startdate,
                end_date=enddate,
                metrics='ga:visitors',
                dimensions='ga:date,ga:hour',
                sort='ga:date',
                start_index='1',
                filters='ga:dayOfWeek=='+str(weekday)+';ga:pagePath=~'+str(channel)+';ga:country=='+str(region)+';ga:pagePath!@clips;ga:pagePath!@on_demand',
                max_results='10000').execute()
        
class GADataExtractor:
    #Note: Added webpropertyid
    def __init__(self,CLIENT_SECRETS,SCOPE,TOKEN_FILE_NAME):
        self.gac=GAconnector(CLIENT_SECRETS,SCOPE,TOKEN_FILE_NAME)
        self.regionvisits=[]
        
    def querybytimeslot(self,webpropertyid,startdate,enddate,channel):
        startdate=startdate.split('-')
        enddate=enddate.split('-')
        startdate=datetime.datetime(int(startdate[0]),int(startdate[1]),int(startdate[2]))
        enddate=datetime.datetime(int(enddate[0]),int(enddate[1]),int(enddate[2]))
        timeperiod=(enddate-startdate).days
        self.gac.get_specified_webproperty_id(webpropertyid)
        for x in xrange(timeperiod):
            intermediatestartdate=startdate+datetime.timedelta(x)
            intermediateenddate=startdate+datetime.timedelta(x+1)
            
            #Multiple versions of the query:
            #qr=self.gac.getuniquevisitorsforchanneloverperiod(str(intermediatestartdate)[0:10],str(intermediateenddate)[0:10], channel)
            qr=self.gac.gettotalvisitorsforchanneloverperiod(str(intermediatestartdate)[0:10],str(intermediateenddate)[0:10], channel)
            #qr=self.gac.getuniquevisitorsforchannelbyhourofday(str(intermediatestartdate)[0:10],str(intermediateenddate)[0:10], channel)
            #qr=self.gac.gettotalvisitorsforchanneloverbyhourofday(str(intermediatestartdate)[0:10],str(intermediateenddate)[0:10], channel)
            
            self.getregioncounts(qr)
    
    #Same as above but only retrieving for a specific country        
    def querybytimeslotforcountry(self,webpropertyid,startdate,enddate,channel,country):
        startdate=startdate.split('-')
        enddate=enddate.split('-')
        startdate=datetime.datetime(int(startdate[0]),int(startdate[1]),int(startdate[2]))
        enddate=datetime.datetime(int(enddate[0]),int(enddate[1]),int(enddate[2]))
        timeperiod=(enddate-startdate).days
        self.gac.get_specified_webproperty_id(webpropertyid)
        '''
        for x in xrange(timeperiod):
            intermediatestartdate=startdate+datetime.timedelta(x)
            intermediateenddate=startdate+datetime.timedelta(x+1)
            
            #Multiple versions of the query:
            #qr=self.gac.getuniquevisitorsforchanneloverperiod(str(intermediatestartdate)[0:10],str(intermediateenddate)[0:10], channel)
            qr=self.gac.gettotalvisitorsforchanneloverperiodincountry(str(intermediatestartdate)[0:10],str(intermediateenddate)[0:10], channel,country)
            #qr=self.gac.getuniquevisitorsforchannelbyhourofday(str(intermediatestartdate)[0:10],str(intermediateenddate)[0:10], channel)
            #qr=self.gac.gettotalvisitorsforchanneloverbyhourofday(str(intermediatestartdate)[0:10],str(intermediateenddate)[0:10], channel)
            
            self.getregioncounts(qr)
        '''
        
    def getregioncounts(self,queryresult):
        regionvisitsmap={}
        for r in queryresult['rows']:
            if r[0] in regionvisitsmap:
                regionvisitsmap[r[0]]=regionvisitsmap[r[0]]+int(r[2])
            else:
                regionvisitsmap[r[0]]=int(r[2])
        self.regionvisits.append(regionvisitsmap)
        
    #Get vector of number of visitors (unique or total) for region depending on time window split
    def getregionvectors(self):
        regiontovectormap={}
        for index in xrange(len(self.regionvisits)):
            regioncountmap=self.regionvisits[index]
            for region in regioncountmap:
                regionvector=[]
                if region in regiontovectormap:
                    continue
                regionvector.append(regioncountmap[region])
                for index2 in xrange(len(self.regionvisits)):
                    if index2 == index:
                        continue
                    if region in self.regionvisits[index2]:
                        regionvector.append(self.regionvisits[index2][region])
                    else:
                        regionvector.append(0)
                regiontovectormap[region]=regionvector
        return regiontovectormap
    
    #Get top N regions by mean number of visitors (unique or total)
    def gettopNregionsbymean(self,N,regiontovectormap):
        topregions=[]
        taken={}
        for x in xrange(N):
            maximum=0
            for region in regiontovectormap:
                if np.mean(regiontovectormap[region]) > maximum and region not in taken:
                    maximum=np.mean(regiontovectormap[region])
                    topregion=region
            taken[topregion]=0
            topregions.append(topregion)
        return topregions
        
    #Determine nature of distribution for regions in terms of deviation from the mean
    def characterizeregionsbythresholdsigma(self,regiontovectormap,topregions,threshold):
        regionsabove=[]
        regionsbelow=[]
        for region in topregions:
            rv=regiontovectormap[region]
            mu=np.mean(rv)
            sigma=np.std(rv)
            if float(sigma/mu) >= threshold:
                regionsabove.append(region)
            else:
                regionsbelow.append(region)
        return regionsabove,regionsbelow
    
    #Retrieve and characterize statistics for each region based on time of day and day of week (Note:Passed webproperty_id)
    def gettimeofdaycharacterizationbyregiontotalvisitors(self,startdate,enddate,channel,topregions):
        weekdaymapslist=[]
        weekdaystatsmapslist=[]
        #self.gac.get_specified_webproperty_id(webpropertyid)
        for region in topregions:
            #To create map of maps, weekday: hourofday to counts map
            weekdaymap={}
            for x in xrange(7):
                weekdaymap[x]={}
            for weekday in xrange(7):
                self.qr=self.gac.gettotalvisitorsforchannelbyhourofday(region,startdate,enddate,channel,weekday)
                #self.qr=self.gac.getuniquevisitorsforchannelbyhourofday(region,startdate,enddate,channel,weekday)
                #New; for fixing missing values
                print self.qr['rows'][0]
                print len(self.qr['rows'])
                print '----------------'
                #Necessary to deal with missing entries
                hoursfoundfordate={}
                previousdate=self.qr['rows'][0][1]
                for result in self.qr['rows']:
                    date=result[1]
                    hour=int(result[2])
                    if date==previousdate:
                        hoursfoundfordate[hour]=0
                    else:
                        for h in xrange(24):
                            if h not in hoursfoundfordate:
                                if h in weekdaymap[weekday]:
                                    weekdaymap[weekday][h].append(0)
                                else:
                                    weekdaymap[weekday][h]=[0]
                        hoursfoundfordate={}
                        previousdate=date
                                   
                    if weekday in weekdaymap:
                        if hour in weekdaymap[weekday]:
                            weekdaymap[weekday][hour].append(int(result[2]))
                        else:
                            weekdaymap[weekday][hour]=[int(result[2])]
    
            weekdaymapslist.append((region,weekdaymap))
            #Get statistics for time of day for each day
            weekdaystatsmap={}
            for day in weekdaymap:
                hourstats={}
                for hour in weekdaymap[day]:
                    hourstats[hour]=(np.mean(weekdaymap[day][hour]),np.median(weekdaymap[day][hour]),np.std(weekdaymap[day][hour]))
                weekdaystatsmap[day]=hourstats
            weekdaystatsmapslist.append((region,weekdaystatsmap))
        return weekdaymapslist,weekdaystatsmapslist
    
    #Applying a smoothing filter to mitigate strong variance effects
    def smoothLS(self,weekdaymapslist,degree,dropVals=False):
        smootheddaymapslist=[]
        smoothedweekdaystatsmapslist=[]
        for regionrecords in weekdaymapslist:
            daymaps=regionrecords[1]
            smootheddaymaps={}
            for day in daymaps:
                smoothedhourrecords={}
                for hour in daymaps[day]:
                    hourrecords=daymaps[day][hour]
                    """performs moving triangle smoothing with a variable degree."""
                    """note that if dropVals is False, output length will be identical
                    to input length, but with copies of data at the flanking regions"""
                    window=np.array(range(degree)+[degree]+range(degree)[::-1])+1
                    smoothed=[]
                    for i in range(degree,len(hourrecords)-degree*2):
                        point=hourrecords[i:i+len(window)]*window
                        smoothed.append(sum(point)/sum(window))
                    if dropVals:
                        smoothedhourrecords[hour]=smoothed
                        continue
                    smoothed=[smoothed[0]]*(degree+degree/2)+smoothed
                    while len(smoothed)<len(hourrecords):
                        smoothed.append(smoothed[-1])
                    smoothedhourrecords[hour]=smoothed
                smootheddaymaps[day]=smoothedhourrecords
            smootheddaymapslist.append((regionrecords[0],smootheddaymaps))
            
            #Get statistics for time of day for each day
            smoothedweekdaystatsmap={}
            for day in smootheddaymaps:
                hourstats={}
                for hour in smootheddaymaps[day]:
                    hourstats[hour]=(np.mean(smootheddaymaps[day][hour]),np.median(smootheddaymaps[day][hour]),np.std(smootheddaymaps[day][hour]))
                smoothedweekdaystatsmap[day]=hourstats
            smoothedweekdaystatsmapslist.append((regionrecords[0],smoothed))
        
        return smootheddaymapslist,smoothedweekdaystatsmapslist
    
    #Same smoothing as above for TV data
    def smoothTV(self,weekdaymapsTV,degree,dropVals=False):
        smootheddaymapsTV={}
        for day in weekdaymapsTV:
            smoothedhourrecords={}
            for hour in weekdaymapsTV[day]:
                hourrecords=weekdaymapsTV[day][hour]
                """performs moving triangle smoothing with a variable degree."""
                """note that if dropVals is False, output length will be identical
                to input length, but with copies of data at the flanking regions"""
                window=np.array(range(degree)+[degree]+range(degree)[::-1])+1
                smoothed=[]
                for i in range(degree,len(hourrecords)-degree*2):
                    point=hourrecords[i:i+len(window)]*window
                    smoothed.append(sum(point)/sum(window))
                if dropVals:
                    smoothedhourrecords[hour]=smoothed
                    continue
                smoothed=[smoothed[0]]*(degree+degree/2)+smoothed
                while len(smoothed)<len(hourrecords):
                    smoothed.append(smoothed[-1])
                smoothedhourrecords[hour]=smoothed
            smootheddaymapsTV[day]=smoothedhourrecords
        
        #Get statistics for time of day for each day
        smoothedweekdaystatsmapTV={}
        for day in smootheddaymapsTV:
            hourstats={}
            for hour in smootheddaymapsTV[day]:
                hourstats[hour]=(np.mean(smootheddaymapsTV[day][hour]),np.median(smootheddaymapsTV[day][hour]),np.std(smootheddaymapsTV[day][hour]))
            smoothedweekdaystatsmapTV[day]=hourstats
        
        return smootheddaymapsTV,smoothedweekdaystatsmapTV
        
    #Test hypothesis 1
    def computesimilaritiesondaymeanvolumes(self,weekdaystatsmapslist,nullHthreshold):
        regionvectorsmap={}
        for entry in weekdaystatsmapslist:
            regiondaymeanvectors=[]
            region = entry[0]
            for dayindex in xrange(len(entry[1])):
                dayvector=[]
                for hour in entry[1][dayindex]:
                    dayvector.append(entry[1][dayindex][hour][0])
                regiondaymeanvectors.append(dayvector)
            regionvectorsmap[region]=regiondaymeanvectors
        
        regionpairsimilarities={}
        for region1 in regionvectorsmap:
            for region2 in regionvectorsmap:
                meanarray1=regionvectorsmap[region1]
                meanarray2=regionvectorsmap[region2]
                corrdists=[]
                countmismatches=0
                for dayvectorindex in xrange(len(meanarray1)):
                    #Exclude days that are not common workdays or weekends (Sunday and Friday)
                    if dayvectorindex == 0 or dayvectorindex == 5:
                        continue
                    vector1=meanarray1[dayvectorindex]
                    vector2=meanarray2[dayvectorindex]
                    if len(vector1)!=len(vector2):
                        countmismatches=countmismatches+1
                        continue
                    corrdist=spsd.correlation(vector1,vector2)
                    corrdists.append(corrdist)
                avcorrdist=np.mean(corrdists)
                regionpairsimilarities[(region1,region2)]=1-avcorrdist
        
        violatingpairs=[]
        for pair in regionpairsimilarities:
            if regionpairsimilarities[pair] > nullHthreshold:
                violatingpairs.append(pair)
                
        print "Mismatch count: " + str(countmismatches)
        
        return violatingpairs,regionpairsimilarities,regionvectorsmap
                 
    #Test hypothesis 2
    def computesimilaritiesondayhourvolumes(self,weekdaymapslist):
        x=1
        
    def performVIFanalysis(self,regionvectorsmap):
        regionVIFmap={}
        for dayindex in xrange(7):
            hourindex=0
            for region in regionvectorsmap:
                X=[]
                dayvector=regionvectorsmap[region][dayindex]
                if len(dayvector)!=24:
                    continue
                for hourindex in xrange(24):
                    predictorvector=[]
                    for region2 in regionvectorsmap:
                        if region2==region:
                            continue
                        if len(regionvectorsmap[region2][dayindex])!=24:
                            continue
                        predictorvector.append(regionvectorsmap[region2][dayindex][hourindex])
                    X.append(predictorvector)
                    hourindex=hourindex+1    
                X=np.array(X)
                dayvector=np.transpose(np.array(dayvector))
                #print X.shape
                #print dayvector.shape
                l=LinearRegression()
                l.fit(X,dayvector)
                rsquared=l.score(X,dayvector)
                if region in regionVIFmap:
                    regionVIFmap[region].append(rsquared)
                else:
                    regionVIFmap[region]=[rsquared]  
            
        for region in regionVIFmap:
            regionVIFmap[region]=1/float(1-np.mean(regionVIFmap[region]))
            
        return regionVIFmap
    
    #Generate same data structures for TV ratings data (First small file)
    def parseTVratingsfile(self,filepath):
        weekdaymapsTV={}
        ifile  = open(filepath, "rb")
        reader = csv.reader(ifile,delimiter='\t')
        for line in reader:
            if 'SMTWTFS' in line[1]:
                continue
            date=line[0]
            if date!='':
                date=date.split('/')
                date=datetime.datetime(int(date[2]),int(date[0]),int(date[1]))
                weekday=date.weekday()
            hour=int(line[1][0:2])
            if hour >= 24:
                hour = hour - 24
                weekday=(weekday+1) % 7
            #Converting to UK timezone
            hour = hour - 4
            if hour < 0:
                hour = hour % 24
                weekday = (weekday - 1) % 7
                
            if weekday in weekdaymapsTV:
                if hour in weekdaymapsTV[weekday]:
                    weekdaymapsTV[weekday][hour].append(int(line[2])*1000)
                else:
                    weekdaymapsTV[weekday][hour]=[int(line[2])*1000]
            else:
                weekdaymapsTV[weekday]={}
                weekdaymapsTV[weekday][hour]=[int(line[2])*1000]
                
        weekdaystatsmapTV={}
        for day in weekdaymapsTV:
            hourstats={}
            for hour in weekdaymapsTV[day]:
                hourstats[hour]=(np.mean(weekdaymapsTV[day][hour]),np.median(weekdaymapsTV[day][hour]),np.std(weekdaymapsTV[day][hour]))
            weekdaystatsmapTV[day]=hourstats
        
        regiondaymeanvectorsTV=[] 
        for dayindex in xrange(len(weekdaystatsmapTV)):
            dayvector=[]
            for hour in weekdaystatsmapTV[dayindex]:
                dayvector.append(weekdaystatsmapTV[dayindex][hour][0])
            regiondaymeanvectorsTV.append(dayvector) 
            
        return weekdaymapsTV,weekdaystatsmapTV,regiondaymeanvectorsTV
    
    #Same as above for longer period file with different channels
    def parsetotalTVratingsfilever2(self,filepath,channelindex):
        weekdaymapsTV={}
        ifile  = open(filepath, "rb")
        reader = csv.reader(ifile,delimiter='\t')
        for line in reader:
            if 'SMTWTFS' in line[1]:
                continue
            date=line[0]
            if date!='' and date!='dates':
                date=date.split('/')
                date=datetime.datetime(int(date[2]),int(date[0]),int(date[1]))
                weekday=date.weekday()
            if line[1]=='':
                continue
            hour=int(line[1][0:2])
            if hour >= 24:
                hour = hour - 24
                weekday=(weekday+1) % 7
            #Converting to UK timezone
            hour = hour - 4
            if hour < 0:
                hour = hour % 24
                weekday = (weekday - 1) % 7
                
            if weekday in weekdaymapsTV:
                if hour in weekdaymapsTV[weekday]:
                    weekdaymapsTV[weekday][hour].append(int(line[channelindex])*1000)
                else:
                    weekdaymapsTV[weekday][hour]=[int(line[channelindex])*1000]
            else:
                weekdaymapsTV[weekday]={}
                weekdaymapsTV[weekday][hour]=[int(line[channelindex])*1000]
                
        weekdaystatsmapTV={}
        for day in weekdaymapsTV:
            hourstats={}
            for hour in weekdaymapsTV[day]:
                hourstats[hour]=(np.mean(weekdaymapsTV[day][hour]),np.median(weekdaymapsTV[day][hour]),np.std(weekdaymapsTV[day][hour]))
            weekdaystatsmapTV[day]=hourstats
        
        regiondaymeanvectorsTV=[] 
        for dayindex in xrange(len(weekdaystatsmapTV)):
            dayvector=[]
            for hour in weekdaystatsmapTV[dayindex]:
                dayvector.append(weekdaystatsmapTV[dayindex][hour][0])
            regiondaymeanvectorsTV.append(dayvector) 
            
        return weekdaymapsTV,weekdaystatsmapTV,regiondaymeanvectorsTV
                   
    #Get correlation between LS average visitor volumes and average TV ratings for same region
    def getcorrelationsLSTVforregion(self,regionvectorsmap,regiondaymeanvectorsTV,region):
        meanarray1=regionvectorsmap[region]
        meanarray2=regiondaymeanvectorsTV
        corrdists=[]
        countmismatches=0
        for dayvectorindex in xrange(len(meanarray1)):
            #Exclude days that are not common workdays or weekends (Sunday and Friday)
            #if dayvectorindex == 0 or dayvectorindex == 5:
                #continue
            vector1=meanarray1[dayvectorindex]
            vector2=meanarray2[dayvectorindex]
            if len(vector1)!=len(vector2):
                countmismatches=countmismatches+1
                continue
            corrdist=spsd.correlation(vector1,vector2)
            corrdists.append(corrdist)
        avcorrdist=np.mean(corrdists)
        
        return 1-avcorrdist
    
    #Examine models' sensitivity to decreasing training set size
    def computemodelsensitivity(self,weekdaymapslist,weekdaymapsTV,region,orderrf,orderreg,ntrees):
        proportiontraining=[0.6,0.7,0.8,0.9]
        averrorpsrf=[]
        averrorpsreg=[]
        for p in proportiontraining:
            dayhourmodelmaprf,dayerrorsrf,dayrsquaredsrf,dayrsquaredsrandom,daycorrsrf,dayerrorstdsrf,dayerrorpsrf=self.trainrandomforest(weekdaymapslist, weekdaymapsTV,region,orderrf,ntrees,p)
            dayhourmodelmapreg,dayerrorsreg,dayerrorpsreg,dayrsquaredsreg,dayrsquaredrandom,daycorrsreg=self.runpolyregression(weekdaymapslist,weekdaymapsTV,region,orderreg,p)
            averrorprf,dayaverrorprf=self.getaveragemetric(dayerrorpsrf)
            averrorpsrf.append(averrorprf)
            averrorpreg,dayaverrorpreg=self.getaveragemetric(dayerrorpsreg)
            averrorpsreg.append(averrorpreg)
        return averrorpsrf,averrorpsreg
        
    #Perform Polynomial regression. Model should be trained for a particular day of the week and a specific time of day
    def runpolyregression(self,weekdaymapslist,weekdaymapsTV,region,order,percenttraining):
        for index in xrange(len(weekdaymapslist)):
            if region == weekdaymapslist[index][0]:
                regionindex=index
                break
        #print "Region index: "+str(regionindex)
        weekdaymapsLS=weekdaymapslist[regionindex][1]
        
        #Constructing training and test sets
        weekdaytrainingmapsLS={}
        weekdaytrainingmapsTV={}
        weekdaytestmapsLS={}
        weekdaytestmapsTV={}
        #trainingsetlength=int(0.7*len(weekdaymapsTV[0][0]))
        #Split dataset into training and test
        for day in weekdaymapsLS:
            dayhourlytrainingmapLS={}
            dayhourlytrainingmapTV={}
            dayhourlytestmapLS={}
            dayhourlytestmapTV={}
            for hour in weekdaymapsLS[day]:
                if len(weekdaymapsLS[day][hour]) <= len(weekdaymapsTV[day][hour]):      
                    trainingsetlength=int(percenttraining*len(weekdaymapsLS[day][hour]))
                else:
                    trainingsetlength=int(percenttraining*len(weekdaymapsTV[day][hour]))  
                trainingvectorLS=weekdaymapsLS[day][hour][0:trainingsetlength]
                validationvectorLS=weekdaymapsLS[day][hour][trainingsetlength:]
                trainingvectorTV=weekdaymapsTV[day][hour][0:trainingsetlength]
                validationvectorTV=weekdaymapsTV[day][hour][trainingsetlength:]
                '''
                print trainingvectorLS
                print validationvectorLS
                print trainingvectorTV
                print validationvectorTV
                '''
                dayhourlytrainingmapLS[hour]=trainingvectorLS
                dayhourlytrainingmapTV[hour]=trainingvectorTV
                dayhourlytestmapLS[hour]=validationvectorLS
                dayhourlytestmapTV[hour]=validationvectorTV
            
            weekdaytrainingmapsLS[day]=dayhourlytrainingmapLS
            weekdaytrainingmapsTV[day]=dayhourlytrainingmapTV
            weekdaytestmapsLS[day]=dayhourlytestmapLS
            weekdaytestmapsTV[day]=dayhourlytestmapTV
        
        #Train the model
        dayhourmodelmap={}
        for day in weekdaytrainingmapsLS:
            for hour in weekdaytrainingmapsLS[day]:
                X=weekdaytrainingmapsLS[day][hour]
                y=weekdaytrainingmapsTV[day][hour]
                if len(y)>len(X):
                    for n in xrange(len(y)-len(X)):
                        X.append(0)
                if len(X)>len(y):
                    for n in xrange(len(X)-len(y)):
                        y.append(0)
                X=np.array(X)
                y=np.array(y)   
                model=np.poly1d(np.polyfit(X, y, order))
                dayhourmodelmap[(day,hour)]=model
        
        #Test the model
        dayvals={}
        daypredictedvals={}
        dayerrors={}
        dayerrorps={}
        dayrsquareds={}
        daycorrs={}
        dayrsquaredrandom={}
        for day in weekdaytestmapsTV:
            hourvals=[]
            hourpredictedvals=[]
            hourerrors={}
            hourerrorps={}
            hourrsquareds={}
            hourcorrs={}
            hourrsquaredrandom={}
            for hour in weekdaytestmapsTV[day]:
                hourvals.append(weekdaytestmapsTV[day][hour])
                predicted=[]
                for value in weekdaytestmapsLS[day][hour]:
                    #print value
                    #print day,hour
                    predicted.append(dayhourmodelmap[(day,hour)](value))
                hourpredictedvals.append(predicted)
                #print weekdaytestmapsTV[day][hour]
                #print predicted
                #A fix that could be changed
                randomrsquareds=[]
                if len(weekdaytestmapsTV[day][hour]) < len(predicted):
                    predicted = predicted[0:len((weekdaytestmapsTV[day][hour]))]
                    actualtv=weekdaytestmapsTV[day][hour]
                else:
                    actualtv=weekdaytestmapsTV[day][hour][0:len(predicted)]
                corr=1-spsd.correlation(actualtv,predicted)
                rsquared=(1-spsd.correlation(actualtv,predicted))**2
                #Computing random rsquareds multiple times
                for nrandom in xrange(100):
                    randomvals=[random.randint(min(actualtv),max(actualtv)) for r in xrange(len(actualtv))]
                    randomrsquareds.append((1-spsd.correlation(actualtv,randomvals))**2)
                hourrsquaredrandom[hour]=np.mean(randomrsquareds)
                #print rsquared
                errorps=[]
                errors=[]
                for valindex in xrange(len(actualtv)):
                    if actualtv[valindex]==0:
                        errorp=math.fabs(actualtv[valindex]-predicted[valindex])/1000.0
                        error=(actualtv[valindex]-predicted[valindex])**2
                    else:
                        error=(actualtv[valindex]-predicted[valindex])**2
                        errorp=math.fabs(actualtv[valindex]-predicted[valindex])/float(actualtv[valindex])
                    errorps.append(errorp)
                    errors.append(error)
                hourerrorps[hour]=np.mean(errorps)
                hourerrors[hour]=np.sqrt(np.mean(errors))
                hourrsquareds[hour]=rsquared
                hourcorrs[hour]=corr
            dayerrors[day]=hourerrors
            dayerrorps[day]=hourerrorps
            dayrsquareds[day]=hourrsquareds
            daycorrs[day]=hourcorrs
            dayrsquaredrandom[day]=hourrsquaredrandom
                
        return dayhourmodelmap,dayerrors,dayerrorps,dayrsquareds,dayrsquaredrandom,daycorrs
    
    #Master method: Will run k-fold CV regression for N times and takes the average
    def runregression(self,weekdaymapslist,weekdaymapsTV,region,order,n,N):
        models=[]
        rsquareds=[]
        corrs=[]
        errors=[]
        errorpercentages=[]
        errorstds=[]
        runerrors={}
        runrsquaredlist=[]
        runcorrslist=[]
        runerrorslist=[]
        runerrorpercentageslist=[]
        runerrorstdslist=[]
        for runindex in xrange(N):
            print runindex
            dayhourmodelmaps,dayrsquaredslist,daycorrslist,dayerrorslist,dayerrorstdslist,dayerrorpercentageslist=self.runpolyregressionwithnfoldcv\
            (weekdaymapslist,weekdaymapsTV,region,order,n)
            rundayrsquareds,rundaycorrs,rundayerrors,rundayerrorstds,rundayerrorpercentages=self.getregressionrunstatistics(dayrsquaredslist,daycorrslist,dayerrorslist,dayerrorstdslist,dayerrorpercentageslist)
            runrsquaredlist.append(rundayrsquareds)
            runcorrslist.append(rundaycorrs)
            runerrorslist.append(rundayerrors)
            runerrorpercentageslist.append(rundayerrorpercentages)
            runerrorstdslist.append(rundayerrorstds)
            averror,averrorstd,avrsquared,averrorpercantages,finalmodels=self.getfinalmodel(dayhourmodelmaps,dayrsquaredslist,dayerrorslist,dayerrorstdslist,dayerrorpercentageslist)
            errors.append(averror)
            errorpercentages.append(averrorpercantages)
            errorstds.append(averrorstd)
            rsquareds.append(avrsquared)
            models.append(finalmodels)
        
        finaldayrsquareds,finaldaycorrs,finaldayerrors,finaldayerrorpercentages,finaldayerrorstds=self.getregressionrunstatistics(runrsquaredlist,runcorrslist,runerrorslist,runerrorstdslist,runerrorpercentageslist)
            
        finalaveragemodel=self.getaveragefinalmodels(models)
        
        #error=np.mean(errors)
        #rsquared=np.mean(rsquareds)
        
        errorsofruns=[]
        errorstdsofruns=[]
        for runerrors in errors:
            folderrors=[]
            for foldindex in xrange(len(runerrors)):
                folderrors.append(runerrors[foldindex][0])
            errorsofruns.append(np.mean(folderrors))
            
        for runerrorstds in errorstds:
            folderrorstds=[]
            for foldindex in xrange(len(runerrorstds)):
                folderrorstds.append(runerrorstds[foldindex][0])
            errorstdsofruns.append(np.mean(folderrorstds))
        
        return errors,errorstds,rsquareds,models,finalaveragemodel,errorsofruns,errorstdsofruns,finaldayrsquareds,finaldaycorrs,finaldayerrors,finaldayerrorstds,finaldayerrorpercentages

    #Get k-fold regression single run statistics
    def getregressionrunstatistics(self,dayrsquaredslist,daycorrslist,dayerrorslist,dayerrorstdslist,dayerrorpercentageslist):
        finaldayrsquareds={}
        finaldaycorrs={}
        finaldayerrors={}
        finaldayerrorpercentages={}
        finaldayerrorstds={}
        dayhourrsquareds={}
        dayhourcorrs={}
        dayhourerrors={}
        dayhourerrorpercentages={}
        dayhourerrorstds={}
        for day in xrange(7):
            finaldayrsquareds[day]={}
            finaldaycorrs[day]={}
            finaldayerrors[day]={}
            finaldayerrorpercentages[day]={}
            finaldayerrorstds[day]={}
        
        for foldindex in xrange(len(dayrsquaredslist)):
            dayrsquareds=dayrsquaredslist[foldindex]
            daycorrs=daycorrslist[foldindex]
            dayerrors=dayerrorslist[foldindex]
            dayerrorpercentages=dayerrorpercentageslist[foldindex]
            dayerrorstds=dayerrorstdslist[foldindex]
            for day in dayrsquareds:
                for hour in dayrsquareds[day]:
                    if (day,hour) in dayhourrsquareds:
                        dayhourrsquareds[(day,hour)].append(dayrsquareds[day][hour])
                    else:
                        dayhourrsquareds[(day,hour)]=[dayrsquareds[day][hour]]
                    
                    if (day,hour) in dayhourcorrs:
                        dayhourcorrs[(day,hour)].append(daycorrs[day][hour])
                    else:
                        dayhourcorrs[(day,hour)]=[daycorrs[day][hour]]
                        
                    if (day,hour) in dayhourerrors:
                        dayhourerrors[(day,hour)].append(dayerrors[day][hour])
                    else:
                        dayhourerrors[(day,hour)]=[dayerrors[day][hour]]
                        
                    if (day,hour) in dayerrorpercentages:
                        dayhourerrorpercentages[(day,hour)].append(dayerrorpercentages[day][hour])
                    else:
                        dayhourerrorpercentages[(day,hour)]=[dayerrorpercentages[day][hour]]
                        
                    if (day,hour) in dayhourerrorstds:
                        dayhourerrorstds[(day,hour)].append(dayerrorstds[day][hour])
                    else:
                        dayhourerrorstds[(day,hour)]=[dayerrorstds[day][hour]]
                        
        for (day,hour) in dayhourrsquareds:
            finaldayrsquareds[day][hour]=np.mean(dayhourrsquareds[(day,hour)])
            finaldaycorrs[day][hour]=np.mean(dayhourcorrs[(day,hour)])
            finaldayerrors[day][hour]=np.mean(dayhourerrors[(day,hour)])
            finaldayerrorpercentages[day][hour]=np.mean(dayhourerrorpercentages[(day,hour)])
            finaldayerrorstds[day][hour]=np.mean(dayhourerrorstds[(day,hour)])
        
        return finaldayrsquareds,finaldaycorrs,finaldayerrors,finaldayerrorstds,finaldayerrorpercentages
    
    #Get final models for k-fold CV regression multiple times
    def getaveragefinalmodels(self,dayhourmodelmaps):
        modelmaps={}
        finalmodels={}
        for index in xrange(len(dayhourmodelmaps)):
            for modelkey in dayhourmodelmaps[index]:
                if modelkey in modelmaps:
                    modelmaps[modelkey].append(list(dayhourmodelmaps[index][modelkey])[0:])
                else:
                    modelmaps[modelkey]=[list(dayhourmodelmaps[index][modelkey])[0:]]
        
        for modelkey in modelmaps:
            index=0
            parametermap={}
            finalparameterlist=[]
            for parameterindex in xrange(len(modelmaps[modelkey][0])):
                for parameterlist in modelmaps[modelkey]:
                    if parameterindex in parametermap:
                        parametermap[parameterindex].append(parameterlist[parameterindex])
                    else:
                        parametermap[parameterindex]=[parameterlist[parameterindex]]
            
            for parameterindex in parametermap:
                finalparameterlist.append(np.mean(parametermap[parameterindex]))
            
            finalmodels[modelkey]=np.poly1d(list(finalparameterlist))
        
        return finalmodels
    
    #Same as above but using n-fold cross validation for the model
    def runpolyregressionwithnfoldcv(self,weekdaymapslist,weekdaymapsTV,region,order,n):
        for index in xrange(len(weekdaymapslist)):
            if region == weekdaymapslist[index][0]:
                regionindex=index
                break
        #print "Region index: "+str(regionindex)
        weekdaymapsLS=weekdaymapslist[regionindex][1]
        
        dayhourmodelmaps=[]
        dayrsquaredslist=[]
        dayerrorslist=[]
        dayerrorpercentageslist=[]
        dayerrorstdslist=[]
        daycorrslist=[]
        finalmodels={}
        for index in xrange(n):
            #Constructing training and test sets
            weekdaytrainingmapsLS={}
            takenindexes={}
            weekdaytrainingmapsTV={}
            weekdayvalidationmapsLS={}
            weekdayvalidationmapsTV={}
            weekdaytestmapsLS={}
            weekdaytestmapsTV={}
            for day in weekdaymapsLS:
                dayhourlytrainingmapLS={}
                dayhourlytrainingmapTV={}
                dayhourlytestmapLS={}
                dayhourlytestmapTV={}
                dayhourlyvalidationmapLS={}
                dayhourlyvalidationmapTV={}
                for hour in weekdaymapsLS[day]:
                    rawvectorLS=weekdaymapsLS[day][hour]
                    rawvectorTV=weekdaymapsTV[day][hour]
                    if len(rawvectorLS)<len(rawvectorTV):
                        rawvectorTV=rawvectorTV[0:len(rawvectorLS)]
                    else:
                        rawvectorLS=rawvectorLS[0:len(rawvectorTV)]
                    #print rawvectorTV
                    #print n
                    
                    #For testing the whole model There's redundancy in computing those since they only need to be computed once
                    #trainingrawvectorLS=rawvectorLS[0:0.7*len(rawvectorLS)]
                    #trainingrawvectorTV=rawvectorTV[0:0.7*len(rawvectorTV)]
                    #testvectorLS=rawvectorLS[0.7*len(rawvectorLS):]
                    #testvectorTV=rawvectorTV[0.7*len(rawvectorTV):]
                    
                    #dayhourlytestmapLS[hour]=testvectorLS
                    #dayhourlytestmapTV[hour]=testvectorTV
                    
                    validationsetlength=len(rawvectorTV)/n
                    validationvectorLS=[]
                    validationvectorTV=[]
                    
                    #Using random choice
                    indexes=[random.randint(0,len(rawvectorLS)-1) for r in xrange(validationsetlength)]
                    indexes.sort()
                    indexes2=list(indexes)
                    #print indexes2
                    for index in xrange(len(indexes)):
                        if indexes[index] in takenindexes:
                            taken=True
                            count=0
                            while taken and count<50:
                                ind=random.randint(0,len(rawvectorLS)-1)
                                count=count+1
                                if ind not in takenindexes:
                                    taken=False
                                    indexes2[index]=ind
                                    takenindexes[ind]=0
                                #print takenindexes
                        else:
                            takenindexes[index]=0
                                 
                    for index in indexes2:
                        validationvectorLS.append(rawvectorLS[index])
                        validationvectorTV.append(rawvectorTV[index])
                    trainingvectorLS=list(rawvectorLS)
                    trainingvectorTV=list(rawvectorTV)
                    trainingvectorLS=[i for j, i in enumerate(trainingvectorLS) if j not in indexes2]
                    trainingvectorTV=[i for j, i in enumerate(trainingvectorTV) if j not in indexes2]
                    
                    '''
                    
                    #print validationsetlength
                    validationvectorLS=rawvectorLS[index*validationsetlength:index*validationsetlength+validationsetlength]
                    #print validationvectorLS
                    validationvectorTV=rawvectorTV[index*validationsetlength:index*validationsetlength+validationsetlength]
                    #print validationvectorTV
                    trainingvectorLS=rawvectorLS[0:index*validationsetlength]+rawvectorLS[index*validationsetlength+validationsetlength:]
                    trainingvectorTV=rawvectorTV[0:index*validationsetlength]+rawvectorTV[index*validationsetlength+validationsetlength:]
                    '''
                    
                    dayhourlytrainingmapLS[hour]=trainingvectorLS
                    dayhourlytrainingmapTV[hour]=trainingvectorTV
                    dayhourlyvalidationmapLS[hour]=validationvectorLS
                    dayhourlyvalidationmapTV[hour]=validationvectorTV
                
                weekdaytrainingmapsLS[day]=dayhourlytrainingmapLS
                weekdaytrainingmapsTV[day]=dayhourlytrainingmapTV
                weekdayvalidationmapsLS[day]=dayhourlyvalidationmapLS
                weekdayvalidationmapsTV[day]=dayhourlyvalidationmapTV
                
                #weekdaytestmapsLS[day]=dayhourlytestmapLS
                #weekdaytestmapsTV[day]=dayhourlytestmapTV
                
            #Train the model
            dayhourmodelmap={}
            for day in weekdaytrainingmapsLS:
                for hour in weekdaytrainingmapsLS[day]:
                    X=weekdaytrainingmapsLS[day][hour]
                    y=weekdaytrainingmapsTV[day][hour]
                    if len(y)>len(X):
                        for n in xrange(len(y)-len(X)):
                            X.append(0)
                    if len(X)>len(y):
                        for n in xrange(len(X)-len(y)):
                            y.append(0)
                    X=np.array(X)
                    y=np.array(y)   
                    model=np.poly1d(np.polyfit(X, y, order))
                    dayhourmodelmap[(day,hour)]=model
            
            #Test the model
            dayvals={}
            daypredictedvals={}
            dayrsquareds={}
            daycorrs={}
            dayerrors={}
            dayerrorpercentages={}
            dayerrorstds={}
            dayrsquaredrandom={}
            for day in weekdayvalidationmapsTV:
                hourvals=[]
                hourpredictedvals=[]
                hourerrors={}
                hourrsquareds={}
                hourcorrs={}
                hourerrors={}
                hourerrorpercentages={}
                hourerrorstds={}
                hourrsquaredrandom={}
                for hour in weekdayvalidationmapsTV[day]:
                    hourvals.append(weekdayvalidationmapsTV[day][hour])
                    predicted=[]
                    for value in weekdayvalidationmapsLS[day][hour]:
                        #print value
                        #print day,hour
                        predicted.append(dayhourmodelmap[(day,hour)](value))
                    hourpredictedvals.append(predicted)
                    #print weekdaytestmapsTV[day][hour]
                    #print predicted
                    #A fix that could be changed
                    randomrsquareds=[]
                    if len(weekdayvalidationmapsTV[day][hour]) < len(predicted):
                        predicted = predicted[0:len((weekdayvalidationmapsTV[day][hour]))]
                        actualtv=weekdayvalidationmapsTV[day][hour]
                    else:
                        actualtv=weekdayvalidationmapsTV[day][hour][0:len(predicted)]
                    corr=1-spsd.correlation(actualtv,predicted)
                    rsquared=(1-spsd.correlation(actualtv,predicted))**2
                    #Computing random rsquareds multiple times
                    for nrandom in xrange(100):
                        randomvals=[random.randint(min(actualtv),max(actualtv)) for r in xrange(len(actualtv))]
                        randomrsquareds.append((1-spsd.correlation(actualtv,randomvals))**2)
                        
                    errors=[]
                    errorpercentages=[]
                    for valindex in xrange(len(actualtv)):
                        if actualtv[valindex]==0:
                            error=math.fabs(actualtv[valindex]-predicted[valindex])**2
                            errorp=math.fabs(actualtv[valindex]-predicted[valindex])/1000.0
                            #print "Zero occurrence"
                        else:
                            error=(actualtv[valindex]-predicted[valindex])**2
                            errorp=math.fabs(actualtv[valindex]-predicted[valindex])/float(actualtv[valindex])
                        errors.append(error)
                        errorpercentages.append(errorp)
                        
                    hourerrors[hour]=np.sqrt(np.mean(errors))
                    hourerrorpercentages[hour]=np.mean(errorpercentages)
                    hourerrorstds[hour]=np.sqrt(np.std(errors))
                    hourrsquaredrandom[hour]=np.mean(randomrsquareds)
                    hourrsquareds[hour]=rsquared
                    hourcorrs[hour]=corr
                dayrsquareds[day]=hourrsquareds
                daycorrs[day]=hourcorrs
                dayerrors[day]=hourerrors
                dayerrorpercentages[day]=hourerrorpercentages
                dayerrorstds[day]=hourerrorstds
                dayrsquaredrandom[day]=hourrsquaredrandom
            dayhourmodelmaps.append(dayhourmodelmap)
            dayrsquaredslist.append(dayrsquareds)
            daycorrslist.append(daycorrs)
            dayerrorslist.append(dayerrors)
            dayerrorpercentageslist.append(dayerrorpercentages)
            dayerrorstdslist.append(dayerrorstds)
        return dayhourmodelmaps,dayrsquaredslist,daycorrslist,dayerrorslist,dayerrorstdslist,dayerrorpercentageslist
    
    def getfinalmodel(self,dayhourmodelmaps,dayrsquaredslist,dayerrorslist,dayerrorpercentageslist,dayerrorstdslist):
        modelmaps={}
        finalmodels={}
        avrsquareds={}
        for index in xrange(len(dayhourmodelmaps)):
            for modelkey in dayhourmodelmaps[index]:
                if modelkey in modelmaps:
                    modelmaps[modelkey].append(list(dayhourmodelmaps[index][modelkey])[0:])
                else:
                    modelmaps[modelkey]=[list(dayhourmodelmaps[index][modelkey])[0:]]
        
        for modelkey in modelmaps:
            index=0
            parametermap={}
            finalparameterlist=[]
            for parameterindex in xrange(len(modelmaps[modelkey][0])):
                for parameterlist in modelmaps[modelkey]:
                    if parameterindex in parametermap:
                        parametermap[parameterindex].append(parameterlist[parameterindex])
                    else:
                        parametermap[parameterindex]=[parameterlist[parameterindex]]
            
            for parameterindex in parametermap:
                finalparameterlist.append(np.mean(parametermap[parameterindex]))
            
            finalmodels[modelkey]=np.poly1d(list(finalparameterlist))
        
        averrors=[]
        for errormap in dayerrorslist:
            averrors.append(self.getaveragemetric(errormap))
            
        averrorpercantages=[]
        for errorpmap in dayerrorpercentageslist:
            averrorpercantages.append(self.getaveragemetric(errorpmap))
            
        averrorstds=[]
        for errorstdmap in dayerrorstdslist:
            averrorstds.append(self.getaveragemetric(errorstdmap))
            
        #Fix
        #averror=np.mean(averrors)
        
        avrsquareds=[]
        for rsquaredmap in dayrsquaredslist:
            avrsquareds.append(self.getaveragemetric(rsquaredmap))
        #avrsquared=np.mean(avrsquareds)
        
        return averrors,averrorstds,avrsquareds,averrorpercantages,finalmodels
            
    #May be useful in future
    def getandtestfinalmodelontestset(self,dayhourmodelmaps,weekdaytestmapsLS,weekdaytestmapsTV):
        modelmaps={}
        finalmodels={}
        for index in xrange(len(dayhourmodelmaps)):
            for modelkey in dayhourmodelmaps[index]:
                if modelkey in modelmaps:
                    modelmaps[modelkey].append(list(modelmaps[modelkey])[0:])
                else:
                    modelmaps[modelkey]=[list(modelmaps[modelkey])[0:]]
        
        for modelkey in modelmaps:
            index=0
            parametermap={}
            finalparameterlist=[]
            for parameterindex in xrange(len(modelmaps[modelkey][0])):
                for parameterlist in modelmaps[modelkey]:
                    if parameterindex in parametermap:
                        parametermap[parameterindex].append(parameterlist[parameterindex])
                    else:
                        parametermap[parameterindex]=[parameterlist[parameterindex]]
            
            for parameterindex in parametermap:
                finalparameterlist.append(np.mean(parametermap[parameterindex]))
            
            finalmodels[modelkey]=np.poly1d(list(finalparameterlist))
        
        #Test (Copied from above)
        #Test the model
        dayvals={}
        daypredictedvals={}
        dayTVvals={}
        dayerrors={}
        dayrsquareds={}
        daycorrs={}
        dayrsquaredrandom={}
        for day in weekdaytestmapsTV:
            hourvals={}
            hourpredictedvals={}
            hourTVvals={}
            hourerrors={}
            hourrsquareds={}
            hourcorrs={}
            hourrsquaredrandom={}
            for hour in weekdaytestmapsTV[day]:
                predicted=[]
                for value in weekdaytestmapsLS[day][hour]:
                    #print value
                    #print day,hour
                    predicted.append(finalmodels[(day,hour)](value))
                hourpredictedvals.append(predicted)
                #print weekdaytestmapsTV[day][hour]
                #print predicted
                #A fix that could be changed
                randomrsquareds=[]
                if len(weekdaytestmapsTV[day][hour]) < len(predicted):
                    predicted = predicted[0:len((weekdaytestmapsTV[day][hour]))]
                    actualtv=weekdaytestmapsTV[day][hour]
                else:
                    actualtv=weekdaytestmapsTV[day][hour][0:len(predicted)]
                corr=1-spsd.correlation(actualtv,predicted)
                rsquared=(1-spsd.correlation(actualtv,predicted))**2
                #Computing random rsquareds multiple times
                hourvals[hour]=weekdaytestmapsLS[day][hour]
                hourpredictedvals[hour]=predicted
                hourTVvals[hour]=actualtv
                for nrandom in xrange(100):
                    randomvals=[random.randint(min(actualtv),max(actualtv)) for r in xrange(len(actualtv))]
                    randomrsquareds.append((1-spsd.correlation(actualtv,randomvals))**2)
                hourrsquaredrandom[hour]=np.mean(randomrsquareds)
                #print rsquared
                errors=[]
                for valindex in xrange(len(actualtv)):
                    if actualtv[valindex]==0:
                        error=math.fabs(actualtv[valindex]-predicted[valindex])/100
                    else:
                        error=math.fabs(actualtv[valindex]-predicted[valindex])/float(actualtv[valindex])
                    errors.append(error)
                hourerrors[hour]=np.mean(errors)
                hourrsquareds[hour]=rsquared
                hourcorrs[hour]=corr
            dayvals[day]=hourvals
            daypredictedvals[day]=hourpredictedvals
            dayTVvals[day]=hourTVvals
            dayerrors[day]=hourerrors
            dayrsquareds[day]=hourrsquareds
            daycorrs[day]=hourcorrs
            dayrsquaredrandom[day]=hourrsquaredrandom
            
        return finalmodels,dayrsquareds,daycorrs,dayerrors,dayvals,dayTVvals,daypredictedvals
        
    #Get Average Metric for model
    def getaveragemetric(self,dayrsquareds):
        dayavrsquared={}
        for day in dayrsquareds:
            rsquaredvals=[]
            for hour in dayrsquareds[day]:
                if math.isnan(dayrsquareds[day][hour]):
                    continue
                rsquaredvals.append(dayrsquareds[day][hour])
            dayavrsquared[day]=np.mean(rsquaredvals)
        
        dayvals=[]
        for day in dayavrsquared:
            dayvals.append(dayavrsquared[day])
        
        avrsquared=np.mean(dayvals)
        return avrsquared,dayavrsquared
    
    #Random forest model
    def trainrandomforest(self,weekdaymapslist,weekdaymapsTV,region,order,ntrees,percenttraining):
        for index in xrange(len(weekdaymapslist)):
            if region == weekdaymapslist[index][0]:
                regionindex=index
                break
        print "Region index: "+str(regionindex)
        weekdaymapsLS=weekdaymapslist[regionindex][1]
        
        #Constructing training and test sets
        weekdaytrainingmapsLS={}
        weekdaytrainingmapsTV={}
        weekdaytestmapsLS={}
        weekdaytestmapsTV={}
        #trainingsetlength=int(0.7*len(weekdaymapsTV[0][0]))
        #Split dataset into training and test
        for day in weekdaymapsLS:
            dayhourlytrainingmapLS={}
            dayhourlytrainingmapTV={}
            dayhourlytestmapLS={}
            dayhourlytestmapTV={}
            for hour in weekdaymapsLS[day]:
                if len(weekdaymapsLS[day][hour]) <= len(weekdaymapsTV[day][hour]):      
                    trainingsetlength=int(percenttraining*len(weekdaymapsLS[day][hour]))
                else:
                    trainingsetlength=int(percenttraining*len(weekdaymapsTV[day][hour]))  
                trainingvectorLS=weekdaymapsLS[day][hour][0:trainingsetlength]
                validationvectorLS=weekdaymapsLS[day][hour][trainingsetlength:]
                trainingvectorTV=weekdaymapsTV[day][hour][0:trainingsetlength]
                validationvectorTV=weekdaymapsTV[day][hour][trainingsetlength:]
                '''
                print trainingvectorLS
                print validationvectorLS
                print trainingvectorTV
                print validationvectorTV
                '''
                dayhourlytrainingmapLS[hour]=trainingvectorLS
                dayhourlytrainingmapTV[hour]=trainingvectorTV
                dayhourlytestmapLS[hour]=validationvectorLS
                dayhourlytestmapTV[hour]=validationvectorTV
            
            weekdaytrainingmapsLS[day]=dayhourlytrainingmapLS
            weekdaytrainingmapsTV[day]=dayhourlytrainingmapTV
            weekdaytestmapsLS[day]=dayhourlytestmapLS
            weekdaytestmapsTV[day]=dayhourlytestmapTV
        
        
        #Train the model
        dayhourmodelmap={}
        for day in weekdaytrainingmapsLS:
            for hour in weekdaytrainingmapsLS[day]:
                X=[weekdaytrainingmapsLS[day][hour]]
                
                #Get polynomial features
                if order>1:
                    for i in xrange(order-1):
                        X.append([j**(i+2) for j in X[i]])
                           
                y=weekdaytrainingmapsTV[day][hour]
                '''
                if len(y)>len(X):
                    for n in xrange(len(y)-len(X)):
                        X.append(0)
                if len(X)>len(y):
                    for n in xrange(len(X)-len(y)):
                        y.append(0)
                '''
                X=np.transpose(np.array(X))
                #print X
                y=np.array(y)
                #print y
                model=rf(n_estimators=ntrees)
                model.fit(X,y)
                dayhourmodelmap[(day,hour)]=model
                
        #Test the model
        dayvals={}
        daypredictedvals={}
        dayerrors={}
        dayerrorpercentages={}
        dayerrorstds={}
        dayrsquareds={}
        daycorrs={}
        dayrsquaredrandom={}
        for day in weekdaytestmapsTV:
            hourvals=[]
            hourpredictedvals=[]
            hourerrors={}
            hourerrorpercentages={}
            hourerrorstds={}
            hourrsquareds={}
            hourcorrs={}
            hourrsquaredrandom={}
            for hour in weekdaytestmapsTV[day]:
                hourvals.append(weekdaytestmapsTV[day][hour])
                predicted=[]
                for value in weekdaytestmapsLS[day][hour]:
                    #print value
                    #print day,hour
                    #Need to change to appropriate format
                    x=[value]
                    if order>1:
                        for i in xrange(order-1):
                            x.append(x[0]**(i+2))
                    predicted.append(dayhourmodelmap[(day,hour)].predict(np.transpose(np.array(x)))[0])
                hourpredictedvals.append(predicted)
                #print weekdaytestmapsTV[day][hour]
                #print predicted
                #A fix that could be changed
                randomrsquareds=[]
                if len(weekdaytestmapsTV[day][hour]) < len(predicted):
                    predicted = predicted[0:len((weekdaytestmapsTV[day][hour]))]
                    actualtv=weekdaytestmapsTV[day][hour]
                else:
                    actualtv=weekdaytestmapsTV[day][hour][0:len(predicted)]
                corr=1-spsd.correlation(actualtv,predicted)
                rsquared=(1-spsd.correlation(actualtv,predicted))**2
                #Computing random rsquareds multiple times
                for nrandom in xrange(100):
                    randomvals=[random.randint(min(actualtv),max(actualtv)) for r in xrange(len(actualtv))]
                    randomrsquareds.append((1-spsd.correlation(actualtv,randomvals))**2)
                hourrsquaredrandom[hour]=np.mean(randomrsquareds)
                #print rsquared
                errors=[]
                errorpercentages=[]
                for valindex in xrange(len(actualtv)):
                    if actualtv[valindex]==0:
                        errorpercentage=math.fabs(actualtv[valindex]-predicted[valindex])/1000.0
                        error=(actualtv[valindex]-predicted[valindex])**2
                    else:
                        errorpercentage=math.fabs(actualtv[valindex]-predicted[valindex])/float(actualtv[valindex])
                        error=(actualtv[valindex]-predicted[valindex])**2
                    errors.append(error)
                    errorpercentages.append(errorpercentage)
                hourerrors[hour]=np.sqrt(np.mean(errors))
                hourerrorpercentages[hour]=np.mean(errorpercentages)
                hourerrorstds[hour]=np.sqrt(np.std(errors))
                hourrsquareds[hour]=rsquared
                hourcorrs[hour]=corr
            dayerrors[day]=hourerrors
            dayerrorpercentages[day]=hourerrorpercentages
            dayerrorstds[day]=hourerrorstds
            dayrsquareds[day]=hourrsquareds
            daycorrs[day]=hourcorrs
            dayrsquaredrandom[day]=hourrsquaredrandom
                
        return dayhourmodelmap,dayerrors,dayrsquareds,dayrsquaredrandom,daycorrs,dayerrorstds,dayerrorpercentages
    
    #Sort models by corr coefficient and RMSE
    def sortmodelsbycorranderrors(self,daycorrs,dayerrors):
        daymodelcorrssorted={}
        for day in daycorrs:
            daymodellistsorted=[]
            for hour in daycorrs[day]:
                daymodellistsorted.append((hour,daycorrs[day][hour]))
            daymodellistsorted=sorted(daymodellistsorted, key=lambda a:a[1],reverse=True)
            daymodelcorrssorted[day]=daymodellistsorted
        
        daymodelerrorssorted={}
        for day in dayerrors:
            daymodellistsorted=[]
            for hour in dayerrors[day]:
                daymodellistsorted.append((hour,dayerrors[day][hour]))
            daymodellistsorted=sorted(daymodellistsorted, key=lambda a:a[1])
            daymodelerrorssorted[day]=daymodellistsorted
            
        return daymodelcorrssorted,daymodelerrorssorted
    
    #Get top performing N models based on corr and RMSE
    def getoverlapbycorranderror(self,N,daymodelcorrssortedrf,daymodelcorrssortedreg,daymodelerrorssortedrf,daymodelerrorssortedreg):
        topmodelsrf={}
        topmodelsreg={}
        for day in daymodelcorrssortedrf:
            corrsrf=daymodelcorrssortedrf[day][0:N]
            errorsrf=daymodelerrorssortedrf[day][0:N]
            corrsreg=daymodelcorrssortedreg[day][0:N]
            errorsreg=daymodelerrorssortedreg[day][0:N]
            corrsrflist=[]
            errorsrflist=[]
            corrsreglist=[]
            errorsreglist=[]
            for tupindex in xrange(len(corrsrf)):
                corrsrflist.append(corrsrf[tupindex][0])
                errorsrflist.append(errorsrf[tupindex][0])
                corrsreglist.append(corrsreg[tupindex][0])
                errorsreglist.append(errorsreg[tupindex][0])
            topmodelsrf[day]=list(set.intersection(set(corrsrflist),set(errorsrflist)))
            topmodelsreg[day]=list(set.intersection(set(corrsreglist),set(errorsreglist)))
        
        return topmodelsrf,topmodelsreg
    
    #Get predictions for days of week for a set of weeks. Model type is used to specify RF or reg (To use appropriate predict method call) 0:Reg 1:RF
    def getvaluesandpredictionsforweeks(self,regionindex,startweekindex,endweekindex,smootheddaymapslist,smootheddaymapsTV,daymodels,modeltype,rforder):
        LSvalues,TVvalues=self.getvaluesforweeks(regionindex,startweekindex,endweekindex,smootheddaymapslist,smootheddaymapsTV)
        predTVvalues={}
        for week in LSvalues:
            dayLSvalues=LSvalues[week]
            dayTVvalues=TVvalues[week]
            daypredvaluesmap={}
            for day in dayLSvalues:
                daypredvalues=[]
                for valindex in xrange(len(dayLSvalues[day])):
                    if modeltype==0: #Reg case
                        hour=dayTVvalues[day][valindex][0]
                        daypredvalues.append((hour,daymodels[(day,hour)](dayLSvalues[day][valindex][1])))
                    else: #RF case
                        hour=dayTVvalues[day][valindex][0]
                        x=[dayLSvalues[day][valindex][1]]
                        if rforder>1:
                            for i in xrange(rforder-1):
                                x.append(x[0]**(i+2))
                        daypredvalues.append((hour,daymodels[(day,hour)].predict(np.transpose(np.array(x)))[0]))
                daypredvaluesmap[day]=daypredvalues
            predTVvalues[week]=daypredvaluesmap
            
        return LSvalues,TVvalues,predTVvalues
    
    #Get values for all hours of day for days of specific weeks
    def getvaluesforweeks(self,regionindex,startweekindex,endweekindex,smootheddaymapslist,smootheddaymapsTV):
        weekindexes=list(range(startweekindex,endweekindex))
        LSvalues={}
        TVvalues={}
        for weekindex in weekindexes:
            dayLSvalues,dayTVvalues=self.getweekvalues(regionindex,weekindex,smootheddaymapslist,smootheddaymapsTV)
            LSvalues[weekindex]=dayLSvalues
            TVvalues[weekindex]=dayTVvalues
        
        return LSvalues,TVvalues
            
    #Get hour values for all days in a specific week
    def getweekvalues(self,regionindex,weekindex,smootheddaymapslist,smootheddaymapsTV):
        dayLSvalues={}
        dayTVvalues={}
        for day in smootheddaymapsTV:
            for hour in smootheddaymapsTV[day]:
                if day in dayTVvalues:
                    dayTVvalues[day].append((hour,smootheddaymapsTV[day][hour][weekindex]))
                else:
                    dayTVvalues[day]=[(hour,smootheddaymapsTV[day][hour][weekindex])]
                
                if day in dayLSvalues:
                    dayLSvalues[day].append((hour,smootheddaymapslist[regionindex][1][day][hour][weekindex]))
                else:
                    dayLSvalues[day]=[(hour,smootheddaymapslist[regionindex][1][day][hour][weekindex])]
                    
        return dayLSvalues,dayTVvalues
    
    #Generate week day plots for a specific week and day
    def generateweekdayplots(self,LSvalues,TVvalues,predTVvalues,weekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        x=xrange(24)
        for dayindex in xrange(7):
            ytvday=[]
            ylsday=[]
            ypredday=[]
            for valindex in xrange(len(TVvalues[weekindex][dayindex])):
                ytvday.append(TVvalues[weekindex][dayindex][valindex][1])
                ylsday.append(LSvalues[weekindex][dayindex][valindex][1])
                ypredday.append(predTVvalues[weekindex][dayindex][valindex][1])
            ytv.append(ytvday)
            yls.append(ylsday)
            ypred.append(ypredday)
            
        # Seven subplots sharing both x/y axes
        f, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = pyplot.subplots(7, sharex=False, sharey=True)
        ax1.plot(x,ytv[0],color="green")
        ax1.plot(x,ypred[0],color="black")
        ax12=ax1.twinx()
        ax12.plot(x,yls[0],color="red")
        
        ax2.plot(x,ytv[1],color="green")
        ax2.plot(x,ypred[1],color="black")
        ax22=ax2.twinx()
        ax22.plot(x,yls[1],color="red")
        
        ax3.plot(x,ytv[2],color="green")
        ax3.plot(x,ypred[2],color="black")
        ax32=ax3.twinx()
        ax32.plot(x,yls[2],color="red")
        
        ax4.plot(x,ytv[3],color="green")
        ax4.plot(x,ypred[3],color="black")
        ax42=ax4.twinx()
        ax42.plot(x,yls[3],color="red")
        
        ax5.plot(x,ytv[4],color="green")
        ax5.plot(x,ypred[4],color="black")
        ax52=ax5.twinx()
        ax52.plot(x,yls[4],color="red")
        
        ax6.plot(x,ytv[5],color="green")
        ax6.plot(x,ypred[5],color="black")
        ax62=ax6.twinx()
        ax62.plot(x,yls[5],color="red")
        
        ax7.plot(x,ytv[6],color="green")
        ax7.plot(x,ypred[6],color="black")
        ax72=ax7.twinx()
        ax72.plot(x,yls[6],color="red")
        
        # Fine-tune figure; make subplots close to each other and hide x ticks for
        # all but bottom plot.
        
        #f.subplots_adjust(hspace=0)
        #pyplot.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
        
        '''
        #Two y-axes
        fig = pyplot.figure()
        ax1 = fig.add_subplot(111)
        t = np.arange(0.01, 10.0, 0.01)
        s1 = np.exp(t)
        ax1.plot(t, s1, 'b-')
        ax1.set_xlabel('time (s)')
        # Make the y-axis label and tick labels match the line color.
        ax1.set_ylabel('exp', color='b')
        for tl in ax1.get_yticklabels():
            tl.set_color('b')
        
        
        ax2 = ax1.twinx()
        s2 = np.sin(2*np.pi*t)
        ax2.plot(t, s2, 'r.')
        ax2.set_ylabel('sin', color='r')
        for tl in ax2.get_yticklabels():
            tl.set_color('r')
        '''
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
     
    #Scatter plot of actual vs predicted   
    def generateactualvspredictedplots(self,LSvalues,TVvalues,predTVvalues,weekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        for dayindex in xrange(7):
            ytvday=[]
            ylsday=[]
            ypredday=[]
            for valindex in xrange(len(TVvalues[weekindex][dayindex])):
                ytvday.append(TVvalues[weekindex][dayindex][valindex][1])
                ylsday.append(LSvalues[weekindex][dayindex][valindex][1])
                ypredday.append(predTVvalues[weekindex][dayindex][valindex][1])
            ytv.append(ytvday)
            yls.append(ylsday)
            ypred.append(ypredday)
            
        # Seven subplots sharing both x/y axes
        f, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = pyplot.subplots(7, sharex=False, sharey=True)
        ax1.scatter(ytv[0],ypred[0],color="green")
        ax1.plot(ytv[0],ytv[0],color="red")
        
        ax2.scatter(ytv[1],ypred[1],color="green")
        ax2.plot(ytv[1],ytv[1],color="red")
        
        ax3.scatter(ytv[2],ypred[2],color="green")
        ax3.plot(ytv[2],ytv[2],color="red")
        
        ax4.scatter(ytv[3],ypred[3],color="green")
        ax4.plot(ytv[3],ytv[3],color="red")
        
        ax5.scatter(ytv[4],ypred[4],color="green")
        ax5.plot(ytv[4],ytv[4],color="red")
        
        ax6.scatter(ytv[5],ypred[5],color="green")
        ax6.plot(ytv[5],ytv[5],color="red")
        
        ax7.scatter(ytv[6],ypred[6],color="green")
        ax7.plot(ytv[6],ytv[6],color="red")
        
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
    
    #Generating plots    
    def generateplotsforvarioussmoothingwindows(self,weekdaymapslist,weekdaymapsTV,region,filename):
        windowlengths=[2,3,4,5]
        degrees=[1,2,3,4]
        Xlabel="d"
        Ylabel="$r^2$"
        colors=['black','red','blue','green','grey']
        Y=[]
        Yrand=[]
        plotLabels=[]
        plotLabels.append("Random")
        for length in windowlengths:
            plotLabels.append("Model at $k=$"+str(length))
            smootheddaymapslist,smoothedweekdaystatsmapslist=self.smoothLS(weekdaymapslist,length)
            smootheddaymapsTV,smoothedweekdaystatsmapTV=self.smoothTV(weekdaymapsTV,length)
            y,yrand=self.getplotvaluesforvariousdegrees(smootheddaymapslist,smootheddaymapsTV,region,degrees)
            Y.append(y)
            Yrand.append(yrand)
        finalY=[]
        finalY.append(Yrand[0])
        for y in Y:
            finalY.append(y)
        self.genericlineplot(degrees,finalY,Xlabel,Ylabel,plotLabels,colors,2.0,filename)
    
    def getplotvaluesforvariousdegrees(self,smootheddaymapslist,smootheddaymapsTV,region,degrees):
        y=[]
        yrand=[]
        for deg in degrees:
            dayhourmodelmap,dayerrors,dayrsquareds,dayrsquaredsrandom=self.runpolyregression(smootheddaymapslist, smootheddaymapsTV,region,deg)
            avrsquared,dayavrsquared=self.getaveragemetric(dayrsquareds)
            avrsquaredrandom,dayavrsquaredrandom=self.getaveragemetric(dayrsquaredsrandom)
            y.append(avrsquared)
            yrand.append(avrsquaredrandom)
        return y,yrand
    
    #Plot effect of varying k on model r^2 
    def generatefixeddegreeplotforvariousk(self,weekdaymapslist,weekdaymapsTV,degree,region,filename):
        windowlengths=[1,2,3,4,5]
        Xlabel="$k$"
        Ylabel="$r^2$"
        colors=['red']
        y=[]
        Y=[]
        plotLabels=["$d=1$"]
        for length in windowlengths:
            smootheddaymapslist,smoothedweekdaystatsmapslist=self.smoothLS(weekdaymapslist,length)
            smootheddaymapsTV,smoothedweekdaystatsmapTV=self.smoothTV(weekdaymapsTV,length)
            dayhourmodelmap,dayerrors,dayrsquareds,dayrsquaredsrandom=self.runpolyregression(smootheddaymapslist, smootheddaymapsTV,region,degree)
            avrsquared,dayavrsquared=self.getaveragemetric(dayrsquareds)
            y.append(avrsquared)
        Y.append(y)
        self.genericlineplot(windowlengths,Y,Xlabel,Ylabel,plotLabels,colors,2.0,filename)
            
    def getvaluesforregionlist(self,regionlist,regionvectorsmap,dayindex):
        valslist=[]
        for region in regionlist:
            vals=regionvectorsmap[region][dayindex]
            valslist.append(vals)
        return valslist
    
    def generatepredictionsplot(self,smootheddaymapslist,smootheddaymapsTV,dayhourmodelmaps,indexforindmodels,finalmodels,startweekindex,endweekindex,day,hour,filename):
        LSvals=smootheddaymapslist[0][1][day][hour][startweekindex:endweekindex]
        TVvals=smootheddaymapsTV[day][hour][startweekindex:endweekindex]
        pred=[]
        Y=[]
        for val in LSvals:
            #pred.append(dayhourmodelmaps[indexforindmodels][day,hour](val))
            pred.append(finalmodels[day,hour](val))
        Y.append(LSvals)
        Y.append(TVvals)
        Y.append(pred)
        x=xrange(endweekindex-startweekindex)
        Xlabel="Week"
        Ylabel="Volumes"
        colors=["red","green","black"]
        plotlabels=["LS volumes","TV ratings","Predicted TV ratings"]
        linewidth=2.0
        self.genericlineplot(x,Y,Xlabel,Ylabel,plotlabels,colors,linewidth,filename)
    
    #Ver 2   
    def generatepredictionsplot2(self,order,smootheddaymapslist,smootheddaymapsTV,dayhourmodelmap,indexforindmodels,startweekindex,endweekindex,day,hour,filename):
        LSvals=smootheddaymapslist[0][1][day][hour][startweekindex:endweekindex]
        TVvals=smootheddaymapsTV[day][hour][startweekindex:endweekindex]
        pred=[]
        Y=[]
        for val in LSvals:
            #pred.append(dayhourmodelmaps[indexforindmodels][day,hour](val))
            x=[val]
            if order>1:
                for i in xrange(order-1):
                    x.append(x[0]**(i+2))
                pred.append(dayhourmodelmap[(day,hour)].predict(np.transpose(np.array(x)))[0])
            else:
                pred.append(dayhourmodelmap[day,hour].predict([val])[0])
        Y.append(LSvals)
        Y.append(TVvals)
        Y.append(pred)
        x=xrange(endweekindex-startweekindex)
        Xlabel="Week"
        Ylabel="Volumes"
        colors=["red","green","black"]
        plotlabels=["LS volumes","TV ratings","Predicted TV ratings"]
        linewidth=2.0
        self.genericlineplot(x,Y,Xlabel,Ylabel,plotlabels,colors,linewidth,filename)
          
    def genericlineplot(self,x,Y,Xlabel,Ylabel,plotLabels,colors,linewidth,filename):
        for index in xrange(len(plotLabels)):
            y=Y[index]
            #pyplot.plot(x,y,"-",color=colors[index],label=plotLabels[index],linewidth=linewidth)
            pyplot.plot(x,y,"-",color=colors[index],linewidth=linewidth)
            pyplot.plot(x,y,"o",color=colors[index],linewidth=linewidth)
            pyplot.legend()
            pyplot.xlabel(Xlabel)
            pyplot.ylabel(Ylabel)
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
        
            
    
    

    
        