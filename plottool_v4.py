
"""
Created on Wed Aug  4 10:00:49 2021

@author: pps
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import scipy as sp
import pandas as pd
import dataprocessor as dp
from scipy.optimize import curve_fit
import scipy.signal as ss
import curfittool as cft
              
class Plottool:
    def __init__(self,frame,xvalues,yvalues, nrow = 1, ncol = 1, xlimits = None, ylimits = None, fontsize = None):
        '''
        

        Parameters
        ----------
        root : tk.Tk()
            DESCRIPTION: tk root to initiate gui base window
        xvalues : dict or list of 1d array or ndarray
            DESCRIPTION: x values to be plotted
        yvalues : dict or list of 1d array or ndarray
            DESCRIPTION: y values to be plotted

        Returns
        -------
        plot of desired axis limit, labels and fonts

        '''
        
        '''global variables'''
        
        self.x = self.formatinput(xvalues)
        self.y = self.formatinput(yvalues)
        self.nrow = nrow
        self.ncol = ncol
        self.plot_num = tk.IntVar()
        self.all_plot_nums = np.arange(0, nrow*ncol, step = 1).tolist()
        self.idx_selectx = tuple([])
        self.idx_selecty = tuple([])
        self.line_weight = tk.IntVar(value = 2)
        self.legendnames = tk.StringVar()
        self.legendnames_display = tk.StringVar(value = 'None')
        self.userlgname = tk.IntVar(value=0)
        self.action = tk.StringVar(value='ready')
        
        self.labelx = tk.StringVar()
        self.labely = tk.StringVar()
        self.xlim_l = tk.DoubleVar()
        self.xlim_h = tk.DoubleVar()
        self.ylim_l = tk.DoubleVar()
        self.ylim_h = tk.DoubleVar()
        
        self.names_y = list(self.y)
        self.names_x = list(self.x)
        self.listvar_x = tk.StringVar(value=self.names_x)
        self.listvar_y = tk.StringVar(value=self.names_y)
        self.text_weight = tk.StringVar(value = 'normal')
        
        self.legendon = tk.IntVar(value=1)
        self.usercolor_switch = tk.IntVar(value=0)
        self.usercolor_value = []
        self.usercolor_varibable = tk.StringVar()
        
        self.selection_x = tk.StringVar(value='Selected x spectrum: \n None')
        self.selection_y = tk.StringVar(value='Selected y spectrum: \n None')
        
        '''
        first window for plot editor
        '''
        self.frame = frame
        self.window = ttk.Labelframe(frame,text='plot editor')
        self.window.grid(column=0,row=0)
        
        
        if fontsize == None:
            self.fontsize_lg = tk.DoubleVar(value = 15)
            self.fontsize_ax = tk.DoubleVar(value = 15)
        else:
            self.fontsize_ax = tk.DoubleVar(value = fontsize)
            self.fontsize_lg = tk.DoubleVar(value = fontsize)
            
        self.gridswitch = tk.IntVar(value = 1)
        
        if xlimits == None and ylimits == None:
            self.autoxlim = tk.IntVar(value = 1)
            self.autoylim = tk.IntVar(value = 1)
        else:
            self.autoxlim = tk.IntVar(value = 0)
            self.autoylim = tk.IntVar(value = 0)
            self.xlim_l.set(xlimits[0])
            self.xlim_h.set(xlimits[1])
            self.ylim_l.set(ylimits[0])
            self.ylim_h.set(ylimits[1])
        
        
        label_usercolor_switch = ttk.Label(self.window,text='user color on')
        label_show_select_x = ttk.Label(self.window,textvariable=self.selection_x)
        label_show_select_y = ttk.Label(self.window,textvariable=self.selection_y)
        button_loadcolors = ttk.Button(self.window,text='load colors by name',command=self.loadcolors)
        button_loadcolors_tuple = ttk.Button(self.window,text='load colors by RGB',command=self.loadcolors_tuple)
        self.usercolor_entry = ttk.Entry(self.window,textvariable=self.usercolor_varibable,width=35)
        
        self.ydata_select = tk.Listbox(self.window,listvariable=self.listvar_y,selectmode='extended',width=35)
        self.xdata_select = tk.Listbox(self.window,listvariable=self.listvar_x,selectmode='extended',width=35)
        self.entry_xlabel = ttk.Entry(self.window,textvariable=self.labelx,width=15)
        self.entry_ylabel = ttk.Entry(self.window,textvariable=self.labely,width=15)
        self.entry_fontsize_lg = ttk.Entry(self.window,textvariable=self.fontsize_lg,width=5)
        self.entry_fontsize_ax = ttk.Entry(self.window,textvariable=self.fontsize_ax,width=5)
        label_line_weight = ttk.Label(self.window, text = 'Line width: ')
        entry_line_weight = ttk.Entry(self.window, textvariable = self.line_weight, width = 5)
        entry_xl = ttk.Entry(self.window,textvariable=self.xlim_l,width=5)
        entry_xh = ttk.Entry(self.window,textvariable=self.xlim_h,width=5)
        entry_yl = ttk.Entry(self.window,textvariable=self.ylim_l,width=5)
        entry_yh = ttk.Entry(self.window,textvariable=self.ylim_h,width=5)
        
        checkbutton_autoxlim = ttk.Checkbutton(self.window,variable=self.autoxlim, text = 'auto x limits')
        checkbutton_autoylim = ttk.Checkbutton(self.window,variable=self.autoylim, text = 'auto y limits')
        checkbutton_legendon = ttk.Checkbutton(self.window,variable=self.legendon, text = 'legend on')
        checkbutton_usercolor_on = ttk.Checkbutton(self.window,variable=self.usercolor_switch, text = 'user color on')
        label_combobox_textweight = ttk.Label(self.window, text = 'text weight:')
        self.combobox_textweight = ttk.Combobox(self.window, textvariable = self.text_weight)
        self.combobox_textweight['value'] = ('bold', 'light', 'heavy', 'normal')
        self.combobox_textweight.bind('<<ComboboxSelected>>', self.new_parem_plot)
        
      
        
        self.label_x = ttk.Label(self.window,text='x-axis name: ')
        self.label_y = ttk.Label(self.window,text='y-axis name: ')
        self.label_font_lg = ttk.Label(self.window,text='legend font size: ')
        self.label_font_ax = ttk.Label(self.window,text='axis font size: ')
        # self.label_grid = ttk.Label(self.window,text='grid on: ')
        self.checkbutton_grid = ttk.Checkbutton(self.window,variable=self.gridswitch, text = 'grid on')
        self.button_plot = ttk.Button(self.window,text='plot',command=self.plotfig)
        button_loadselection_x = ttk.Button(self.window,text='load x selection',command=self.loadselection_x)
        button_loadselection_y = ttk.Button(self.window,text='load y selection',command=self.loadselection_y)
        
        # legendnames part
        label_userlgname = ttk.Label(self.window,text='user defined legend names')
        button_loadlegendnames = ttk.Button(self.window,text='Load names',command=self.loadnames)
        checkbutton_userlegendname = ttk.Checkbutton(self.window,variable=self.userlgname)
        self.entry_legendnames = ttk.Entry(self.window,textvariable=self.legendnames,width=35)
        label_lg_0 = ttk.Label(self.window, text = 'Following labels will be used to replace shown ones: ')
        label_show_loaded_lgs = ttk.Label(self.window, textvariable = self.legendnames_display)
        
        label_combobox_plotnum = ttk.Label(self.window, text = 'Select subplot number to plot: ')
        self.combobox_plot_num = ttk.Combobox(self.window, textvariable = self.plot_num)
        self.combobox_plot_num['values'] = self.all_plot_nums
        
        label_xlim1 = ttk.Label(self.window,text='x from: ')
        label_xlim2 = ttk.Label(self.window,text='to: ')
        label_ylim1 = ttk.Label(self.window,text='y from: ')
        label_ylim2 = ttk.Label(self.window,text='to: ')
        # label_autoxlim = ttk.Label(self.window,text='auto')
        # label_autoylim = ttk.Label(self.window,text='auto')
        
        # label_legendon = ttk.Label(self.window,text='legend on')
        
        
        
        
        self.xdata_select.grid(column=0,row=0,columnspan=3, sticky = 'w')
        self.ydata_select.grid(column=3,row=0,columnspan=3, sticky = 'w')
        button_loadselection_x.grid(column=2,row=1, sticky = 'w')
        button_loadselection_y.grid(column=5,row=1, sticky = 'w')
        self.label_x.grid(column=0,row=2, sticky = 'w')
        self.entry_xlabel.grid(column=1,row=2, sticky = 'w')
        self.label_y.grid(column=2,row=2, sticky = 'w')
        self.entry_ylabel.grid(column=3,row=2, sticky = 'w')
        
        self.label_font_lg.grid(column=0,row=3, sticky = 'w')
        self.entry_fontsize_lg.grid(column=1,row=3, sticky = 'w')
        self.label_font_ax.grid(column=2,row=3, sticky = 'w')
        self.entry_fontsize_ax.grid(column=3,row=3, sticky = 'w')
        label_line_weight.grid(column = 4, row = 3, sticky = 'w')
        entry_line_weight.grid(column = 5, row = 3, sticky = 'w')
        
        label_xlim1.grid(column=0,row=4, sticky = 'w')
        entry_xl.grid(column=1,row=4, sticky = 'w')  
        label_xlim2.grid(column=2,row=4, sticky = 'w')
        entry_xh.grid(column=3,row=4, sticky = 'w') 
        # label_autoxlim.grid(column=4,row=4, sticky = 'w')
        checkbutton_autoxlim.grid(column=5,row=4, sticky = 'w')
        
        
        label_ylim1.grid(column=0,row=5, sticky = 'w')
        entry_yl.grid(column=1,row=5, sticky = 'w')
        label_ylim2.grid(column=2,row=5, sticky = 'w')
        entry_yh.grid(column=3,row=5, sticky = 'w')
        # label_autoylim.grid(column=4,row=5, sticky = 'w')
        checkbutton_autoylim.grid(column=5,row=5, sticky = 'w')
        
        
        
        
        # self.label_grid.grid(column=0,row=6, sticky = 'w')
        self.checkbutton_grid.grid(column=0,row=6, sticky = 'w')
        # label_legendon.grid(column=3,row=6, sticky = 'w')
        checkbutton_legendon.grid(column=1,row=6, sticky = 'w')
        label_combobox_textweight.grid(column  = 2, row = 6)
        self.combobox_textweight.grid(column = 3, row = 6)
        # checkbutton_bold.grid(column = 5, row = 6)
        
        
        label_usercolor_switch.grid(column=0,row=7, sticky = 'w')
        checkbutton_usercolor_on.grid(column=1,row=7, sticky = 'w')
        self.usercolor_entry.grid(column=2,row=7, columnspan = 2, sticky = 'w')
        button_loadcolors.grid(column = 4,row=7, sticky = 'w')
        button_loadcolors_tuple.grid(column = 5,row = 7, sticky = 'w')
        label_show_select_x.grid(column=0,row=8,columnspan=3, sticky = 'w')
        label_show_select_y.grid(column=2,row=8,columnspan=3, sticky = 'w')
        
        
        # grid for legendname parts
        label_userlgname.grid(column=0,row=9, sticky = 'w')
        checkbutton_userlegendname.grid(column=1,row=9)
        self.entry_legendnames.grid(column=2,row=9,columnspan=2, sticky = 'w')
        button_loadlegendnames.grid(column=4,row=9, sticky = 'w')
        label_lg_0.grid(column = 0, row = 10, columnspan = 3, sticky = 'w')
        label_show_loaded_lgs.grid(column = 3, row = 10, sticky = 'w')
        label_combobox_plotnum.grid(column = 3, row = 11, sticky = 'w')
        self.combobox_plot_num.grid(column = 4, row = 11, sticky = 'w')
        self.button_plot.grid(column = 5,row = 11, sticky = 'w')
        
        
        '''
        second window for showing plots
        '''
        self.window2 = ttk.Labelframe(self.frame,text='plot')
        self.window2.grid(column=1,row=0,columnspan = 2, sticky='nsew')
        self.figure, self.ax = plt.subplots(self.nrow, self.ncol, figsize = (14, 9))
        self.canvas0 = FigureCanvasTkAgg(figure = self.figure, master=self.window2)
        # self.canvas0.figure, self.ax = plt.subplots(self.nrow, self.ncol, figsize = (15, 8))
        self.canvas0.get_tk_widget().grid(column=0,row=0,columnspan=10,rowspan=10,sticky='w')
        self.canvas0.draw()
        button_operate_plot = ttk.Button(self.window2,text='examine',command=self.exam_plot)
        button_curvefit = ttk.Button(self.window2, text = 'curve fit', command = self.start_curvefit)



      
        
        button_exportdata = ttk.Button(self.window2,text='Export Data as shown in plot',command=self.export_data)
        
        button_operate_plot.grid(column = 0,row = 12)
        # self.plotall(fig)
        button_curvefit.grid(column = 1, row = 12)
        button_exportdata.grid(column = 4,row = 12)
 
        
    
        
        
        
        '''
        bottom window for status bar
        '''
        self.window6 = tk.Frame(frame)
        self.window6.grid(column=0,row=3, columnspan = 2, sticky = 'n')

        label_status = ttk.Label(self.window6,text='status: ', font = ('Times', 15))
        label_showaction = ttk.Label(self.window6,textvariable=self.action, font=('Times', 15))
        
        label_status.grid(column=0,row=0)
        label_showaction.grid(column=1,row=0, sticky = 'n')
        
    def exam_plot(self):
        root = tk.Toplevel()
        frame = ttk.Frame(root)
        frame.pack(fill=tk.BOTH,expand=True)
        self.canvas1 = FigureCanvasTkAgg(self.canvas0.figure,master=frame)
        self.canvas1.figure = self.canvas0.figure
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH,expand=True)
        self.canvas1.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas1,frame)
    
    def loadcolors(self):
        self.usercolor_value = self.usercolor_varibable.get().split('+')
        self.action.set('colors loaded')
        
    def loadcolors_tuple(self):
        self.usercolor_value = self.usercolor_varibable.get().split('+')
        for i in range(0,len(self.usercolor_value)):
            self.usercolor_value[i] = eval(self.usercolor_value[i])
        self.action.set('colors loaded')
        
    
    def start_curvefit(self):
        new_root = tk.Toplevel(self.frame)
        len_data = len(self.idx_selectx)
        if len_data == 1:
            x = self.x[self.names_x[self.idx_selectx[0]]]
            y = self.y[self.names_y[self.idx_selecty[0]]]
            idx0 = np.where(x>self.xlim_l.get())[0][0]
            idx1 = np.where(x<self.xlim_h.get())[0][-1]
            x = x[idx0:idx1]
            y = y[idx0:idx1]
            self.curfitgo = cft.Curvefit(new_root, x, y)
        else:
            self.action.set('Please only select 1 pair of data to do curve fitting')
        
    def savefit(self):
        self.y_fit_save[self.names_x[self.idx_selectx[0]]] = self.y_fit
        self.para_fit_save[self.names_x[self.idx_selectx[0]]] = self.para_fit
        self.action.set('fit saved')

    
    def loadselection_x(self):
        self.selection_x.set('Selected x spectrums: \n')
        self.idx_selectx = self.xdata_select.curselection()
        for i in self.idx_selectx:
            self.selection_x.set(self.selection_x.get()+self.names_x[i]+'\n')
        self.action.set('x data selected')
        
    def loadselection_y(self):
        self.idx_selecty = self.ydata_select.curselection()
        self.selection_y.set('Selected y spectrums: \n')
        for i in self.idx_selecty:
            self.selection_y.set(self.selection_y.get()+self.names_y[i]+'\n')
        self.action.set('y data selected')
    
    def loadnames(self):
        self.userlegendnames = self.legendnames.get().split('+')
        self.legendnames_display.set(self.legendnames.get().replace('+', '\n'))
        self.action.set('legend names loaded')
        


    def new_parem_plot(self, comboboxx_event):
        mpl.rc('font', weight = self.text_weight.get())
            
            
    def plotfig(self):
        
        # make sure x data and y data are selected
        if len(self.idx_selectx) == 0 or len(self.idx_selecty) == 0:
            self.action.set('Error! please select x and y to be plotted')
            return
        if type(self.ax) is np.ndarray:
            plot0 = self.ax[self.plot_num.get()]
        else:
            plot0 = self.ax
        plot0.cla()
        if self.userlgname.get() == 1:
            if self.usercolor_switch.get() == 1:
                k=0
                if len(self.idx_selectx) == 1:
                    key_x = self.names_x[self.idx_selectx[0]]
                    for i in self.idx_selecty:
                        plot0.plot(self.x[key_x], self.y[self.names_y[i]],
                                   label = self.userlegendnames[k],
                                   color = self.usercolor_value[k], 
                                   linewidth = self.line_weight.get())
                        k=k+1
                else:
                    if len(self.idx_selectx) == len(self.idx_selecty):
                        for i in range(0, len(self.idx_selectx)):
                            key_x = self.names_x[self.idx_selectx[i]]
                            key_y = self.names_y[self.idx_selecty[i]]
                            plot0.plot(self.x[key_x], self.y[key_y], 
                                       label = self.userlegendnames[k], 
                                       color = self.usercolor_value[k],
                                       linewidth = self.line_weight.get())
                            k = k+1
                    else:
                        self.action.set('Error! please select same number of x and y')
            else:
                k=0
                if len(self.idx_selectx) == 1:
                    key_x = self.names_x[self.idx_selectx[0]]
                    for i in self.idx_selecty:
                        plot0.plot(self.x[key_x], self.y[self.names_y[i]],
                                   label = self.userlegendnames[k],
                                   linewidth = self.line_weight.get())
                        k=k+1
                else:
                    if len(self.idx_selectx) == len(self.idx_selecty):
                        for i in range(0, len(self.idx_selectx)):
                            key_x = self.names_x[self.idx_selectx[i]]
                            key_y = self.names_y[self.idx_selecty[i]]
                            plot0.plot(self.x[key_x], self.y[key_y], 
                                       label = self.userlegendnames[k],
                                       linewidth = self.line_weight.get())
                            k = k+1
                    else:
                        self.action.set('Error! please select same number of x and y')
        else:
            if self.usercolor_switch.get() == 0:
                if len(self.idx_selectx) == 1:
                    key_x = self.names_x[self.idx_selectx[0]]
                    for i in self.idx_selecty:
                        plot0.plot(self.x[key_x], self.y[self.names_y[i]],
                                       label = self.names_y[i],
                                       linewidth = self.line_weight.get())
                      
                else:
                    if len(self.idx_selectx) == len(self.idx_selecty):
                        for i in range(0, len(self.idx_selectx)):
                            key_x = self.names_x[self.idx_selectx[i]]
                            key_y = self.names_y[self.idx_selecty[i]]
                            plot0.plot(self.x[key_x], self.y[key_y], 
                                       label = key_y,
                                       linewidth = self.line_weight.get())
                    else:
                        self.action.set('Error! please select same number of x and y')
            else:
                k = 0
                if len(self.idx_selectx) == 1:
                    key_x = self.names_x[self.idx_selectx[0]]
                    for i in self.idx_selecty:
                        plot0.plot(self.x[key_x], self.y[self.names_y[i]], 
                                   label = self.names_y[i], 
                                   color = self.usercolor_value[k],
                                   linewidth = self.line_weight.get())
                        k = k + 1
                else:
                    if len(self.idx_selectx) == len(self.idx_selecty):
                        for i in range(0, len(self.idx_selectx)):
                            key_x = self.names_x[self.idx_selectx[i]]
                            key_y = self.names_y[self.idx_selecty[i]]
                            plot0.plot(self.x[key_x], self.y[key_y], 
                                       label = key_y, 
                                       color = self.usercolor_value[k],
                                       linewidth = self.line_weight.get())
                            k = k + 1
                    else:
                        self.action.set('Error! please select same number of x and y')
        if self.autoxlim.get() == 0:
            plot0.set_xlim(left=float(self.xlim_l.get()),right=float(self.xlim_h.get()))
        if self.autoylim.get() == 0:
            plot0.set_ylim(bottom=float(self.ylim_l.get()),top=float(self.ylim_h.get()))
        plot0.set_xlabel(self.labelx.get(),fontsize = self.fontsize_ax.get())
        plot0.set_ylabel(self.labely.get(),fontsize = self.fontsize_ax.get())
        plot0.tick_params(axis='both', labelsize = self.fontsize_ax.get())
        if self.legendon.get() == 1:
            plot0.legend(loc='upper right',fontsize=self.fontsize_lg.get())
        plot0.grid(self.gridswitch.get())
        
        # self.canvas0.figure.savefig(path+'\\'+'Waveforms_fd.pdf')
        self.canvas0.draw()
        
        if type(self.ax) is np.ndarray:
            self.plot_num = self.plot_num + 1
            
            if  self.plot_num <= self.nrow*self.ncol - 1:
                while self.plot_num in self.lock_num:
                    self.plot_num = self.plot_num + 1
                    if self.plot_num > self.nrow*self.ncol - 1:
                        self.plot_num = 0
            else:
                self.plot_num = 0
                while self.plot_num in self.lock_num:
                    self.plot_num = self.plot_num + 1
                    if self.plot_num > self.nrow*self.ncol - 1:
                        self.plot_num = 0
            
        
            # self.canvas0.figure, self.ax = plt.subplots(self.nrow, self.ncol, figsize = (12,6))
        self.action.set('Figure plotted')
        
    
      
    
    def formatinput(self,x):
        '''
        

        Parameters
        ----------
        x : list or dict or ndarray
            input data to be format into a dict type

        Returns
        -------
        x_new : dict
            output dict type data

        '''
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
        
        if type(x) is pd.core.frame.DataFrame:
            x_new = x
        
        return x_new
    
    def export_data(self):
        '''
        export processed data
        
        '''
        path = tk.filedialog.askdirectory()
        if len(self.idx_selectx) != 1:
            if len(self.idx_selectx) == len(self.idx_selecty):
                for i in range(0, len(self.idx_selectx)):
                    key_x = self.names_x[self.idx_selectx[i]]
                    key_y = self.names_y[self.idx_selecty[i]]
                    newname_x = 'export_' + key_x
                    newname_y = 'export_' + key_y
                    if self.autoxlim.get() == 0:
                        self.x[newname_x],self.y[newname_y] = dp.Basic_functions().specchop(self.x[key_x],self.y[key_y], self.xlim_l.get(), self.xlim_h.get())
                    else:
                        self.x[newname_x] = self.x[key_x]
                        self.y[newname_y] = self.y[key_y]
                    data_output = np.stack((self.x[newname_x],self.y[newname_y]),axis=1)
                    datasave = open(path+ '/' + newname_x + '.dat', 'w')
                    np.savetxt(path + '/' + newname_x + '.dat', data_output)
                    datasave.close()
                    del newname_x,newname_y,datasave,data_output
            else:
                self.action.set('Error! selection same number of x and y')
                        
        else:
            key_x = self.names_x[self.idx_selectx[0]]
            newname_x = 'export_' + key_x
            for i in range(0, len(self.idx_selecty)):
                key_y = self.names_y[self.idx_selecty[i]]
                newname_y = 'export_' + key_y
                if self.autoxlim.get() == 0:
                    self.x[newname_x],self.y[newname_y] = dp.Basic_functions().specchop(self.x[key_x],self.y[key_y], self.xlim_l.get(), self.xlim_h.get())
                else:
                    self.x[newname_x] = self.x[key_x]
                    self.y[newname_y] = self.y[key_y]
                data_output = np.stack((self.x[newname_x],self.y[newname_y]),axis=1)
                datasave = open(path + '/'+ newname_y + '.dat', 'w')
                np.savetxt(path + '/' + newname_y + '.dat', data_output)
                datasave.close()
                del newname_x,newname_y,datasave,data_output
        self.action.set('data exported') 
        
        
        
    def plotall(self,figure):
        plot = figure.add_subplot()
        for i in range(0,len(self.names_x)):
            plot.plot(self.x[self.names_x[i]],self.y[self.names_y[i]],label=self.names_x)
        self.canvas0.draw()   
        
    def linear(self,x,a,b):
        return a*x+b
    
    def poly2(self,x,a,b,c):
        return a*(x-b)**2+c
    
    def poly3(self,x,a,b,c):
        return a*(x-b)**3+c
    
    def poly4(self,x,a,b,c):
        return a*(x-b)**4+c
    
    def sinu(self,x,a,b,c):
        return a*np.sin(b*x+c)
    
    def exponential(self,x,a,b,c):
        return a*np.exp(b*x+c)
    
    def gaussian(self,x,sigma,tau):
        return 1/((np.sqrt(np.pi*2)*sigma))*np.exp(-(x-tau)**2/2/sigma**2)
    
    def modcos(self,x,a,b,c,d,e,f,g):
        return np.cos(2*np.pi*f*x+b)*(a*x**4+g*x**3+c*x**2+d*x+e)

    def modsin(self,x,a,b,c,d,e,f,g):
        return np.sin(2*np.pi*f*x+b)*(a*x**4+g*x**3+c*x**2+d*x+e)
    
    def cosine(self,x,a,b):
        return b*np.cos(2*np.pi*0.8*x+a)
    
    
        
    
    def get_timewindows(self):
        self.timewindow = dict()
        for name in list(self.deri_value):
            self.timewindow[name] = list()
            self.tw_x = self.deri_value[name]
            self.tw_t = self.x[name]
            for i in range(0,len(self.tw_x)-1):
                tw_x1 = self.tw_x[i]
                tw_x2 = self.tw_x[i+1]
                if tw_x1<0 and tw_x2 > 0:
                    self.timewindow[name].append((tw_x1+tw_x2)/2)
                


        
        
# x = np.linspace(1, 10,10)
# y = x**2
# root=tk.Tk()
# window_master=tk.Frame()
# window_master.grid()
# pt=Plottool(window_master, x, y)
# root.mainloop()