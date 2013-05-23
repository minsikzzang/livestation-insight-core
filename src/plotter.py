from matplotlib import mpl,pyplot,gridspec,pylab
import numpy as np
import itertools
import math
import csv

class Plotter:
    '''
    classdocs
    '''
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
    
    #Get average error and corr for top performing models
    def getavcorranderrorfortopmodels(self,topmodelsrf,topmodelsreg,dayerrorsrf,daycorrsrf,dayerrorsreg,daycorrsreg):
        topmodelserrorsrf={}
        topmodelscorrsrf={}
        topmodelscorrsreg={}
        topmodelserrorsreg={}
        for day in topmodelsrf:
            modelsrf=topmodelsrf[day]
            modelsreg=topmodelsreg[day]
            corrsrf=[]
            errorsrf=[]
            corrsreg=[]
            errorsreg=[]
            for hourmodel in modelsrf:
                errorsrf.append(dayerrorsrf[day][hourmodel])
                corrsrf.append(daycorrsrf[day][hourmodel])
            topmodelserrorsrf[day]=np.mean(errorsrf)
            topmodelscorrsrf[day]=np.mean(corrsrf)
            
            for hourmodel in modelsreg:
                errorsreg.append(dayerrorsreg[day][hourmodel])
                corrsreg.append(daycorrsreg[day][hourmodel])
            topmodelserrorsreg[day]=np.mean(errorsreg)
            topmodelscorrsreg[day]=np.mean(corrsreg)
            
        return topmodelserrorsrf,topmodelscorrsrf,topmodelserrorsreg,topmodelscorrsreg
        
    
    #Generate residual boxplot, hour window is the number of hours to split and aggregate over
    def generateboxplot(self,hourwindow,LSvalues,TVvalues,predTVvalues,startweekindex,endweekindex,filename):
        weekindexes=list(range(startweekindex,endweekindex))
        dayresiduals={}
        for day in xrange(7):
            dayresiduals[day]=[[] for r in xrange(24)]
        for weekindex in weekindexes:
            for day in TVvalues[weekindex]:
                for hourtupleindex in xrange(len(TVvalues[weekindex][day])):
                    dayresiduals[day][hourtupleindex].append(TVvalues[weekindex][day][hourtupleindex][1]-predTVvalues[weekindex][day][hourtupleindex][1])
                    #hourresiduals[TVvalues[weekindex][day][hourtupleindex][0]]=\
                    #TVvalues[weekindex][day][hourtupleindex][1]-predTVvalues[weekindex][day][hourtupleindex][1]
        
        x=[[] for r in xrange(len(dayresiduals))]
        for day in dayresiduals:
            x[day]=dayresiduals[day]
           
        x2=[[] for r in xrange(len(dayresiduals))]
        for reslistindex in xrange(len(x)):
            xint=[]
            dayxint={}
            for weekindex in xrange(len(x[reslistindex][0])):
                partitioned=[x[reslistindex][i:i+hourwindow] for i in range(0,len(x[reslistindex]),hourwindow)]
            for elem in partitioned:
                x2[reslistindex].append(np.mean(elem))
            
        #f, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = pyplot.subplots(7, sharex=False, sharey=True)
        
        gs = gridspec.GridSpec(5, 6)
        
        '''
        ax1 = pyplot.subplot(gs[0:2,0:5])
        ax1.set_title("Sunday")
        ax2 = pyplot.subplot(gs[3:,0:5])
        ax2.set_title("Monday")
        
        '''
        
        '''
        ax3 = pyplot.subplot(gs[0:2,0:5])
        ax3.set_title("Tuesday")
        ax4 = pyplot.subplot(gs[3:,0:5])
        ax4.set_title("Wednesday")
        '''
        
        ax5 = pyplot.subplot(gs[0:2,0:5])
        ax5.set_title("Thursday")
        ax6 = pyplot.subplot(gs[3:,0:5])
        ax6.set_title("Friday")
        
        '''
        ax7 = pyplot.subplot(gs[0:,0:])
        ax7.set_title("Saturday")
        '''
        '''
        ax1.boxplot(x[0])
        ax2.boxplot(x[1])
        '''
        '''
        ax3.boxplot(x[2])
        ax4.boxplot(x[3])
        '''
        
        ax5.boxplot(x[4])
        ax6.boxplot(x[5])

        '''
        ax7.boxplot(x[6])
        '''
        
        '''
        ax1.boxplot(x2[0])
        ax2.boxplot(x2[1])
        ax3.boxplot(x2[2])
        ax4.boxplot(x2[3])
        ax5.boxplot(x2[4])
        ax6.boxplot(x2[5])
        ax7.boxplot(x2[6])
        '''
        
        '''
        pyplot.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax2.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax2.get_yticklabels(), rotation='horizontal', fontsize=6)
        '''
        
        '''
        pyplot.setp(ax3.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax3.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax4.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax4.get_yticklabels(), rotation='horizontal', fontsize=6)
        '''
        
        
        pyplot.setp(ax5.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax5.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax6.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax6.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        
        '''
        pyplot.setp(ax7.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax7.get_yticklabels(), rotation='horizontal', fontsize=6)
        '''
        
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
                    
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
        #f, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = pyplot.subplots(7, sharex=False, sharey=True)
        gs = gridspec.GridSpec(3,3)
        ax1=pyplot.subplot(gs[0,0])
        ax2=pyplot.subplot(gs[1,0])
        ax3=pyplot.subplot(gs[2,0])
        ax4=pyplot.subplot(gs[0,1])
        ax5=pyplot.subplot(gs[1,1])
        ax6=pyplot.subplot(gs[2,1])
        ax7=pyplot.subplot(gs[0,2])
        
        ax1.set_title("Sunday")
        ax2.set_title("Monday")
        ax3.set_title("Tuesday")
        ax4.set_title("Wednesday")
        ax5.set_title("Thursday")
        ax6.set_title("Friday")
        ax7.set_title("Saturday")
        
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
        
        pyplot.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=6)
        pyplot.setp(ax12.get_yticklabels(), rotation='horizontal', fontsize=6,visible=False)
        
        pyplot.setp(ax2.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax2.get_yticklabels(), rotation='horizontal', fontsize=6)
        pyplot.setp(ax22.get_yticklabels(), rotation='horizontal', fontsize=6,visible=False)
        
        pyplot.setp(ax3.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax3.get_yticklabels(), rotation='horizontal', fontsize=6)
        pyplot.setp(ax32.get_yticklabels(), rotation='horizontal', fontsize=6,visible=False)
        
        pyplot.setp(ax4.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax4.get_yticklabels(), rotation='horizontal', fontsize=6)
        pyplot.setp(ax42.get_yticklabels(), rotation='horizontal', fontsize=6,visible=False)
        
        
        pyplot.setp(ax5.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax5.get_yticklabels(), rotation='horizontal', fontsize=6)
        pyplot.setp(ax52.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax6.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax6.get_yticklabels(), rotation='horizontal', fontsize=6)
        pyplot.setp(ax62.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        
        pyplot.setp(ax7.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax7.get_yticklabels(), rotation='horizontal', fontsize=6)
        pyplot.setp(ax72.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        #pyplot.axes().set_aspect('equal')
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
    
    #Generate plots for a day of the week averaged over a number of weeks
    def generateweekdayplotsaveragedoverweeks(self,dayindex,LSvalues,TVvalues,predTVvalues,startweekindex,endweekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        x=xrange(24)
        daymap={0:"Sunday",
                1:"Monday",
                2:"Tuesday",
                3:"Wednesday",
                4:"Thursday",
                5:"Friday",
                6:"Saturday"}
        
        for weekindex in range(startweekindex,endweekindex+1):
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
        
        ytvav=[sum(i)/len(i) for i in itertools.izip(*ytv)]
        ylsav=[sum(i)/len(i) for i in itertools.izip(*yls)]
        ypredav=[sum(i)/len(i) for i in itertools.izip(*ypred)]
        
        f, (ax1, ax2) = pyplot.subplots(2)
        
        ax1.set_title(daymap[dayindex]+" TV vs Predicted")
        ax2.set_title("Livestation")
        
        ax1.plot(x,ytvav,color="green",linewidth=2.0)
        ax1.plot(x,ytvav,'o',color="green")
        ax1.plot(x,ypredav,color="red",linewidth=2.0)
        ax1.plot(x,ypredav,'o',color="red")
        
        ax2.plot(x,ylsav,color="blue",linewidth=2.0)
        ax2.plot(x,ylsav,'o',color="blue")
        
        pyplot.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=9)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=9)
        
        pyplot.setp(ax2.get_xticklabels(), rotation='vertical', fontsize=9)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=9)
        
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
    
    #Same as above but all weekdays in one plot
    def generateallweekdayplotsaveragedoverweeks(self,LSvalues,TVvalues,predTVvalues,startweekindex,endweekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        #x=xrange(24)*7
        x=xrange(24*7)
        daymap={0:"Sunday",
                1:"Monday",
                2:"Tuesday",
                3:"Wednesday",
                4:"Thursday",
                5:"Friday",
                6:"Saturday"}
        days=xrange(7)
        for dayindex in days:
            ytvday=[]
            ylsday=[]
            ypredday=[]
            for weekindex in range(startweekindex,endweekindex+1):
                ytvweek=[]
                ylsweek=[]
                ypredweek=[]
                for valindex in xrange(len(TVvalues[weekindex][dayindex])):
                    ytvweek.append(TVvalues[weekindex][dayindex][valindex][1])
                    ylsweek.append(LSvalues[weekindex][dayindex][valindex][1])
                    ypredweek.append(predTVvalues[weekindex][dayindex][valindex][1])
                ytvday.append(ytvweek)
                ylsday.append(ylsweek)
                ypredday.append(ypredweek)
        
            ytvav=[sum(i)/len(i) for i in itertools.izip(*ytvday)]
            ylsav=[sum(i)/len(i) for i in itertools.izip(*ylsday)]
            ypredav=[sum(i)/len(i) for i in itertools.izip(*ypredday)]
            
            ytv.append(ytvav)
            yls.append(ylsav)
            ypred.append(ypredav)
            
        ytv=[item for sublist in ytv for item in sublist]
        yls=[item for sublist in yls for item in sublist]
        ypred=[item for sublist in ypred for item in sublist]
        
        f, (ax1, ax2) = pyplot.subplots(2)
        
        #ax1.set_title("TV vs Predicted")
        #ax2.set_title("Livestation")
        
        ax1.plot(x,ytv,color="green",linewidth=1.0)
        #ax1.plot(x,ytv,'o',color="green")
        ax1.plot(x,ypred,color="red",linewidth=1.0)
        #ax1.plot(x,ypred,'o',color="red")
        
        ax2.plot(x,yls,color="blue",linewidth=1.0)
        #ax2.plot(x,yls,'o',color="blue")
        
        pyplot.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=9)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=9)
        
        pyplot.setp(ax2.get_xticklabels(), rotation='vertical', fontsize=9)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=9)
        
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
        
    #Same as above but with LS in same plot
    def generateallweekdayplotsaveragedoverweekssingleplot(self,LSvalues,TVvalues,predTVvalues,startweekindex,endweekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        #x=xrange(24)*7
        x=xrange(24*7)
        daymap={0:"Sunday",
                1:"Monday",
                2:"Tuesday",
                3:"Wednesday",
                4:"Thursday",
                5:"Friday",
                6:"Saturday"}
        days=xrange(7)
        for dayindex in days:
            ytvday=[]
            ylsday=[]
            ypredday=[]
            for weekindex in range(startweekindex,endweekindex+1):
                ytvweek=[]
                ylsweek=[]
                ypredweek=[]
                for valindex in xrange(len(TVvalues[weekindex][dayindex])):
                    ytvweek.append(TVvalues[weekindex][dayindex][valindex][1])
                    ylsweek.append(LSvalues[weekindex][dayindex][valindex][1])
                    ypredweek.append(predTVvalues[weekindex][dayindex][valindex][1])
                ytvday.append(ytvweek)
                ylsday.append(ylsweek)
                ypredday.append(ypredweek)
        
            ytvav=[sum(i)/len(i) for i in itertools.izip(*ytvday)]
            ylsav=[sum(i)/len(i) for i in itertools.izip(*ylsday)]
            ypredav=[sum(i)/len(i) for i in itertools.izip(*ypredday)]
            
            ytv.append(ytvav)
            yls.append(ylsav)
            ypred.append(ypredav)
            
        ytv=[item for sublist in ytv for item in sublist]
        yls=[item for sublist in yls for item in sublist]
        ypred=[item for sublist in ypred for item in sublist]
        
        f, (ax1) = pyplot.subplots(1)
        
        #ax1.set_title("TV vs Predicted")
        #ax2.set_title("Livestation")
        
        ax1.plot(x,ytv,color="green",linewidth=1.0)
        #ax1.plot(x,ytv,'o',color="green")
        ax1.plot(x,ypred,color="red",linewidth=1.0)
        ax1.plot(x,yls,color="blue",linewidth=1.0)
        #ax1.plot(x,ypred,'o',color="red")
        
        #pylab.ylim([0,25000])
        pyplot.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=9)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=9)
        
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
     
    #Generate CSV file for above plot   
    def generatecsvfileforweekdayplots(self,LSvalues,TVvalues,predTVvalues,startweekindex,endweekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        #x=xrange(24)*7
        x=xrange(24*7)
        daymap={0:"Sunday",
                1:"Monday",
                2:"Tuesday",
                3:"Wednesday",
                4:"Thursday",
                5:"Friday",
                6:"Saturday"}
        days=xrange(7)
        for dayindex in days:
            ytvday=[]
            ylsday=[]
            ypredday=[]
            for weekindex in range(startweekindex,endweekindex+1):
                ytvweek=[]
                ylsweek=[]
                ypredweek=[]
                for valindex in xrange(len(TVvalues[weekindex][dayindex])):
                    ytvweek.append(TVvalues[weekindex][dayindex][valindex][1])
                    ylsweek.append(LSvalues[weekindex][dayindex][valindex][1])
                    ypredweek.append(predTVvalues[weekindex][dayindex][valindex][1])
                ytvday.append(ytvweek)
                ylsday.append(ylsweek)
                ypredday.append(ypredweek)
        
            ytvav=[sum(i)/len(i) for i in itertools.izip(*ytvday)]
            ylsav=[sum(i)/len(i) for i in itertools.izip(*ylsday)]
            ypredav=[sum(i)/len(i) for i in itertools.izip(*ypredday)]
            
            ytv.append(ytvav)
            yls.append(ylsav)
            ypred.append(ypredav)
            
        ytv=[item for sublist in ytv for item in sublist]
        yls=[item for sublist in yls for item in sublist]
        ypred=[item for sublist in ypred for item in sublist]
        
        ofile = open(filename, 'wb')
        writer = csv.writer(ofile, delimiter=',')
        
        for valindex in xrange(len(ytv)):
            writer.writerow([ytv[valindex],ypred[valindex],yls[valindex]])
        
    
    #Average percent error by hour over several weeks  
    def plotavpercenterroroverweeks(self,LSvalues,TVvalues,predTVvalues,startweekindex,endweekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        #x=xrange(24)*7
        x=xrange(24*7)
        daymap={0:"Sunday",
                1:"Monday",
                2:"Tuesday",
                3:"Wednesday",
                4:"Thursday",
                5:"Friday",
                6:"Saturday"}
        days=xrange(7)
        for dayindex in days:
            ytvday=[]
            ylsday=[]
            ypredday=[]
            for weekindex in range(startweekindex,endweekindex+1):
                ytvweek=[]
                ylsweek=[]
                ypredweek=[]
                for valindex in xrange(len(TVvalues[weekindex][dayindex])):
                    ytvweek.append(TVvalues[weekindex][dayindex][valindex][1])
                    ylsweek.append(LSvalues[weekindex][dayindex][valindex][1])
                    ypredweek.append(predTVvalues[weekindex][dayindex][valindex][1])
                ytvday.append(ytvweek)
                ylsday.append(ylsweek)
                ypredday.append(ypredweek)
        
            ytvav=[sum(i)/len(i) for i in itertools.izip(*ytvday)]
            ylsav=[sum(i)/len(i) for i in itertools.izip(*ylsday)]
            ypredav=[sum(i)/len(i) for i in itertools.izip(*ypredday)]
            
            ytv.append(ytvav)
            yls.append(ylsav)
            ypred.append(ypredav)
            
        ytv=[item for sublist in ytv for item in sublist]
        yls=[item for sublist in yls for item in sublist]
        ypred=[item for sublist in ypred for item in sublist]
        
        percenterror=[]
        for elemindex in range(len(ytv)):
            if ytv[elemindex]!=0:
                percenterror.append(math.fabs(ytv[elemindex]-ypred[elemindex])/ytv[elemindex])
            else:
                percenterror.append(math.fabs(ytv[elemindex]-ypred[elemindex])/1000)
        
        pyplot.plot(x,percenterror,color="red",linewidth=1.5)
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
    
    #Generate boxplot
    def generateboxplotforhourresiduals(self,LSvalues,TVvalues,predTVvalues,startweekindex,endweekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        #x=xrange(24)*7
        x=xrange(24)
        daymap={0:"Sunday",
                1:"Monday",
                2:"Tuesday",
                3:"Wednesday",
                4:"Thursday",
                5:"Friday",
                6:"Saturday"}
        days=xrange(7)
        #residualsday={}
        residuals=[]
        for dayindex in days:
            ytvday=[]
            ylsday=[]
            residualsday=[]
            ypredday=[]
            for weekindex in range(startweekindex,endweekindex+1):
                ytvweek=[]
                ylsweek=[]
                residualsweek=[]
                ypredweek=[]
                for valindex in xrange(len(TVvalues[weekindex][dayindex])):
                    ytvweek.append(TVvalues[weekindex][dayindex][valindex][1])
                    ylsweek.append(LSvalues[weekindex][dayindex][valindex][1])
                    ypredweek.append(predTVvalues[weekindex][dayindex][valindex][1])
                    residualsweek.append(TVvalues[weekindex][dayindex][valindex][1]-predTVvalues[weekindex][dayindex][valindex][1])
                ytvday.append(ytvweek)
                ylsday.append(ylsweek)
                ypredday.append(ypredweek)
                residualsday.append(residualsweek)
            
            residuals.append(list(itertools.izip(*residualsday)))
            
        residuals=list(itertools.izip(*residuals))
        resfinal=[]
        for reslist in residuals:
            resfinal.append([item for sublist in reslist for item in sublist])
         
        pyplot.boxplot(resfinal)   
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
        
 
    #Generate plots for a day of the week for a specific week    
    def generateweekdayplotforspecificweek(self,dayindex,LSvalues,TVvalues,predTVvalues,weekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        x=xrange(24)
        daymap={0:"Sunday",
                1:"Monday",
                2:"Tuesday",
                3:"Wednesday",
                4:"Thursday",
                5:"Friday",
                6:"Saturday"}
        
        for valindex in xrange(len(TVvalues[weekindex][dayindex])):
            ytv.append(TVvalues[weekindex][dayindex][valindex][1])
            yls.append(LSvalues[weekindex][dayindex][valindex][1])
            ypred.append(predTVvalues[weekindex][dayindex][valindex][1])
        
        f, (ax1, ax2) = pyplot.subplots(2)
        
        ax1.set_title(daymap[dayindex]+" TV vs Predicted")
        ax2.set_title("Livestation")
        
        ax1.plot(x,ytv,color="green",linewidth=2.0)
        ax1.plot(x,ytv,'o',color="green")
        ax1.plot(x,ypred,color="red",linewidth=2.0)
        ax1.plot(x,ypred,'o',color="red")
        
        ax2.plot(x,yls,color="blue",linewidth=2.0)
        ax2.plot(x,yls,'o',color='blue')
        
        pyplot.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=9)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=9)
        
        pyplot.setp(ax2.get_xticklabels(), rotation='vertical', fontsize=9)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=9)
        
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
        
    #Same as above but all days of the week in one plot   
    def generateweekplot(self,LSvalues,TVvalues,predTVvalues,weekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        x=xrange(24*7)
        daymap={0:"Sunday",
                1:"Monday",
                2:"Tuesday",
                3:"Wednesday",
                4:"Thursday",
                5:"Friday",
                6:"Saturday"}
        days=xrange(7)
        for dayindex in days:
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
        
        ytv=[item for sublist in ytv for item in sublist]
        yls=[item for sublist in yls for item in sublist]
        ypred=[item for sublist in ypred for item in sublist]
        
        f, (ax1, ax2) = pyplot.subplots(2)
        
        #ax1.set_title(daymap[dayindex]+" TV vs Predicted")
        #ax2.set_title("Livestation")
        
        ax1.plot(x,ytv,color="green",linewidth=1.0)
        #ax1.plot(x,ytv,'o',color="green")
        ax1.plot(x,ypred,color="red",linewidth=1.0)
        #ax1.plot(x,ypred,'o',color="red")
        
        ax2.plot(x,yls,color="blue",linewidth=1.0)
        #ax2.plot(x,yls,'o',color='blue')
        
        pyplot.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=9)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=9)
        
        pyplot.setp(ax2.get_xticklabels(), rotation='vertical', fontsize=9)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=9)
        
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
        
    #Multiple weeks back to back in single plot
    def generateconsecutiveweeksplot(self,LSvalues,TVvalues,predTVvalues,startweekindex,endweekindex,filename):
        nweeks=endweekindex-startweekindex+1
        x=xrange(24*7*nweeks)
        Ytv=[]
        Ypred=[]
        Yls=[]
        for weekindex in range(startweekindex,endweekindex+1):
            ytv,yls,ypred=self.getvaluesforweek(LSvalues,TVvalues,predTVvalues,weekindex)
            Ytv.append(ytv)
            Yls.append(yls)
            Ypred.append(ypred)
        
        Ytv=[item for sublist in Ytv for item in sublist]
        Yls=[item for sublist in Yls for item in sublist]
        Ypred=[item for sublist in Ypred for item in sublist]
        
        f, (ax1) = pyplot.subplots(1)
        
        ax1.plot(x,Ytv,color="green",linewidth=0.5)
        ax1.plot(x,Ypred,color="red",linewidth=0.5)
        ax1.plot(x,Yls,color="blue",linewidth=1.0)
        #ax1.plot(x,ypred,'o',color="red")
        
        #pyplot.ylim([0,100000])
        #pyplot.xlim([0,2000])
        pyplot.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=9)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=9)
        
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
                  
    #Get values for specific week
    def getvaluesforweek(self,LSvalues,TVvalues,predTVvalues,weekindex):
        ytv=[]
        yls=[]
        ypred=[]
        x=xrange(24*7)
        daymap={0:"Sunday",
                1:"Monday",
                2:"Tuesday",
                3:"Wednesday",
                4:"Thursday",
                5:"Friday",
                6:"Saturday"}
        days=xrange(7)
        for dayindex in days:
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
        
        ytv=[item for sublist in ytv for item in sublist]
        yls=[item for sublist in yls for item in sublist]
        ypred=[item for sublist in ypred for item in sublist]
        
        return ytv,yls,ypred
    
    #Generate CSV file for single week values
    def generatecsvforweek(self,LSvalues,TVvalues,predTVvalues,weekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        x=xrange(24*7)
        daymap={0:"Sunday",
                1:"Monday",
                2:"Tuesday",
                3:"Wednesday",
                4:"Thursday",
                5:"Friday",
                6:"Saturday"}
        days=xrange(7)
        for dayindex in days:
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
        
        ytv=[item for sublist in ytv for item in sublist]
        yls=[item for sublist in yls for item in sublist]
        ypred=[item for sublist in ypred for item in sublist]
        
        ofile = open(filename, 'wb')
        writer = csv.writer(ofile, delimiter=',')
        
        for valindex in xrange(len(ytv)):
            writer.writerow([ytv[valindex],ypred[valindex],yls[valindex]])
    
    #Percent error by hour for a specific week    
    def plotpercenterrorforspecificweek(self,LSvalues,TVvalues,predTVvalues,weekindex,filename):
        ytv=[]
        yls=[]
        ypred=[]
        x=xrange(24*7)
        daymap={0:"Sunday",
                1:"Monday",
                2:"Tuesday",
                3:"Wednesday",
                4:"Thursday",
                5:"Friday",
                6:"Saturday"}
        days=xrange(7)
        for dayindex in days:
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
        
        ytv=[item for sublist in ytv for item in sublist]
        yls=[item for sublist in yls for item in sublist]
        ypred=[item for sublist in ypred for item in sublist]
        
        percenterror=[]
        for elemindex in range(len(ytv)):
            if ytv[elemindex]!=0:
                percenterror.append(math.fabs(ytv[elemindex]-ypred[elemindex])/ytv[elemindex])
            else:
                percenterror.append(math.fabs(ytv[elemindex]-ypred[elemindex])/1000)
        
        pyplot.plot(x,percenterror,color="red",linewidth=1.5)
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
        #f, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = pyplot.subplots(7, sharex=False, sharey=True)
        gs = gridspec.GridSpec(3,3)
        ax1=pyplot.subplot(gs[0,0])
        ax2=pyplot.subplot(gs[1,0])
        ax3=pyplot.subplot(gs[2,0])
        ax4=pyplot.subplot(gs[0,1])
        ax5=pyplot.subplot(gs[1,1])
        ax6=pyplot.subplot(gs[2,1])
        ax7=pyplot.subplot(gs[0,2])
        
        ax1.set_title("Sunday")
        ax2.set_title("Monday")
        ax3.set_title("Tuesday")
        ax4.set_title("Wednesday")
        ax5.set_title("Thursday")
        ax6.set_title("Friday")
        ax7.set_title("Saturday")
        
        ax1.scatter(ytv[0],ypred[0],color="green")
        ax1.plot(ytv[0],ytv[0],color="red")
        x0,x1 = ax1.get_xlim()
        y0,y1 = ax1.get_ylim()
        ax1.set_aspect((x1-x0)/(y1-y0))
        
        ax2.scatter(ytv[1],ypred[1],color="green")
        ax2.plot(ytv[1],ytv[1],color="red")
        x0,x1 = ax2.get_xlim()
        y0,y1 = ax2.get_ylim()
        ax2.set_aspect((x1-x0)/(y1-y0))
        
        ax3.scatter(ytv[2],ypred[2],color="green")
        ax3.plot(ytv[2],ytv[2],color="red")
        x0,x1 = ax3.get_xlim()
        y0,y1 = ax3.get_ylim()
        ax3.set_aspect((x1-x0)/(y1-y0))
        
        ax4.scatter(ytv[3],ypred[3],color="green")
        ax4.plot(ytv[3],ytv[3],color="red")
        x0,x1 = ax4.get_xlim()
        y0,y1 = ax4.get_ylim()
        ax4.set_aspect((x1-x0)/(y1-y0))
        
        ax5.scatter(ytv[4],ypred[4],color="green")
        ax5.plot(ytv[4],ytv[4],color="red")
        x0,x1 = ax5.get_xlim()
        y0,y1 = ax5.get_ylim()
        ax5.set_aspect((x1-x0)/(y1-y0))
        
        ax6.scatter(ytv[5],ypred[5],color="green")
        ax6.plot(ytv[5],ytv[5],color="red")
        x0,x1 = ax6.get_xlim()
        y0,y1 = ax6.get_ylim()
        ax6.set_aspect((x1-x0)/(y1-y0))
        
        ax7.scatter(ytv[6],ypred[6],color="green")
        ax7.plot(ytv[6],ytv[6],color="red")
        x0,x1 = ax7.get_xlim()
        y0,y1 = ax7.get_ylim()
        ax7.set_aspect((x1-x0)/(y1-y0))
        
        pyplot.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax2.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax2.get_yticklabels(), rotation='horizontal', fontsize=6)
        pyplot.setp(ax3.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax3.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax4.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax4.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        
        pyplot.setp(ax5.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax5.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax6.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax6.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        
        pyplot.setp(ax7.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax7.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
    
    #Scatter plot with grouping by hour window  
    def generateactualvspredictedplotsusinghourgrouping(self,nhours,LSvalues,TVvalues,predTVvalues,weekindex,filename):
        reducedTVvalues={}
        reducedpredTVvalues={}
        reducedTVvalues[weekindex]={}
        reducedpredTVvalues[weekindex]={}
        hourvals=[]
        hourpredvals=[]
        for day in TVvalues[weekindex]:
            hourvals=[i[1] for i in TVvalues[weekindex][day]]
            hourpredvals=[i[1] for i in predTVvalues[weekindex][day]]
            
            hourvalsred=[]
            hourpredvalsred=[]
               
            partitionedvals=[hourvals[i:i+nhours] for i in range(0,len(hourvals),nhours)]
            for elemindex in xrange(len(partitionedvals)):
                hourvalsred.append((elemindex,np.mean(partitionedvals[elemindex])))
            reducedTVvalues[weekindex][day]=hourvalsred
            
            partitionedvals=[hourpredvals[i:i+nhours] for i in range(0,len(hourpredvals),nhours)]
            for elemindex in xrange(len(partitionedvals)):
                hourpredvalsred.append((elemindex,np.mean(partitionedvals[elemindex])))
                
            reducedpredTVvalues[weekindex][day]=hourpredvalsred
            
        self.generateactualvspredictedplots(LSvalues,reducedTVvalues,reducedpredTVvalues,weekindex,filename)
    
    #prepare data for scatter plot over all weeks    
    def gettimeslicevalues(self,nhours,LSvalues,TVvalues,predTVvalues,weekindex):
        timeslicevalmap={}
        timeslicepredvalmap={}
        nslices=24/nhours
        for tslice in xrange(nslices):
            timeslicevalmap[tslice]=[]
            timeslicepredvalmap[tslice]=[]
        for day in TVvalues[weekindex]:
            hourvals=[i[1] for i in TVvalues[weekindex][day]]
            hourpredvals=[i[1] for i in predTVvalues[weekindex][day]]
            
            hourvalsred=[]
            hourpredvalsred=[]
               
            partitionedvals=[hourvals[i:i+nhours] for i in range(0,len(hourvals),nhours)]
            for elemindex in xrange(len(partitionedvals)):
                hourvalsred.append((elemindex,np.mean(partitionedvals[elemindex])))
            
            partitionedvals=[hourpredvals[i:i+nhours] for i in range(0,len(hourpredvals),nhours)]
            for elemindex in xrange(len(partitionedvals)):
                hourpredvalsred.append((elemindex,np.mean(partitionedvals[elemindex])))
            
            timeslice=0   
            for valueindex in range(len(hourvalsred)):
                timeslicevalmap[timeslice].append(hourvalsred[valueindex])
                timeslicepredvalmap[timeslice].append(hourpredvalsred[valueindex])
                timeslice=timeslice+1
        return timeslicevalmap,timeslicepredvalmap
    
    #Generate scatter plot for time slots over all weeks           
    def generatescatterplothourgrouping(self,nhours,LSvalues,TVvalues,predTVvalues,startweekindex,endweekindex,filename):
        timeslicevalmaps=[]
        timeslicepredvalmaps=[]
        finaltimeslicevalmap={}
        finaltimeslicepredvalmap={}
        for weekindex in list(range(startweekindex,endweekindex+1)):
            timeslicevalmap,timeslicepredvalmap=self.gettimeslicevalues(nhours,LSvalues,TVvalues,predTVvalues,weekindex)
            timeslicevalmaps.append(timeslicevalmap)
            timeslicepredvalmaps.append(timeslicepredvalmap)
        
        for timesliceindex in xrange(len(timeslicevalmaps[0])):
            valarrays=[]
            predvalarrays=[]
            for timeslicemap in timeslicevalmaps:
                valarrays.append(timeslicemap[timesliceindex])
            timeslicevalaverages=list(np.average(np.array(valarrays),axis=0))
            finaltimeslicevalmap[timesliceindex]=timeslicevalaverages
            
            for timeslicemap in timeslicepredvalmaps:
                predvalarrays.append(timeslicemap[timesliceindex])
            timeslicepredvalaverages=list(np.average(np.array(predvalarrays),axis=0))
            finaltimeslicepredvalmap[timesliceindex]=timeslicepredvalaverages
        
        ytv=[]
        ypred=[]
        for index in xrange(len(finaltimeslicevalmap)):
            ytv.append([i[1] for i in list(finaltimeslicevalmap[index])])
            ypred.append([j[1] for j in list(finaltimeslicepredvalmap[index])])
            
        gs = gridspec.GridSpec(3,3)
        ax1=pyplot.subplot(gs[0,0])
        ax2=pyplot.subplot(gs[1,0])
        ax3=pyplot.subplot(gs[2,0])
        ax4=pyplot.subplot(gs[0,1])
        ax5=pyplot.subplot(gs[1,1])
        ax6=pyplot.subplot(gs[2,1])
        ax7=pyplot.subplot(gs[0,2])
        ax8=pyplot.subplot(gs[1,2])
        
        ax1.set_title("00-03")
        ax2.set_title("03-06")
        ax3.set_title("06-09")
        ax4.set_title("09-12")
        ax5.set_title("12-15")
        ax6.set_title("15-18")
        ax7.set_title("18-21")
        ax8.set_title("21-00")
        
        ax1.scatter(ytv[0],ypred[0],color="green")
        ax1.plot(ytv[0],ytv[0],color="red")
        x0,x1 = ax1.get_xlim()
        y0,y1 = ax1.get_ylim()
        ax1.set_aspect((x1-x0)/(y1-y0))
        
        ax2.scatter(ytv[1],ypred[1],color="green")
        ax2.plot(ytv[1],ytv[1],color="red")
        x0,x1 = ax2.get_xlim()
        y0,y1 = ax2.get_ylim()
        ax2.set_aspect((x1-x0)/(y1-y0))
        
        ax3.scatter(ytv[2],ypred[2],color="green")
        ax3.plot(ytv[2],ytv[2],color="red")
        x0,x1 = ax3.get_xlim()
        y0,y1 = ax3.get_ylim()
        ax3.set_aspect((x1-x0)/(y1-y0))
        
        ax4.scatter(ytv[3],ypred[3],color="green")
        ax4.plot(ytv[3],ytv[3],color="red")
        x0,x1 = ax4.get_xlim()
        y0,y1 = ax4.get_ylim()
        ax4.set_aspect((x1-x0)/(y1-y0))
        
        ax5.scatter(ytv[4],ypred[4],color="green")
        ax5.plot(ytv[4],ytv[4],color="red")
        x0,x1 = ax5.get_xlim()
        y0,y1 = ax5.get_ylim()
        ax5.set_aspect((x1-x0)/(y1-y0))
        
        ax6.scatter(ytv[5],ypred[5],color="green")
        ax6.plot(ytv[5],ytv[5],color="red")
        x0,x1 = ax6.get_xlim()
        y0,y1 = ax6.get_ylim()
        ax6.set_aspect((x1-x0)/(y1-y0))
        
        ax7.scatter(ytv[6],ypred[6],color="green")
        ax7.plot(ytv[6],ytv[6],color="red")
        x0,x1 = ax7.get_xlim()
        y0,y1 = ax7.get_ylim()
        ax7.set_aspect((x1-x0)/(y1-y0))
        
        ax8.scatter(ytv[7],ypred[7],color="green")
        ax8.plot(ytv[7],ytv[7],color="red")
        x0,x1 = ax8.get_xlim()
        y0,y1 = ax8.get_ylim()
        ax8.set_aspect((x1-x0)/(y1-y0))
        
        pyplot.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax2.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax2.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax3.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax3.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax4.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax4.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax5.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax5.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax6.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax6.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax7.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax7.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax8.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax8.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
        
    #Generate box plot across whole period characterizing by time bins
    def generateboxplotbyhourgroups(self,nhours,LSvalues,TVvalues,predTVvalues,startweekindex,endweekindex,filename):
        timeslicevalmaps=[]
        timeslicepredvalmaps=[]
        finalresidualsmap={}
        finaltimeslicevalmap={}
        finaltimeslicepredvalmap={}
        for weekindex in list(range(startweekindex,endweekindex+1)):
            timeslicevalmap,timeslicepredvalmap=self.gettimeslicevalues(nhours,LSvalues,TVvalues,predTVvalues,weekindex)
            timeslicevalmaps.append(timeslicevalmap)
            timeslicepredvalmaps.append(timeslicepredvalmap)
        
        for timesliceindex in xrange(len(timeslicevalmaps[0])):
            valarrays=[]
            predvalarrays=[]
            residuals=[]
            for timeslicemap in timeslicevalmaps:
                valarrays.append(timeslicemap[timesliceindex])
                
            #timeslicevalaverages=list(np.average(np.array(valarrays),axis=0))
            #finaltimeslicevalmap[timesliceindex]=timeslicevalaverages
            
            for timeslicemap in timeslicepredvalmaps:
                predvalarrays.append(timeslicemap[timesliceindex])
            #timeslicepredvalaverages=list(np.average(np.array(predvalarrays),axis=0))
            
            residuals=[]
            for arrayindex in xrange(len(valarrays)):
                difflist=[]
                for elemindex in xrange(len(valarrays[arrayindex])):
                    difflist.append(valarrays[arrayindex][elemindex][1]-predvalarrays[arrayindex][elemindex][1])
                residuals.append(difflist)
            
            #print residuals
            #print residuals
            residualsaverages=list(np.average(np.array(residuals),axis=0))
            finalresidualsmap[timesliceindex]=residualsaverages
            #finaltimeslicepredvalmap[timesliceindex]=timeslicepredvalaverages
         
        print finalresidualsmap[0]   
        x=[]
        for index in xrange(len(finalresidualsmap)):
            x.append(finalresidualsmap[index])
            
        #print x
            
        gs = gridspec.GridSpec(3,3)
        ax1=pyplot.subplot(gs[0,0])
        ax2=pyplot.subplot(gs[1,0])
        ax3=pyplot.subplot(gs[2,0])
        ax4=pyplot.subplot(gs[0,1])
        ax5=pyplot.subplot(gs[1,1])
        ax6=pyplot.subplot(gs[2,1])
        ax7=pyplot.subplot(gs[0,2])
        ax8=pyplot.subplot(gs[1,2])
        
        ax1.boxplot(x[0])
        ax2.boxplot(x[1])
        ax3.boxplot(x[2])
        ax4.boxplot(x[3])
        ax5.boxplot(x[4])
        ax6.boxplot(x[5])
        ax7.boxplot(x[6])
        ax8.boxplot(x[7])
        
        ax1.set_title("00-03")
        ax2.set_title("03-06")
        ax3.set_title("06-09")
        ax4.set_title("09-12")
        ax5.set_title("12-15")
        ax6.set_title("15-18")
        ax7.set_title("18-21")
        ax8.set_title("21-00")
        
        pyplot.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax1.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax2.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax2.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax3.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax3.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax4.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax4.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax5.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax5.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax6.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax6.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax7.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax7.get_yticklabels(), rotation='horizontal', fontsize=6)
        
        pyplot.setp(ax8.get_xticklabels(), rotation='vertical', fontsize=6)
        pyplot.setp(ax8.get_yticklabels(), rotation='horizontal', fontsize=6)
        
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
      
    #Generate model sensitivity plot  
    def generatesensitivityplot(self,numberofmonths,percentages,averrorpsrf,averrorpsreg,filename):
        x=range(len(percentages))
        ticks=[numberofmonths-i*numberofmonths for i in percentages]
        ticks.reverse()
        #averrorpsrf.reverse()
        #averrorpsreg.reverse()
        pyplot.plot(x,averrorpsreg,"-",color='red',label="Regression",linewidth=2.0)
        pyplot.plot(x,averrorpsreg,"o",color='red',linewidth=2.0)
        pyplot.plot(x,averrorpsrf,"-",color='green',label="RF",linewidth=2.0)
        pyplot.plot(x,averrorpsrf,"o",color='green',linewidth=2.0)
        pyplot.xlabel("Number of months to predict")
        pyplot.ylabel("Average Error")
        pyplot.xticks(range(len(ticks)),ticks)
        pyplot.legend()
        pyplot.savefig(filename,dpi=1000)
        pyplot.show()
        
    def getaverageLSuservolforweek(self,LSvalues,weekindex):
        daymeanvol=[]
        for day in LSvalues[weekindex]:
            daymeanvol.append(np.mean([i[1] for i in LSvalues[weekindex][0]]))
        
        
        
        