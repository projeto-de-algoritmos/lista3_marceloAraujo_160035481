import tkinter as tk
from const import *
import glob, os
#!/usr/bin/python3
import time

MAIN_PATH = 'files/'
WINDOW_FORMAT = (16, 9)
WINDOW_TIMES_SIZE = 60
width = None
hight = None
# class Date requires at least month, day and hour as parameters

class FileName(object):
    def __init__(self,name):
        self.name = name

class Date(object):
    def __init__(self, month, day, hour, minute=0, year=None):
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        # if year isn't given, it sets the current year
        if year is None:
            self.year = self.now().year
        else:
            self.year = year
    
    def now(self):
        t = time.localtime(time.time())
        return Date(t[MONTH], t[DAY], t[HOUR], t[MINUTE], t[YEAR])
    
    def getStrDate(self,onlyTime=False, onlyDate=False):
        time = "{}h{}m".format(self.hour, self.minute)
        date = "{}/{}/{}".format(self.day, self.month, self.year)
        if(onlyTime):
            return time
        if(onlyDate):
            return date
        
        return time + ' ' + date
    
    def getSec(self):
        tupleTime = (self.year, self.month, self.day, self.hour, self.minute, 0, 0, 0, 0)
        return time.mktime(tupleTime)
    
def toDate(secs):
    t = time.localtime(secs)
    return Date(t[MONTH], t[DAY], t[HOUR], t[MINUTE], t[YEAR])

def toHourMin(secs):
    h = int(secs / 3600)
    secs = secs % 3600
    m = int(secs / 60)
    if(h==0):
        if(m==0):
            return '0'
        return "{}m".format(m)
    return "{}h{}m".format(h, m)

class Job(object):
    '''
    parameter deadlineDate is a Date object
    parameters hours and minutes are the processing time
    '''
    hours=None
    minutes=None
    deadline=None
    start=None

    def __init__(self, name, hours, minutes, deadlineDate):
        self.name = name
        self.hours = hours
        self.minutes = minutes
        self.setDeadline(deadlineDate)
    
    def setDeadline(self, dt):
        tupleTime = (dt.year, dt.month, dt.day, dt.hour, dt.minute, 0, 0, 0, 0)
        self.deadline = time.mktime(tupleTime)
    
    def setStart(self, start):
        self.start = start
        #self.finish = start + self.time
        #self.lateness = max(0, self.finish-self.deadline)
    
    def getStart(self):
        return self.start
    
    def getFinish(self):
        return self.start + self.hours*3600 + self.minutes*60

    def getLateness(self):
        return max(0, self.getFinish() - self.deadline)
    
    def getStrDeadline(self):
        return toDate(self.deadline).getStrDate()
    
    def getTime(self):
        #if(self.hours > )
        return "{}h{}m".format(self.hours, self.minutes)

def loadJobsFromFile(fileName, jobs):
    #fullPath = "{}{}.txt".format(MAIN_PATH,fileName.strip())
    #print("esse eh o caminho ",fullPath)
    try:
        arq = open("{}.txt".format(fileName),'r')
    except FileNotFoundError as fnf_error:
        print(fnf_error)

    
    lines = arq.readlines()
    ''' in the file:
        |    deadline              |    job         |
        year, month, day, hour, min, name, hours, min
    '''
    
    for job in lines:
        l = job.replace('\n', '').split(',')
        jobs.append(Job(l[5], int(l[6]), int(l[7]), 
            Date(int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[0]))))
    arq.close()
    return True


def valideAndLoad(window, file, filesToRead, jobs, infoText):
    try:
        file.name = filesToRead
        #print("file deu ",file)
        loadJobsFromFile(file.name,jobs)
        #print("terminou de carregar")
        infoText.set("Arquivo selecionado: {}".format(file.name))
        jobs = []
        window.quit()
        window.destroy()
    except:
        print("Erro ao carregar ",file)

def loadFileWindow(file, jobs, jobsFrame, infoText, startTime):
    window = tk.Tk()
    window.title('Carregar arquivo')
    window.geometry('600x800')
    loadFrame = tk.Frame(window)

    label = tk.Label(loadFrame, text='Escreva o nome do arquivo para carregar')#.grid(row=0,column=0)
    entry = tk.Entry(loadFrame)
    loadFileBtm = tk.Button(loadFrame, text='carregar arquivo',
         command=lambda: valideAndLoad(window, file, entry.get(), jobs, infoText))
    
    '''os.chdir('.')
    btns = []
    i = 1
    for files in glob.glob("*.txt"):
        flName = files.replace('.txt','').replace('\n','')
        print(flName)
        btns.append(
        tk.Button(loadFrame, text=flName,
         command=lambda: valideAndLoad(window, file, flName, jobs, infoText))
        )
        btns[i-1].grid(row=i,column=0)
        i = i + 1
    
    '''
    loadFrame.grid(row=0,column=0)
    loadFileBtm.grid(row=1,column=0)
    label.grid(row=0, column=0)
    entry.grid(row=0, column=1)
    
    window.mainloop()
    
    calcMinLateness(jobs, jobsFrame, infoText, startTime)

def valideAndCreate(window, fileName, infoText, jobsFrame, file, jobs, menu):
    try:
        arq = open("{}.txt".format(fileName),"w")
        arq.close()
        infoText.set("Arquivo selecionado: {}".format(fileName))
        jobs = []
        file.name = fileName
        menu.add_command(label='Adicionar',command=lambda:addJob(infoText, jobsFrame, file, jobs, startTime))
        window.quit()
        window.destroy()
    except:
        infoText.set("Erro ao criar arquivo")

def newFileWindow(file, jobs, infoText, jobsFrame, menu):
    #frame.destroy()
    window = tk.Tk()
    window.title('Novo arquivo')
    window.geometry('400x300')
    frame = tk.Frame(window)

    label = tk.Label(frame, text='nome do novo arquivo: ')
    entry = tk.Entry(frame)
    
    fileBtm = tk.Button(frame, text='Criar arquivo',
         command=lambda: valideAndCreate(window, entry.get(), infoText, jobsFrame, file, jobs, menu))
    
    frame.grid(row=0,column=0)
    fileBtm.grid(row=1,column=0)
    label.grid(row=0, column=0)
    entry.grid(row=0, column=1)
    
    
    #file.name = entry.get()
    
    window.mainloop()
    print("foi? ",file)
    #window.quit
    #calcMinLateness(jobs)

def calcMinLateness(jobs, jobsFrame, infoText, startTime):
    print("\nTodas as tarefas:")
    if(jobs == None):
        print("não há tarefas")
        return False
    for job in jobs:
        print("tarefa {}:  tempo = {}, deadline = {}".format(
            job.name, job.getTime(), job.getStrDeadline()))
    print("")

    # sorting jobs by deadline
    jobs = sorted(jobs, key=lambda x: x.deadline)

    #startTime = time.time()
    
    #startTime = Date(MAY, 10, 0).getSec()

    print("Tempo de inicio ",toDate(startTime).getStrDate())
    maxLateness = 0
    maxJob = jobs[0]
    for job in jobs:
        job.setStart(startTime)
        startTime = job.getFinish()
        if (job.getLateness() > maxLateness):
            maxLateness = job.getLateness()
            maxJob = job

    fillJobsFrame(jobs, jobsFrame)

    print("\nTarefas por ordem de deadline\n")
    title = " tarefa | tempo  | deadline        | inicio          | fim             | atraso        "
    print(title)
    for i in range(len(title)):
        print("-",end="")
    print("")
    for job in jobs:
        print(" {:7}| {:7}| {:16}| {:16}| {:16}| {:7}".format(
            job.name,
            job.getTime(),
            toDate(job.deadline).getStrDate(),
            toDate(job.getStart()).getStrDate(),
            toDate(job.getFinish()).getStrDate(),
            toHourMin(job.getLateness())
            )
        )
    infoText.set("Atraso maximo: {}, da tarefa {}".format(toHourMin(maxLateness), maxJob.name))
    print("\natraso maximo ",toHourMin(maxLateness))

def deleteJob(jobs, jobName, jobsFrame, isModded=True):
    print("sera apagado o ",jobName)
    size = len(jobs)
    for i in range(size):
        print("olha o condenado ",jobs[i].name)
        if(jobs[i].name == jobName):
            del jobs[i]
    #for i in jobs:
    #    print("veja a galera ",i.name)
    #jobs.remove(job)
    fillJobsFrame(jobs, jobsFrame, isModded)

def fillJobsFrame(jobs, jobsFrame, isModded=True):
    # tarefa | tempo  | deadline| inicio| fim | atraso
    #print("asdasd",jobsFrame.winfo_children())
    
    for widget in jobsFrame.winfo_children():
        widget.destroy()

    tk.Label(jobsFrame, text='| tarefa').grid(row=0,column=0, sticky=tk.W)
    tk.Label(jobsFrame, text='| tempo').grid(row=0,column=1, sticky=tk.W)
    tk.Label(jobsFrame, text='| deadline').grid(row=0,column=2, sticky=tk.W)
    if(isModded):
        tk.Label(jobsFrame, text='| inicio').grid(row=0,column=3, sticky=tk.W)
        tk.Label(jobsFrame, text='| fim').grid(row=0,column=4, sticky=tk.W)
        tk.Label(jobsFrame, text='| atraso').grid(row=0,column=5, sticky=tk.W)
    
    #size = len(jobs)
    i = 0
    print("temos isso de jobs ",len(jobs))
    for jbs in jobs:
        if(isModded):
            j = "{}|{}|{}|{}|{}|{}".format(
            jbs.name,
            jbs.getTime(),
            toDate(jbs.deadline).getStrDate(),
            toDate(jbs.getStart()).getStrDate(),
            toDate(jbs.getFinish()).getStrDate(),
            toHourMin(jbs.getLateness())
            )
        else:
            j = "{}|{}|{}".format(
                jbs.name,
                jbs.getTime(),
                toDate(jbs.deadline).getStrDate(),
            )
        j = j.split('|')

        tk.Label(jobsFrame, text='| '+j[0]).grid(row=i+1,column=0)
        tk.Label(jobsFrame, text='| '+j[1]).grid(row=i+1,column=1)
        tk.Label(jobsFrame, text='| '+j[2]).grid(row=i+1,column=2)
        if(isModded):
            tk.Label(jobsFrame, text='| '+j[3]).grid(row=i+1,column=3)
            tk.Label(jobsFrame, text='| '+j[4]).grid(row=i+1,column=4)
            tk.Label(jobsFrame, text='| '+j[5]).grid(row=i+1,column=5)
        '''
            tk.Button(jobsFrame, text='excluir',
            command=lambda: deleteJob(jobs, jbs.name, jobsFrame)).grid(row=i+1,column=6)
        else:
            #print("esse ",jbs.name)
            tk.Button(jobsFrame, text='excluir',
            command=lambda: deleteJob(jobs, jbs.name, jobsFrame, False)).grid(row=i+1,column=3)'''
        i = i+1

def addJobToBuff(e, buffJobs, addedJobsFrame):
    # name, hours, minutes, 
    #   deadlineDate =  month, day, hour, minute, year
    
    buffJobs.append(
        Job(
            e[-3].get(),#nome
            int(e[-2].get()),#horas
            int(e[-1].get()),#minutos
            Date(
                int(e[MONTH].get()),
                int(e[DAY].get()),
                int(e[HOUR].get()),
                int(e[MINUTE].get()),
                int(e[YEAR].get())
            )
        )
    )
    e[5].delete(0,tk.END)
    e[6].delete(0,tk.END)
    e[7].delete(0,tk.END)
    
    e[HOUR].delete(0,tk.END)
    e[MINUTE].delete(0,tk.END)
    e[DAY].delete(0,tk.END)
    
    e[YEAR].delete(0,tk.END)
    e[YEAR].insert(0,Date.now(Date).year)
    e[MONTH].delete(0,tk.END)
    e[MONTH].insert(0,Date.now(Date).month)
    e[DAY].delete(0,tk.END)
    e[DAY].insert(0,Date.now(Date).day)
    '''for i in range(8):
        e[i].delete(0,tk.END)
        e[i].insert(0,i)'''

    fillJobsFrame(buffJobs, addedJobsFrame, isModded=False)

def saveJobs(window, buffJobs, jobs, jobsFrame, infoText, startTime):
    jobs = jobs + buffJobs
    buffJobs.clear()
    calcMinLateness(jobs, jobsFrame, infoText, startTime)
    window.destroy()

def addJob(infoText, jobsFrame, file, jobs, startTime, popula=False):
    # addJob(infoText, jobsFrame, jobs)
    #loadFileWindow(file, jobs, jobsFrame, infoText):
    '''if not arquivoCriado:
        infoText.set("Selecione ou crie um arquivo para adicionar tarefas")
        return None'''
    window = tk.Tk()
    window.title('Adicionar jobs')
    wtsize = 50
    width = WINDOW_FORMAT[0]*wtsize
    hight = WINDOW_FORMAT[1]*wtsize
    window.geometry('%dx%d'%(width,hight))

    buffJobs = []

    addedJobsFrame = tk.Frame(window)
    addFrame = tk.Frame(window)
    optionsFrame = tk.Frame(window)

    optionsFrame.grid(row=0,column=0)
    addFrame.grid(row=1,column=0)
    addedJobsFrame.grid(row=2,column=0)
    
    labelCol = 0
    entryCol = 1
    tk.Label(addFrame, text='nome').grid(row=0,column=labelCol)

    tk.Label(addFrame, text='tempo de duração').grid(row=1,column=labelCol)
    tk.Label(addFrame, text='horas').grid(row=2,column=labelCol)
    tk.Label(addFrame, text='min').grid(row=3,column=labelCol)

    tk.Label(addFrame, text='deadline').grid(row=4,column=labelCol)
    tk.Label(addFrame, text='hora').grid(row=5,column=labelCol)
    tk.Label(addFrame, text='minuto').grid(row=6,column=labelCol)
    tk.Label(addFrame, text='dia').grid(row=7,column=labelCol)
    tk.Label(addFrame, text='mes').grid(row=8,column=labelCol)
    tk.Label(addFrame, text='ano').grid(row=9,column=labelCol)
    e = []

    e.append(tk.Entry(addFrame))#0 ano dl
    e.append(tk.Entry(addFrame))#1 mes dl
    e.append(tk.Entry(addFrame))#2 dia dl
    e.append(tk.Entry(addFrame))#3 hora dl
    e.append(tk.Entry(addFrame))#4 min dl
    e.append(tk.Entry(addFrame))#5 nome
    e.append(tk.Entry(addFrame))#6 duração h
    e.append(tk.Entry(addFrame))#7 duração m
    
    e[YEAR].delete(0,tk.END)
    e[YEAR].insert(0,Date.now(Date).year)
    e[MONTH].delete(0,tk.END)
    e[MONTH].insert(0,Date.now(Date).month)
    e[DAY].delete(0,tk.END)
    e[DAY].insert(0,Date.now(Date).day)

    e[HOUR].grid(row=5,column=entryCol)
    e[MINUTE].grid(row=6,column=entryCol)
    e[DAY].grid(row=7,column=entryCol)
    e[MONTH].grid(row=8,column=entryCol)
    e[YEAR].grid(row=9,column=entryCol)
    e[5].grid(row=0,column=entryCol)#nome
    e[6].grid(row=2,column=entryCol)#horas
    e[7].grid(row=3,column=entryCol)#minutos

    if(popula):
        for a in range(4):
            for i in range(8):
                e[i].delete(0,tk.END)
                e[i].insert(0,i)
            e[5].delete(0,tk.END)
            e[5].insert(0,a)
            e[YEAR].delete(0,tk.END)
            e[YEAR].insert(0,Date.now(Date).year)
            e[MONTH].delete(0,tk.END)
            e[MONTH].insert(0,Date.now(Date).month)
            e[DAY].delete(0,tk.END)
            e[DAY].insert(0,Date.now(Date).day)
            addJobToBuff(e, buffJobs, addedJobsFrame)
        saveJobs(window, buffJobs, jobs, jobsFrame, infoText, startTime)
        return False
    
    add = tk.Button(optionsFrame, text='adicionar',
         command=lambda: addJobToBuff(e, buffJobs, addedJobsFrame))
    done = tk.Button(optionsFrame, text='Pronto!',
         command=lambda: saveJobs(window, buffJobs, jobs, jobsFrame, infoText, startTime))
    cancel = tk.Button(optionsFrame, text='cancelar',
         command=lambda: window.destroy())
    add.grid(row=0,column=0)
    done.grid(row=0,column=1)
    cancel.grid(row=0,column=2)
    
    window.mainloop()
    

def saveToFile(file, jobs, infoText):
    #print("aaaaaaaa ",file)
    try:
        arq = open(file,'w')
        for job in jobs:
            arq.write("{},{},{},{},{},{}\n".format(
                job.name,
                job.getTime(),
                toDate(job.deadline).getStrDate(),
                toDate(job.getStart()).getStrDate(),
                toDate(job.getFinish()).getStrDate(),
                toHourMin(job.getLateness())
                )
                )
            arq.close()
    except:
        infoText.set("erro ao salvar dados")

'''def gerar(window, buffJobs, jobs, jobsFrame, infoText, startTime, e):
    for a in range(4):
        for i in range(8):
            jobs.append(
            Job(
                e[-3].get(),#nome
                random.randint(1,200),
                ,#horas
                random.randint(0,int(e[-2].get()))
                int(e[-1].get()),#minutos
                
                Date(
                    int(e[MONTH].get()),
                    int(e[DAY].get()),
                    int(e[HOUR].get()),
                    int(e[MINUTE].get()),
                    int(e[YEAR].get())
                )
            )
            )
            e[HOUR].get()
            e[MINUTE].get()
            e[DAY].get()
            e[MONTH].get()
            e[YEAR].get()
            e[5].get()
            e[6].get()
            e[7].get()
        addJobToBuff(e, buffJobs, addedJobsFrame)
    saveJobs(window, buffJobs, jobs, jobsFrame, infoText, startTime)
'''
'''def random(infoText, jobsFrame, file, jobs, startTime):
    
    window = tk.Tk()
    window.title('Adicionar jobs aleatorios')
    wtsize = 50
    width = WINDOW_FORMAT[0]*wtsize
    hight = WINDOW_FORMAT[1]*wtsize
    window.geometry('%dx%d'%(width,hight))

    buffJobs = []

    addedJobsFrame = tk.Frame(window)
    addFrame = tk.Frame(window)
    optionsFrame = tk.Frame(window)

    optionsFrame.grid(row=0,column=0)
    addFrame.grid(row=1,column=0)
    addedJobsFrame.grid(row=2,column=0)
    
    labelCol = 0
    entryCol = 1
    #tk.Label(addFrame, text='nome').grid(row=0,column=labelCol)

    tk.Label(addFrame, text='tempo de duração máxima').grid(row=1,column=labelCol)
    tk.Label(addFrame, text='horas').grid(row=2,column=labelCol)
    tk.Label(addFrame, text='minutos').grid(row=3,column=labelCol)

    tk.Label(addFrame, text='deadline máximo').grid(row=4,column=labelCol)
    tk.Label(addFrame, text='hora').grid(row=5,column=labelCol)
    tk.Label(addFrame, text='minuto').grid(row=6,column=labelCol)
    tk.Label(addFrame, text='dia').grid(row=7,column=labelCol)
    tk.Label(addFrame, text='mes').grid(row=8,column=labelCol)
    tk.Label(addFrame, text='ano').grid(row=9,column=labelCol)
    e = []

    e.append(tk.Entry(addFrame))#0 ano dl
    e.append(tk.Entry(addFrame))#1 mes dl
    e.append(tk.Entry(addFrame))#2 dia dl
    e.append(tk.Entry(addFrame))#3 hora dl
    e.append(tk.Entry(addFrame))#4 min dl
    e.append(tk.Entry(addFrame))#5 nome
    e.append(tk.Entry(addFrame))#6 duração h
    e.append(tk.Entry(addFrame))#7 duração m
    
    e[YEAR].delete(0,tk.END)
    e[YEAR].insert(0,Date.now(Date).year)
    e[MONTH].delete(0,tk.END)
    e[MONTH].insert(0,Date.now(Date).month)
    e[DAY].delete(0,tk.END)
    e[DAY].insert(0,Date.now(Date).day)

    e[HOUR].grid(row=5,column=entryCol)
    e[MINUTE].grid(row=6,column=entryCol)
    e[DAY].grid(row=7,column=entryCol)
    e[MONTH].grid(row=8,column=entryCol)
    e[YEAR].grid(row=9,column=entryCol)
    e[5].grid(row=0,column=entryCol)#nome
    e[6].grid(row=2,column=entryCol)#horas
    e[7].grid(row=3,column=entryCol)#minutos
    
    done = tk.Button(optionsFrame, text='Pronto!',
         command=lambda: gerar(window, buffJobs, jobs, jobsFrame, infoText, startTime))
    cancel = tk.Button(optionsFrame, text='cancelar',
         command=lambda: window.destroy())
    
    done.grid(row=0,column=0)
    cancel.grid(row=0,column=1)
    
    window.mainloop()'''

def run():
    os.system("clear")
    
    file = FileName('')
    jobs = []
    startTime = time.time()

    root = tk.Tk()
    root.title('atraso minimo')
    width = WINDOW_FORMAT[0]*WINDOW_TIMES_SIZE
    hight = WINDOW_FORMAT[1]*WINDOW_TIMES_SIZE
    root.geometry('%dx%d'%(width,hight))

    jobsFrame = tk.Frame(root)
    infoFrame = tk.Frame(root)

    infoFrame.grid(row=0,column=0)
    
    infoText = tk.StringVar()
    infoText2 = tk.StringVar()
    info1 = tk.Label(infoFrame, textvariable=infoText)
    info2 = tk.Label(infoFrame, textvariable=infoText2)
    
    
    info1.grid(row=0,column=0)
    info2.grid(row=1,column=0)
    jobsFrame.grid(row=1,column=0)
    #fillJobsFrame(jobs, jobsFrame)
    
    infoText2.set('======= tempo de inicio: {} ======='.format(toDate(startTime).getStrDate()))
    menu = tk.Menu(root) 
    root.config(menu=menu) 
    '''filemenu = tk.Menu(menu) 
    menu.add_cascade(label='File', menu=filemenu)
    filemenu.add_command(label='New',command=lambda: newFileWindow(file, jobs, infoText, jobsFrame, menu)) 
    filemenu.add_command(label='Open...',command=lambda: loadFileWindow(file, jobs, jobsFrame, infoText))
    filemenu.add_command(label='Save',command=lambda: saveToFile(file, jobs, infoText)) 
    filemenu.add_separator() 
    filemenu.add_command(label='Save and exit', command=root.quit) 
    helpmenu = tk.Menu(menu) 
    menu.add_cascade(label='Help', menu=helpmenu) 
    helpmenu.add_command(label='About')'''

    menu.add_command(label='Adicionar manualmente',command=lambda:addJob(infoText, jobsFrame, file, jobs, startTime))
    #menu.add_command(label='Gerar tarefas aleatorias',command=lambda:addJob(infoText, jobsFrame, file, jobs, startTime))
    
    #menu.add_command(label='Geração aleatória',command=lambda:addJob(infoText, jobsFrame, file, jobs))
    #menu.add_command(label='Adicionar',command=lambda:addJob(infoText, jobsFrame, file, jobs))
    
    #addJob(infoText, jobsFrame, file, jobs, startTime,True)

    root.mainloop() 

if(__name__ == '__minimizeLateness__'):
    run()
