# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:17:11 2021

@author: pps
"""
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import copy
from statistics import mean
from scipy.signal.windows import blackman
from numpy import pi

class SpecProcess:
    def __init__(self,path,expstyle,filetype='.dat'):
        self.path = path
        self.expstyle = expstyle
        self.filetype = filetype
        self.pathlist = glob.glob(self.path+'/'+'*'+filetype)
        self.filenames = []
        for i in range(0,len(self.pathlist)):
            self.pathlist[i] = self.pathlist[i].replace('\\','/')
            iter1 = re.finditer('/', self.pathlist[i])
            iter2 = re.finditer('_', self.pathlist[i])
            # iter3 = re.finditer('\.dat',name)
            for j in iter1:
                id1 = j
            for k in iter2:
                id2 = k
            # for l in iter3:
                #     id3 = l
            id_backs = id1.end()
            id_unders = id2.start()
            #id_dot = id3.start()
            name = self.pathlist[i][id_backs:id_unders]
            if name in self.filenames:
                continue
            else:
                self.filenames.append(name)              
                
    def loadspecs(self):           
        Xvalue = dict()
        Yvalue = dict()
        Tvalue = dict()
        for i in range(0,len(self.filenames)):
            self.pathname = glob.glob(self.path+'/'+self.filenames[i]+'_*[0-9]'+self.filetype)   
            Nspec = len(self.pathname)
            data0 = np.loadtxt(self.pathname[0])
            Ndata,Ncol = np.shape(data0)
            x_store = np.zeros((Ndata,Nspec))
            y_store = np.zeros((Ndata,Nspec))
            t_store = np.zeros((Ndata,Nspec))
            del Nspec,Ndata
            for j in range(0,len(self.pathname)):
                filenum = str(j+1)
                data = np.loadtxt(self.path+'/'+self.filenames[i]+'_'+filenum+self.filetype)
                x_store[:,j] = data[:,1]
                if Ncol == 3:
                    y_store[:,j] = data[:,2]
                t_store[:,j] = data[:,0]
                del data
            # del self.pathname
            Xvalue[self.filenames[i]] = x_store
            Yvalue[self.filenames[i]] = y_store
            Tvalue[self.filenames[i]] = t_store
        return Xvalue,Yvalue,Tvalue
    
    def avespecs_sam(self,xdata,ydata,tdata):
        xave = dict()
        yave = dict()
        tave = dict()
        for i in range(0,len(self.filenames)):
            xsum = np.sum(xdata[self.filenames[i]],axis=1)
            ysum = np.sum(ydata[self.filenames[i]],axis=1)
            N_scans = np.size(xdata[self.filenames[i]],axis=1)
            xave[self.filenames[i]] = xsum/N_scans
            yave[self.filenames[i]] = ysum/N_scans
            tave[self.filenames[i]] = tdata[self.filenames[i]][:,0]
        return xave,yave,tave
    
    def dict_curve_smooth(self,x):
        x = self.formatinput(x)
        for key,value in x.items():
            n = len(x[key])
            for i in range(0,n-3):
                value[i] = (value[i]+value[i+1]+value[i+2])/3
        return x
    
    # def avespecs_samref(self,xdata,ydata,tdata,Nsam,Nref):
    #     self.samid = list()
    #     self.refid = list()
    #     xave_sam = dict()
    #     yave_sam = dict()
    #     tave_sam = dict()
    #     xave_ref = dict()
    #     yave_ref = dict()
    #     tave_ref = dict() 
    #     for i in range(0,len(self.filenames)):
    #         N_scans = np.size(xdata[self.filenames[i]],axis=1)
    #         N_dps = np.size(xdata[self.filenames[i]],axis=0)
    #         N_cycles = N_scans//(Nsam+Nref)
    #         xsum_sam = np.zeros((N_dps))
    #         ysum_sam = np.zeros((N_dps))
    #         xsum_ref = np.zeros((N_dps))
    #         ysum_ref = np.zeros((N_dps))
    #         if N_scans < (Nsam+Nref):
    #             continue
    #         else:
    #             for j in range(0,N_scans):
    #                 if j % (Nsam+Nref) < Nsam:
    #                     self.samid.append(j)
    #                     xsum_sam = xsum_sam+xdata[self.filenames[i]][:,j]
    #                     ysum_sam = ysum_sam+ydata[self.filenames[i]][:,j]
    #                 else:
    #                     self.refid.append(j)
    #                     xsum_ref = xsum_ref+xdata[self.filenames[i]][:,j]
    #                     ysum_ref = ysum_ref+ydata[self.filenames[i]][:,j]
    #             xave_sam[self.filenames[i]] = xsum_sam/N_cycles/Nsam
    #             yave_sam[self.filenames[i]] = ysum_sam/N_cycles/Nsam
    #             tave_sam[self.filenames[i]] = tdata[self.filenames[i]][:,0]
    #             xave_ref[self.filenames[i]] = xsum_ref/N_cycles/Nref
    #             yave_ref[self.filenames[i]] = ysum_ref/N_cycles/Nref
    #             tave_ref[self.filenames[i]] = tdata[self.filenames[i]][:,Nsam]
    #     return xave_sam,yave_sam,tave_sam,xave_ref,yave_ref,tave_ref
    
    def average_samref(self,x,t,nsam,nref):
        samx = dict()
        samt = dict()
        refx = dict()
        reft = dict()
        comp1 = dict()
        comp2 = dict()
        for key in list(x):
            x_temp = x[key]
            t_temp = t[key]
            self.t_temp=t_temp
            samx_sum = 0
            refx_sum = 0
            self.n_cycle = round(np.size(x_temp,axis=1)/(nsam+nref))
            for i in range(0,np.size(x_temp,axis=1)):
                if i%(nsam+nref) < nsam:
                    samx_sum = x_temp[:,i]+samx_sum
                else:
                    refx_sum = x_temp[:,i]+refx_sum
            samx[key] = samx_sum/self.n_cycle
            samt[key] = t_temp[:,0]
            reft[key] = t_temp[:,nref]
            refx[key] = refx_sum/self.n_cycle
            comp1[key] = samx[key]+refx[key]
            comp2[key] = samx[key]-refx[key]
        return samx,samt,refx,reft,comp1,comp2
    
    def Totalfield(self,xdata,ydata):
        filenames = list(xdata)
        for name in filenames:
            theta = np.arctan(ydata[name]/xdata[name])
            xdata[name] = xdata[name]/np.cos(theta)
        return xdata
                
    
    def plot_dict(self,xvalues,yvalues):
        plt.figure()
        for name in self.filenames:
            plt.plot(xvalues[name],yvalues[name],label=name)
            plt.legend(loc='best',fontsize=5)
            
    def plot_list(self,xvalues,yvalues):
        plt.figure()
        for i in range(len(yvalues)):
            plt.plot(xvalues[i],yvalues[i],label=self.filenames[i])
            plt.legend(loc='best',fontsize=5)
            
    
    
    def polarimetry(self,comp1,comp2,time,idxsam,idxref,idxref_select=[]):
        samx = []
        samsx = []
        samy = []
        samsy = []
        tsam = []
        fsam = []
        refx = []
        refsx = []
        refy = []
        refsy = []
        tref = []
        fref = []
        trans = []
        theta = []
        eta = []
        samnames = []
        refnames = []
        Efield = dict()
        #save sample spectrum data 
        for i in idxsam:
            samx.append(comp1[self.filenames[i]] + comp2[self.filenames[i]])
            samy.append(comp1[self.filenames[i]] - comp2[self.filenames[i]])
            tsam.append(time[self.filenames[i]])
            samnames.append(self.filenames[i])
        #fft sample data and get polarization angle as well as ellipticity  
        for i in range(len(samx)):
            [freq,sx] = self.fftx(samx[i],tsam[i],2)
            [freq,sy] = self.fftx(samy[i],tsam[i],2)
            fsam.append(freq)
            samsx.append(sx)
            samsy.append(sy)
            Ecra = sx + 1j*sy
            Ecri = sx - 1j*sy
            theta.append((np.unwrap(np.angle(Ecra))-np.unwrap(np.angle(Ecri)))/2)
            eta.append((abs(Ecri)-abs(Ecra))/(abs(Ecri)+abs(Ecra)))
            del freq,sx,sy
        #save referene spectrumm data
        if idxref == []:
            for k in idxref:
                k = int(k)
                refx.append(comp1[self.filenames[k]] + comp2[self.filenames[k]])
                refy.append(comp1[self.filenames[k]] - comp2[self.filenames[k]])
                tref.append(time[self.filenames[k]])
                refnames.append(self.filenames[k])
        else:
            for k in idxref_select:
                id1 = int(idxref[k])
                id2 = int(idxref[k+1])
                refx.append(1/2*(comp1[self.filenames[id1]]+comp1[self.filenames[id2]]) + 1/2*(comp2[self.filenames[id1]]+comp2[self.filenames[id2]]))
                refy.append(1/2*(comp1[self.filenames[id1]]+comp1[self.filenames[id2]]) - 1/2*(comp2[self.filenames[id1]]+comp2[self.filenames[id2]]))
                tref.append(time[self.filenames[id1]])
                refnames.append(self.filenames[id1])
        #fft reference data and calculate transmission            
        for i in range(len(tref)):
            [freq,sx] = self.fftx(refx[i],tref[i],2)
            [freq,sy] = self.fftx(refy[i],tref[i],2)
            refsx.append(sx)
            refsy.append(sy)
            fref.append(freq)
            Asam = np.sqrt(abs(samsx[i])**2+abs(samsy[i])**2)
            Aref = np.sqrt(abs(refsx[i])**2+abs(refsy[i])**2)
            trans.append(Asam/Aref)
            del freq,sx,sy
        
        Efield['sam xvalues td'] = samx 
        Efield['sam xvalues fd'] = samsx 
        Efield['sam yvalues td'] = samy
        Efield['sam yvalues fd'] = samsy 
        Efield['sam time axis'] = tsam
        Efield['sam frequency axis'] = fsam
        Efield['ref xvalues td'] = refx 
        Efield['ref xvalues fd'] = refsx 
        Efield['ref yvalues td'] = refy
        Efield['ref yvalues fd'] = refsy 
        Efield['ref time axis'] = tref
        Efield['ref frequency axis'] = fref
        Efield['polarization angles'] = theta
        Efield['Ellipticity angles'] = eta
        Efield['transmission'] = trans
        Efield['sam names'] = samnames
        Efield['ref names'] = refnames
        
        return Efield

    def average_polarimetry_so(self,t,x):
        samx = dict()
        samy = dict()
        tsam = dict()
        refx = dict()
        refy = dict()
        tref = dict()
        sam_comp1=dict()
        sam_comp2=dict()
        ref_comp1=dict()
        ref_comp2=dict()
        # total_field_sam = dict()
        # total_field_ref = dict()
        for key,value in x.items():
            x_temp = value 
            t_temp = t[key]
            sam_comp1_sum = 0
            sam_comp2_sum = 0
            ref_comp1_sum = 0
            ref_comp2_sum = 0
            self.n_cycle = np.ceil(np.size(x_temp,axis=1)/4)
            for i in range(0,np.size(x_temp,axis=1)):
                if i%4 == 0:
                    sam_comp1_sum = x_temp[:,i]+sam_comp1_sum
                if i%4 == 1:
                    ref_comp1_sum = x_temp[:,i]+ref_comp1_sum
                if i%4 == 2:
                    sam_comp2_sum = x_temp[:,i]+sam_comp2_sum
                if i%4 == 3:
                    ref_comp2_sum = x_temp[:,i]+ref_comp2_sum
            sam_comp1[key] = sam_comp1_sum/self.n_cycle
            sam_comp2[key] = sam_comp2_sum/self.n_cycle
            ref_comp1[key] = ref_comp1_sum/self.n_cycle
            ref_comp2[key] = ref_comp2_sum/self.n_cycle
            samx[key] = (sam_comp1_sum-sam_comp2_sum)/self.n_cycle
            samy[key] = (sam_comp1_sum+sam_comp2_sum)/self.n_cycle
            tsam[key] = t_temp[:,0]
            tref[key] = t_temp[:,1]
            refx[key] = (ref_comp1_sum-ref_comp2_sum)/self.n_cycle
            refy[key] = (ref_comp1_sum+ref_comp2_sum)/self.n_cycle
        # for key,value in samx.items():
        #     total_field_sam[key] = np.sqrt(samx[key]**2+samy[key]**2)
        # for key,value in refx.items():
        #     total_field_ref[key] = np.sqrt(refx[key]**2+refy[key]**2)
        return samx,samy,tsam,refx,refy,tref,sam_comp1,sam_comp2,ref_comp1,ref_comp2
    # def getindex(self,freq,E_sam,E_ref,L,E_echo=None,c=3e8):
    #     freq = self.formatinput(freq)
    #     E_sam = self.formatinput(E_sam)
    #     E_ref = self.formatinput(E_ref)
    #     fname = list(freq)[0]
    #     samname = list(E_sam)[0]
    #     refname = list(E_ref)[0]
    #     omega = freq[fname]*2*np.pi
    #     if E_echo is None:
    #         phi = np.unwrap(np.angle(E_sam[samname]/E_ref[refname]))
    #         n = dict()
    #         n[samname] = phi/omega/L*c+1
    #     else:
    #         E_echo = self.formatinput(E_echo)
    #         echoname = list(E_echo)[0]
    #         l = np.linspace(0.9*L,1.1*L,1000)
    #         L0 = np.ones(len(l))*L
    #         phi_sam = np.unwrap(np.angle(E_sam[samname]/E_ref[refname]))
    #         phi_echo = np.unwrap(np.angle(E_echo[echoname]/E_ref[refname]))
    #         n_sam = phi_sam[:,np.newaxis]/omega[:,np.newaxis]/l[np.newaxis,:]*c+1
    #         n_echo = phi_echo[:,np.newaxis]/omega[:,np.newaxis]/l[np.newaxis,:]*c+1                
    #         dn = n_sam-n_echo
    #         for i in range(0,len(freq)):
    #             L0[i] = self.findzeropoints(l,dn[i,:])
    #         n = dict()
    #         n[samname] = phi_sam/omega/L0*c+1
    #     return n
     
    def findzeropoints(self,x,y):
        for i in range(0,len(x)-1):
            x_zeros = []
            if y[i]*y[i+1] <= 0:
               x_zeros.append((x[i]+x[i+1])/2)
        return x_zeros
    
    def specchop(self,x,y,x0,xt):
        idx0 = np.where(x>=x0)[0]
        idxt = np.where(x<=xt)[0]
        x_new = x[idx0:idxt]
        y_new = y[idx0:idxt]
        return x_new,y_new
    
        
    
    def getEfield(self,t0,E0,r_focus,w0,eps0=8.85e-12,c=3e8):
        # r = np.linspace(0,r_focus,100)
        # P = np.zeros((len(t0),len(r)))
        En = E0/max(E0)
        rc = r_focus/1.5
        P = c*eps0*En**2*rc**2/2*(1-np.exp(-r_focus**2/rc**2))
        # for i in range(0,len(r)):
        #     En_r = En*np.exp(-r[i]**2/rc**2)
        #     P[:,i] = c*eps0*En_r**2*np.pi*(r[2]-r[1])*r[i]
        # w_r = np.trapz(P,x=t0,axis=0)
        # w = np.trapz(w_r,x=r)
        w = np.trapz(P,x=t0)
        E_out = np.sqrt(w0/w)/1e5
        return E_out
    
    def formatinput(self,x):
        if type(x) is list:
            x_new = dict()
            for i in range(len(x)):
                name = 'x'+str(i)
                x_new[name] = x[i]
        if type(x) is np.ndarray:
            x_new = dict()
            if np.size(x) == len(x):
                    name = 'x0'
                    x_new[name] = x
            else:
                for i in range(np.size(x,1)):
                    name = 'x'+str(i)
                    x_new[name] = x[:,i]
        if type(x) is dict:
            x_new = x
        return x_new
    
    def transmission(self,sxsam,sxref):
        sxsam = self.formatinput(sxsam)
        sxref = self.formatinput(sxref)
        trans = dict()
        names_sam = list(sxsam)
        names_ref = list(sxref)
        N = len(sxsam)
        for i in range(0,N):
            trans[names_sam[i]] = abs(sxsam[names_sam[i]])/abs(sxref[names_ref[i]])
        return trans
    
    def combinedict(self,xsam,xref,subs='_ref'):
        x_new = dict()
        x_new = copy.deepcopy(xsam) 
        for key,value in xref.items():
            if key in xsam.keys(): 
                key_new = key+subs
                x_new[key_new] = value
            else:
                x_new[key] = value
        return x_new
    
class Basic_functions:
    def __init__(self):
        self.default = 0
        
    def formatinput(self,x):
        if type(x) is list:
            x_new = dict()
            for i in range(len(x)):
                name = 'x'+str(i)
                x_new[name] = x[i]
        if type(x) is np.ndarray:
            x_new = dict()
            if np.size(x) == len(x):
                    name = 'x0'
                    x_new[name] = x
            else:
                for i in range(np.size(x,1)):
                    name = 'x'+str(i)
                    x_new[name] = x[:,i]
        if type(x) is dict:
            x_new = x
        return x_new
    
    def specchop(self,x,y,x0,xt):
        idx0 = np.where(x>=x0)[0][0]
        idxt = np.where(x<=xt)[0][-1]
        x_new = x[idx0:idxt]
        y_new = y[idx0:idxt]
        return x_new,y_new
    
    def findzeropoints(self,x,y):
        for i in range(0,len(x)-1):
            x_zeros = []
            if y[i]*y[i+1] <= 0:
               x_zeros.append((x[i]+x[i+1])/2)
        return np.array(x_zeros)
    
    def find_1st_zero(self,x,y):
        x0 = None
        for i in range(0,len(y)-1):
            if y[i]*y[i+1] <= 0:
               x0 = (x[i]+x[i+1])/2
            if i == len(y)-2 and x0 == None:
                x0 = x[round(len(x)/2)]
        return x0
    
    def getindex(self,freq,E_sam,E_ref,L,E_echo=None,c=3e8):
        freq = self.formatinput(freq)
        self.E_sam = self.formatinput(E_sam)
        self.E_ref = self.formatinput(E_ref)
        fname = list(freq)[0]
        samname = list(self.E_sam)[0]
        refname = list(self.E_ref)[0]
        omega = freq[fname]*2*np.pi*1e12
        if E_echo is None:
            self.phi = np.unwrap((np.angle(E_sam[samname]/E_ref[refname])))
            
            n = dict()
            n[samname] = self.phi/omega/L*c+1
        else:
            self.Lr = np.linspace(0.9*L,1.1*L,1000)
            self.dn = np.zeros(len(self.Lr))
            E_echo = self.formatinput(E_echo)
            echoname = list(E_echo)[0]
            # self.phi_sam = np.unwrap((np.angle(E_sam[samname]/E_ref[refname])),discont=pi/4)
            # self.phi_echo = np.unwrap((np.angle(E_echo[echoname]/E_ref[refname])),discont=pi/4)
            self.phi_sam = (np.angle(E_sam[samname]/E_ref[refname]))
            self.phi_echo = (np.angle(E_echo[echoname]/E_ref[refname]))
            for i in range(0,len(self.Lr)):
                self.n_sam = self.phi_sam/omega/self.Lr[i]*c+1
                self.n_echo = (self.phi_echo/omega/self.Lr[i]*c+1)/3          
                self.dn[i] = np.nanmean(self.n_echo-self.n_sam)
            self.L0 = self.find_1st_zero(self.Lr,self.dn)
            n = dict()
            n[samname] = self.phi_sam/omega/self.L0*c+1
        return n
    
    def getindex_array(self,freq,E_sam,E_ref,L,E_echo=None,c=3e8):
        '''
        Parameters
        ----------
        freq : np.array
            DESCRIPTION.frequency of the spectrums
        E_sam : np.array
            DESCRIPTION.sample spectrum
        E_ref : np.array
            DESCRIPTION.reference spectrum
        L : float
            DESCRIPTION.initial guess of the sample thickness
        E_echo : np.array, optional
            DESCRIPTION. echo spectrum
        c : float, optional
            DESCRIPTION.speed of light, The default is 3e8.
        Returns
        -------
        n : np.array
            DESCRIPTION. calcullated refractive index
        '''
        omega = freq*2*pi*1e12
        self.freq  = freq
        if E_echo is None: #if there is no echo in the scan
            self.phi = abs(np.unwrap(np.angle(E_sam/E_ref))) #calculate phase of transmission
            n = self.phi/omega/L*c+1 # calculate refractive index
            
        else:
            self.Lr = np.linspace(0.8*L,1.2*L,1000) #create a range of estimated thickness
            self.dn = np.zeros((len(self.freq),len(self.Lr))) #prepare dn to store the refractive index difference
            # self.L0 = np.zeros(len(self.freq))
            # self.dn_max = np.zeros(len(self.Lr))
            # self.dn_min = np.zeros(len(self.Lr))
            self.phi_sam = np.unwrap((np.angle(E_sam/E_ref)),discont=pi/4) # phase angle of transmission from sample signal
            self.phi_echo = np.unwrap((np.angle(E_echo/E_ref)),discont=pi/4)#phase angle of transmission from echo signal
            # self.phi_sam = (np.angle(E_sam/E_ref))
            # self.phi_echo = (np.angle(E_echo/E_ref))
            for i in range(0,len(self.Lr)):
                self.n_sam = self.phi_sam/omega/self.Lr[i]*c+1  #refractive index calculated from sample signal
                self.n_sam = self.index_normal(self.n_sam)
                self.n_echo = (self.phi_echo/omega/self.Lr[i]*c+1)/3 #refractive index calculated from echo signal
                self.n_echo = self.index_normal(self.n_echo)
                self.dn[:,i] = self.n_echo-self.n_sam # difference of refractive index average over entire frequency range
                # self.dn_max[i] = max(self.n_echo-self.n_sam)
                # self.dn_min[i] = min(self.n_echo-self.n_sam)
            # self.L0 = self.find_1st_zero(self.Lr,self.dn) #get the true thickness by finding the zeros point
            self.L0 = L
            n = self.phi_sam/omega/self.L0*c+1 #use the true thickness to calculate refractive index
            n = self.index_normal(n)
        return n
    
    def index_normal(self,n):
        if n[-1]<1:
            n = n+(1-n[-1])
        else:
            n = n
        return n
        
    def special_unwrap(self,angle,freq,f_t):
        idx_max = np.where(freq>=f_t)[0][0]
        angle = np.hstack((angle[0:idx_max],np.unwrap(angle[idx_max:],discont=pi/4)))
        return angle
    
    def fftx_filter(self,xvalues,tvalues,pad):
        xvalues = self.formatinput(xvalues)
        tvalues = self.formatinput(tvalues)
        self.sx = dict()
        self.freq = dict()
        for name in list(xvalues):
            dim = np.shape(xvalues[name])
            dim2 = np.shape(tvalues[name])
            if len(dim) == 1: 
                blackman_filter = blackman(len(xvalues[name]))
                if len(dim2) == 1:
                    ts = abs(tvalues[name][1]-tvalues[name][0])
                if len(dim2) == 2:
                    ts = abs(tvalues[name][1,0]-tvalues[name][0,0])
                NFFT = int(2**(np.ceil(np.log2(len(tvalues[name])))+pad))
                fs = 1/ts
                xvalue_reduce = xvalues[name]-np.average(xvalues[name])
                xvalue_filtered = xvalue_reduce*blackman_filter
                self.SX = np.fft.fft(xvalue_filtered,n=NFFT)
                self.sx[name] = self.SX[0:int(NFFT/2)]
                self.freq[name] = fs/2*np.linspace(0,1,len(self.sx[name]))
            else:
                blackman_filter = blackman(len(xvalues[name]))
                blackman_filter = blackman_filter[:,np.newaxis]
                if len(dim2) == 1:
                    ts = abs(tvalues[name][1]-tvalues[name][0])
                if len(dim2) == 2:
                    ts = abs(tvalues[name][1,0]-tvalues[name][0,0])
                NFFT = int(2**(np.ceil(np.log2(len(tvalues[name])))+pad))
                fs = 1/ts
                xvalue_reduce = xvalues[name]-np.average(xvalues[name],axis=0)
                xvalue_filtered = xvalue_reduce*blackman_filter
                self.SX = np.fft.fft(xvalue_filtered,n=NFFT,axis=0)
                self.sx[name] = self.SX[0:int(NFFT/2),:]
                self.freq[name] = fs/2*np.linspace(0,1,len(self.sx[name]))
                self.freq[name] = self.freq[name][np.where(self.freq[name]>0.1)]
                self.sx[name] = self.sx[name][np.where(self.freq[name]>0.1)]
        return self.freq,self.sx     
    
    def fftx(self,xvalues,tvalues,pad):
        xvalues = self.formatinput(xvalues)
        tvalues = self.formatinput(tvalues)
        self.sx = dict()
        self.freq = dict()
        for name in list(xvalues):
            dim = np.shape(xvalues[name])
            dim2 = np.shape(tvalues[name])
            if len(dim) == 1: 
                if len(dim2) == 1:
                    ts = abs(tvalues[name][1]-tvalues[name][0])
                if len(dim2) == 2:
                    ts = abs(tvalues[name][1,0]-tvalues[name][0,0])
                NFFT = int(2**(np.ceil(np.log2(len(tvalues[name])))+pad))
                fs = 1/ts
                xvalue_reduce = xvalues[name]-np.average(xvalues[name],axis=0)
                self.SX = np.fft.fft(xvalue_reduce,n=NFFT)
                # self.sx[name] = self.SX
                self.sx[name] = self.SX[0:int(NFFT/2)]
                self.freq[name] = fs/2*np.linspace(0,1,len(self.sx[name]))
                self.freq[name] = self.freq[name][np.where(self.freq[name]>0.1)]
                self.sx[name] = self.sx[name][np.where(self.freq[name]>0.1)]
            else:
                if len(dim2) == 1:
                    ts = abs(tvalues[name][1]-tvalues[name][0])
                if len(dim2) == 2:
                    ts = abs(tvalues[name][1,0]-tvalues[name][0,0])
                NFFT = int(2**(np.ceil(np.log2(len(tvalues[name])))+pad))
                fs = 1/ts
                xvalue_reduce = xvalues[name]-np.average(xvalues[name],axis=0)
                self.SX = np.fft.fft(xvalue_reduce,n=NFFT,axis=0)
                self.sx[name] = self.SX[0:int(NFFT/2),:]
                # self.sx[name] = self.SX
                self.freq[name] = fs/2*np.linspace(0,1,len(self.sx[name]))
                self.freq[name] = self.freq[name][np.where(self.freq[name]>0.1)]
                self.sx[name] = self.sx[name][np.where(self.freq[name]>0.1)]
        return self.freq,self.sx 
    
    def fftx_omega(self,xvalues,tvalues,pad):
        xvalues = self.formatinput(xvalues)
        tvalues = self.formatinput(tvalues)
        self.sx = dict()
        self.omega = dict()
        for name in list(xvalues):
            dim = np.shape(xvalues[name])
            dim2 = np.shape(tvalues[name])
            if len(dim) == 1: 
                if len(dim2) == 1:
                    ts = abs(tvalues[name][1]-tvalues[name][0])
                if len(dim2) == 2:
                    ts = abs(tvalues[name][1,0]-tvalues[name][0,0])
                NFFT = int(2**(np.ceil(np.log2(len(tvalues[name])))+pad))
                fs = 1/ts
                self.SX = 1/2/np.pi*np.fft.fft(xvalues[name],n=NFFT)
                self.sx[name] = self.SX[0:int(NFFT/2)]
                self.omega[name] = 2*np.pi*fs/2*np.linspace(0,1,len(self.sx[name]))
            else:
                if len(dim2) == 1:
                    ts = abs(tvalues[name][1]-tvalues[name][0])
                if len(dim2) == 2:
                    ts = abs(tvalues[name][1,0]-tvalues[name][0,0])
                NFFT = int(2**(np.ceil(np.log2(len(tvalues[name])))+pad))
                fs = 1/ts
                self.SX = 1/2/np.pi*np.fft.fft(xvalues[name],n=NFFT,axis=0)
                self.sx[name] = self.SX[0:int(NFFT/2),:]
                self.omega[name] = 2*np.pi*fs/2*np.linspace(0,1,len(self.sx[name]))
        return self.omega,self.sx
    
    def array_fftx(self,xvalues,tvalues,pad=2):
        ts = abs(tvalues[1]-tvalues[0])
        NFFT = int(2**(np.ceil(np.log2(len(tvalues)))+pad))
        fs = 1/ts
        xvalue_reduce = xvalues-np.average(xvalues)
        SX = np.fft.fft(xvalue_reduce,n=NFFT)
        sx = SX[0:int(NFFT/2)]
        freq = fs/2*np.linspace(0,1,len(sx))
        # freq = freq[np.where(freq>0.1)]
        # sx = sx[np.where(freq>0.1)]
        return freq,sx 
    
    def array_ifftx(self,t,sx):
        # fs = abs(f[1]-f[0])
        NFFT = 2*len(sx)
        # NFFT = int(2**(np.ceil(np.log2(len(f)))))
        # ts = 1/fs
        X = np.fft.ifft(sx,n=NFFT)
        # x = X[0:int(NFFT/2)]
        x = X[0:len(t)]
        # freq = freq[np.where(freq>0.1)]
        # sx = sx[np.where(freq>0.1)]
        return 2*x
    
    def ifftx(self,sxvalues,fvalues,pad):
        sxvalues = self.formatinput(sxvalues)
        fvalues = self.formatinput(fvalues)
        time = dict()
        x = dict()
        for name in list(sxvalues):
            dim1 = np.shape(sxvalues[name])
            dim2 = np.shape(fvalues[name])
            if len(dim1) == 1:
                fs = abs(fvalues[name][1]-fvalues[name][0])
                # NFFT = int(2**(np.ceil(np.log2(len(fvalues[name])))+pad))
                NFFT = 2*len(sxvalues[name])
                ts = 1/fs
                X = np.fft.ifft(sxvalues[name],n=NFFT)
                # x[name] = X[0:int(NFFT/2)]
                x[name] = X
                time[name] = ts/2*np.linspace(0,1,len(x[name]))
            if len(dim1) == 2:
                if len(dim2) == 1:
                    fs = abs(fvalues[name][1]-fvalues[name][0])
                    # NFFT = int(2**(np.ceil(np.log2(len(fvalues[name])))+pad))
                    NFFT = 2*len(sxvalues[name])
                    ts = 1/fs
                    X = np.fft.ifft(sxvalues[name],n=NFFT,axis=0)
                    # x[name] = X[0:int(NFFT/2)]
                    x[name] = X
                    time[name] = ts/2*np.linspace(0,1,len(x[name]))
                if len(dim2) == 2:
                    fs = abs(fvalues[name][1,0]-fvalues[name][0,0])
                    # NFFT = int(2**(np.ceil(np.log2(len(fvalues[name])))+pad))
                    NFFT = 2*len(sxvalues[name])
                    ts = 1/fs
                    X = np.fft.ifft(sxvalues[name],n=NFFT,axis=0)
                    # x[name] = X[0:int(NFFT/2)]
                    x[name] = X
                    time[name] = ts/2*np.linspace(0,1,len(x[name]))
        return x,time
    
    def ifftx_omega(self,sxvalues,omega,pad=0):
        sxvalues = self.formatinput(sxvalues)
        omega = self.formatinput(omega)
        time = dict()
        x = dict()
        for name in list(sxvalues):
            dim1 = np.shape(sxvalues[name])
            dim2 = np.shape(omega[name])
            if len(dim1) == 1:
                fs = abs(omega[name][1]-omega[name][0])/2/np.pi
                NFFT = int(2**(np.ceil(np.log2(len(omega[name])))+pad))
                ts = 1/fs
                X = 2*np.pi*np.fft.ifft(sxvalues[name],n=NFFT)
                x[name] = X[0:int(NFFT/2)]
                time[name] = ts/2*np.linspace(0,1,len(x[name]))
            if len(dim1) == 2:
                if len(dim2) == 1:
                    fs = abs(omega[name][1]-omega[name][0])/2/np.pi
                    NFFT = int(2**(np.ceil(np.log2(len(omega[name])))+pad))
                    ts = 1/fs
                    X = 2*np.pi*np.fft.ifft(sxvalues[name],n=NFFT,axis=0)
                    x[name] = X[0:int(NFFT/2)]
                    time[name] = ts/2*np.linspace(0,1,len(x[name]))
                if len(dim2) == 2:
                    fs = abs(omega[name][1,0]-omega[name][0,0])/2/np.pi
                    NFFT = int(2**(np.ceil(np.log2(len(omega[name])))+pad))
                    ts = 1/fs
                    X = 2*np.pi*np.fft.ifft(sxvalues[name],n=NFFT,axis=0)
                    x[name] = X[0:int(NFFT/2)]
                    time[name] = ts/2*np.linspace(0,1,len(x[name]))
        return x,time
    
    def dict_getabs(self,sxvalues):
        names = list(sxvalues)
        for name in names:
            sxvalues[name] = abs(sxvalues[name])
        return sxvalues
    
    def dict_getreal(self,sxvalues):
        names = list(sxvalues)
        for name in names:
            sxvalues[name] = np.real(sxvalues[name])
        return sxvalues
    
    def dict_total_field(self,sx,sy):
        sall = dict() 
        for key,value in sx.items():
            if key in list(sy):
                sall[key] = np.sqrt(sx[key]**2+sy[key]**2)
        return sall
    
    def spec_sum(self,xvalues):
        xvalues = self.formatinput(xvalues)
        xsum = dict()
        for name in list(xvalues):
            xsum['SO'] = xsum['SO']+xvalues[name]
        return xsum
    
    def array_getderivative(self,xvalues,yvalues):
        xdata = xvalues
        ydata = yvalues
        deri_store = np.zeros(len(xdata))
        for i in range(0,len(xdata)):
            if i == 0:
                deri_store[i] = (ydata[i+1]-ydata[i])/(xdata[i+1]-xdata[i])
            else:
                if i == len(xdata)-1:
                    deri_store[i] = (ydata[i]-ydata[i-1])/(xdata[i]-xdata[i-1])
                else:
                    deri_store[i] = (ydata[i+1]-ydata[i-1])/(xdata[i+1]-xdata[i-1])
        return deri_store
     
    def dict_normalize(self,x):
        x = self.formatinput(x)
        xnew = dict()
        for name in x:
            xnew[name] = x[name]/max(x[name])
        return xnew
                             
    def dict_square(self,x):
        x_sq = dict()
        for key,value in x.items():
            x_sq[key] = x[key]**2
        return x_sq