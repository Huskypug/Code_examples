import matplotlib.pyplot as plt
from numpy import exp, pi, sqrt, mean
from scipy.optimize import minpack2
from lmfit import Model, Parameters
from tkinter import filedialog
from tkinter import Tk
import xlsxwriter
from os import path, makedirs

# isChecked()
def prog(dd1,dd2,dd3,dd4,dd5,dd6,n1,n2,n3,n4,n5,n6,er1,er2,er3,er4,er5,er6,a1,b1,c1,d1,mol1,mol2,mol3,mol4,mol5,mol6,flag,mina,minb,minc,mind,maxa,maxb,maxc,maxd):
    
    def func3(x,a,b,c,d):
     return ((x-d)/a + (1 + a*Ss/b)/(2*a*a*Ss*c)-sqrt(((1 + a*Ss/b)/(2*a*a*Ss*c))*((1 + a*Ss/b)/(2*a*a*Ss*c))+(x-d)*(a*Ss/b+1)/(a*a*a*Ss*c)-x/(b*a*a*c)))/Ss
    
    def func4(x,a,c,d):
     return ((x-d)/a + (1)/(2*a*a*Ss*c)-sqrt(((1)/(2*a*a*Ss*c))*((1)/(2*a*a*Ss*c))+(x-d)*(1)/(a*a*a*Ss*c)))/Ss
    
    def Html(mu,Rs,Vbi,name,dd,Rsh,result,Sd):      
        SA = result.params['c'].stderr
        SRs = result.params['a'].stderr
        SVbi = result.params['d'].stderr
        Smu=mu*sqrt((SA/Aa)*(SA/Aa)+(Sd/dd)*(Sd/dd))
        mu,Smu = stup2(mu,Smu)
        Rs,SRs = stup2(Rs,SRs)
        Vbi,SVbi = stup2(Vbi,SVbi)
        table0 = """<tr>
          <td><div style='float:left'><table>
          <tr>
            <th>Variable</th>
            <th>Value</th>
            <th>Error</th>
          </tr>
          <tr>
            <td>Sample #</td>
            <td>"""+str(name)+"""</td>
            <td>None</td>
          </tr>
          <tr>
          <tr>
            <td>Thickness(nm)</td>
            <td>"""+str(round(dd*1e9,1))+"""</td>
            <td>"""+str(round(Sd*1e9,1))+"""</td>
          </tr>
          <tr>
            <td>mu(m^2/V/sec)</td>
            <td>"""+str(mu)+"""</td>
            <td>"""+str(Smu)+"""</td>
          </tr>"""
        if (Rsh != -150):
           SRsh = result.params['b'].stderr
           Rsh,SRsh = stup2(Rsh,SRsh)
           table1="""<tr>
            <td>Rsh(Om*m^2)</td>
            <td>"""+str(Rsh)+"""</td>
            <td>"""+str(SRsh)+"""</td>
          </tr>"""
        if (Rsh == -150): table1 = """"""
        table2="""<tr>
            <td>Rs(Om)</td>
            <td>"""+str(Rs)+"""</td>
            <td>"""+str(SRs)+"""</td>
          </tr>
          <tr>
            <td>Vbi(V)</td>
            <td>"""+str(Vbi)+"""</td>
            <td>"""+str(SVbi)+"""</td>
          </tr>
        </table></div>
        </td>
        <td>
        <div style='float:left'>
        <img src=" """+str("graph/graph"+name)+".png"""" " width="500" height="377">
        </div>
        </td>
        </tr>"""
        table = table0 + table1 + table2
        return table	
    
    
    def stup(a3):
      point = 0
      num = 0 
      acc = 0
      for i in range(0,len(str(a3))):
        if str(a3)[i].isdigit():
          if int(str(a3)[i]) != 0:
            acc = i
            num = int(str(a3)[i])
            break
        else:
          point = 1
      if point == 0: return num,acc
      if point == 1: return num,(acc-1)
    
    def stup2(a,Sa):
        temp = int(Sa)
        if temp != 0:
          if ((temp == 1) or (temp == 2)):
            Sa = round(Sa,1)
            a = round(a,1)
          else:
            Sa = round(Sa,0)
            a = round(a,0) 
        
        else:
          num,acc = stup(Sa)
          numa,acca = stup(a)
          if (int(a) == 0) and (acca==0):
            a = a*1000000
            Sa = Sa*1000000
            num,acc = stup(Sa)
            numa,acca = stup(a)
            Sa = Sa/1000000
            a = a/1000000
          if (int(a) != 0) and (acc==0):
            a = a*100
            Sa = Sa*100
            num,acc = stup(Sa)
            numa,acca = stup(a)
            Sa = Sa/100
            a = a/100  
            acc=acc+2
          if((num == 1) or (num == 2)):
            Sa = "%.2g" % Sa
            
            if abs((acca-acc)) == 0:
              a = "%.2g" % a
            if abs((acca-acc)) == 1:
              a = "%.3g" % a
            if abs((acca-acc)) == 2:
              a = "%.4g" % a
            if abs((acca-acc)) == 3:
              a = "%.5g" % a
            if abs((acca-acc)) == 4:
              a = "%.6g" % a
          else:
            Sa = "%.1g" % Sa
            if abs((acca-acc)) == 0:
              a = "%.1g" % a
            if abs((acca-acc)) == 1:
              a = "%.2g" % a
            if abs((acca-acc)) == 2:
              a = "%.3g" % a
            if abs((acca-acc)) == 3:
              a = "%.4g" % a
            if abs((acca-acc)) == 4:
              a = "%.5g" % a
        
        return a,Sa
     
    def exinit():
      		
      return worksheet
    
    def ex(htmlname,result,pinname,row,worksheet,mu,Aa,Rs,Vbi,Sd,dd,flag):    
      col = 0
      SA = result.params['c'].stderr
      Smu=mu*sqrt((SA/Aa)*(SA/Aa)+(Sd/dd)*(Sd/dd))
      worksheet.write(row, col, htmlname)
      worksheet.write(row, col+1,pinname)
      worksheet.write(row, col+2,mu)
      worksheet.write(row, col+3,Smu)
      worksheet.write(row, col+4,Aa)
      worksheet.write(row, col+5,SA)
      worksheet.write(row, col+6,Rs)
      worksheet.write(row, col+7,result.params['a'].stderr)
      worksheet.write(row, col+8,Vbi)
      worksheet.write(row, col+9,result.params['d'].stderr)
      if(flag==0):
          worksheet.write(row, col+10,result.params['b'].value)
          worksheet.write(row, col+11,result.params['b'].stderr)
      
    def setdd(htmlname):      
      if(int(htmlname) == n1):
        dd = dd1 * 1e-9
        Sd = er1 *1e-9
      if(int(htmlname) == n2): 
        dd = dd2 * 1e-9
        Sd = er2 *1e-9
      if(int(htmlname) == n3): 
        dd = dd3 * 1e-9
        Sd = er3 *1e-9
      if(int(htmlname) == n4): 
        dd = dd4 * 1e-9
        Sd = er4 *1e-9
      if(int(htmlname) == n5): 
        dd = dd5 * 1e-9
        Sd = er5 *1e-9
      if(int(htmlname) == n6): 
        dd = dd6 * 1e-9
        Sd = er6 *1e-9
      return dd, Sd
    
    def exnames(worksheet,row,flag):		
      if (flag==1): names = ('mu(m^2*V^-1*sec^-1)','Smu(m^2*V^-1*sec^-1)','A(SI)','SA(SI)','Rs(Om)','SRs(Om)','Vbi(V)','SVbi(V)')      
      if (flag==0): names = ('mu(m^2*V^-1*sec^-1)','Smu(m^2*V^-1*sec^-1)','A(SI)','SA(SI)','Rs(Om)','SRs(Om)','Vbi(V)','SVbi(V)','Rsh(Om*m^2)','SRsh(Om*m^2)')
      col = 0
      for name in (names):
        worksheet.write(row, col+2,name)
        col += 1
    
    def count(myList):
     return len(set(myList))
    
    def frange(start, stop, step):
      i = start
      while i < stop:
          yield i
          i += step
    
    def list_duplicates_of(seq,item):
     start_at = -1
     locs = []
     while True:
         try:
             loc = seq.index(item,start_at+1)
         except ValueError:
             break
         else:
             locs.append(loc)
             start_at = loc
     return locs
    
    
    Tk().withdraw()
    filenames = filedialog.askopenfilenames(filetypes=(("SMA files", "*.sma"),
                                           ("All files", "*.*") ))
    #print(filenames)
    my_path = path.dirname(path.abspath(__file__))
    graph_path =  my_path + "/report/"+str(n1)+str(n2)+str(n3)+str(n4)+str(n5)+str(n6)+"/graph"
    makedirs(path.abspath(graph_path), exist_ok=True)
    txt_path = my_path + "/report/"+str(n1)+str(n2)+str(n3)+str(n4)+str(n5)+str(n6)+"/txts/"
    makedirs(path.abspath(txt_path), exist_ok=True)
    Rsh = -150
    eps=3
    eps0=8.85e-12
    Ss=4.6e-6
    tablefull = """<html>
    <head>
    <style>
    table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
    }
    
    td, th {
        border: 2px solid #000000;
        text-align: left;
        padding: 8px;
    }
    
    tr:nth-child(even) {
        background-color: #ddddff;
    }
    tr:nth-child(odd) {
        background-color: #ffffff;
    }
    </style>
    </head>
    <body><table>"""
    tableend = """</table></body>
    </html>"""
    workbook = xlsxwriter.Workbook(my_path + '/report/'+str(n1)+str(n2)+str(n3)+str(n4)+str(n5)+str(n6)+'/report'+str(n1)+' '+str(n2)+' '+str(n3)+' '+str(n4)+' '+str(n5)+' '+str(n6)+'.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    exnames(worksheet,row,flag)
    
    
    listmol = [mol1,mol2,mol3,mol4,mol5,mol6]
    listn = [n1,n2,n3,n4,n5,n6]
    bad = list_duplicates_of(listn,0)
    for index in sorted(bad, reverse=True):
        del listn[index]
        del listmol[index]
    listdup = []
    for i in range(0,6-len(list_duplicates_of(listn,0))):
     lst = list_duplicates_of(listmol,i)
     if(len(lst) !=0) :listdup.append(lst)	
    nummol = count(listmol)
    if(nummol > 0):
     fig2 = plt.figure(num=2,figsize=(10, 8))
     listmu1 = []
     ax2 = fig2.add_subplot(1,1,1)
     ax2.set_xlim([0.1,5])
     if(nummol > 1):
      listmu2 = [] 
      fig3 = plt.figure(num=3,figsize=(10, 8))
      ax3 = fig3.add_subplot(1,1,1)
      ax3.set_xlim([0.1,5])
      if(nummol > 2):
       listmu3 = []
       fig4 = plt.figure(num=4,figsize=(10, 8))
       ax4 = fig4.add_subplot(1,1,1)
       ax4.set_xlim([0.1,5])
    
    if(n1 != 0): listAa1 = []
    if(n2 != 0): listAa2 = []
    if(n3 != 0): listAa3 = []
    if(n4 != 0): listAa4 = []
    if(n5 != 0): listAa5 = []
    if(n6 != 0): listAa6 = []
    
    
    
    for i in range(0,len(filenames)):
        cnt = 0
        x = []
        xf = []
        y = []
        yf = []
        with open(filenames[i]) as f:
            for line in f:
                cnt = cnt + 1
                if (cnt ==15):
                  sp = line.split()
                  name = sp[1]+sp[2]
                  htmlname = sp[1][:-1]
                  pinname = sp[2]
                if(cnt > 85) and (cnt<127):
                 sp = line.split()
                 x.append(float(sp[0]))
                 y.append(float(sp[1])/Ss) 
                if(cnt > 15) and (cnt<127):
                 sp = line.split()
                 xf.append(float(sp[0]))
                 yf.append(float(sp[1])/Ss) 
        
        if(flag==1):
            gmodel = Model(func4)
            params = gmodel.make_params(a=a1, c=c1, d=d1)
            params['a'].max = maxa
            params['a'].min = mina
            params['c'].min = minc
            params['c'].max = maxc
            params['d'].min = mind
            params['d'].max = maxd
    
            result = gmodel.fit(y, x=x, params=params)
            dd,Sd = setdd(htmlname)
            Aa = result.params['c'].value 
            mu=8*dd*dd*dd*Aa/(9*eps*eps0)
            Rs = result.params['a'].value
            Vbi = result.params['d'].value
        if(flag==0):
            gmodel = Model(func3)
            params = gmodel.make_params(a=a1,b=b1, c=c1, d=d1)
            params['a'].max = maxa
            params['a'].min = mina
            params['b'].min = minb
            params['b'].max = maxb
            params['c'].min = minc
            params['c'].max = maxc
            params['d'].min = mind
            params['d'].max = maxd
    
            result = gmodel.fit(y, x=x, params=params)
            dd,Sd = setdd(htmlname)
            Aa = result.params['c'].value 
            mu=8*dd*dd*dd*Aa/(9*eps*eps0)
            Rs = result.params['a'].value
            Rsh = result.params['b'].value
            Vbi = result.params['d'].value
        
        
        xlg = []
        ylg = []
        f = open(txt_path+str(dd*1E9).split(".")[0]+' '+name+'.smc', 'w')
        for i in range(0,len(yf)):
            ylg.append(yf[i]*dd*dd*dd)
        for i in range(0,len(xf)):
            xlg.append(xf[i]-Vbi-yf[i]*Ss*Rs)
            f.write(str(xlg[i])+' '+str(ylg[i])+'\n')
        row += 1
        ex(htmlname,result,pinname,row,worksheet,mu,Aa,Rs,Vbi,Sd,dd,flag)
        #lin
        fig1 = plt.figure(num=1,figsize=(10, 8))
        plt.plot(xf, yf, 'bo')
        plt.plot(x, result.best_fit, 'r-')
        plt.xlabel('Vlotage, V')
        plt.ylabel('Current density, A/m^2')
        fig1.savefig(graph_path + '/graph'+name+'.png')
        fig1.clf()
        #log
        if(int(pinname)!=1):
         if(int(pinname)!=8): 
           if int(htmlname) in listn[listdup[0][0]:listdup[0][0]+len(listdup[0])]:
           #if((int(htmlname) == n1)or(int(htmlname) == n2)): 
            listmu1.append(mu)
            ax2.loglog(xlg,ylg,label=name)
           if(nummol > 1):
            if int(htmlname) in listn[listdup[1][0]:listdup[1][0]+len(listdup[1])]:
             listmu2.append(mu)
             ax3.loglog(xlg,ylg,label=name)
           if(nummol > 2):
            if int(htmlname) in listn[listdup[2][0]:listdup[2][0]+len(listdup[2])]:
             listmu3.append(mu)
             ax4.loglog(xlg,ylg,label=name)
           if(int(htmlname) == n1):
            listAa1.append(Aa)			   			   
           if(int(htmlname) == n2):
            listAa2.append(Aa)
           if(int(htmlname) == n3):
            listAa3.append(Aa)
           if(int(htmlname) == n4):
            listAa4.append(Aa)
           if(int(htmlname) == n5):
            listAa5.append(Aa)
           if(int(htmlname) == n6):
            listAa6.append(Aa) 
        
        f.close()
        tablefull = tablefull + Html(mu,Rs,Vbi,name,dd,Rsh,result,Sd)
    
    listmeanAa = []
    meanmu1 = mean(listmu1)
    if((nummol > 1)and(listmu2)): meanmu2 = mean(listmu2)
    if((nummol > 2)and(listmu3)): meanmu3 = mean(listmu3)
    if(n1 != 0): listmeanAa.append(mean(listAa1))
    if(n2 != 0): listmeanAa.append(mean(listAa2))
    if(n3 != 0): listmeanAa.append(mean(listAa3))
    if(n4 != 0): listmeanAa.append(mean(listAa4))
    if(n5 != 0): listmeanAa.append(mean(listAa5))
    if(n6 != 0): listmeanAa.append(mean(listAa6))
    newdd = []
    for i in range(0,len(listn)):
     if listn[i] in listn[listdup[0][0]:listdup[0][0]+len(listdup[0])]: 		
      newdd.append(pow(9/8*eps*eps0*meanmu1/listmeanAa[i],1/3)*1e9)
     if((nummol > 1)and(listmu2)): 
      if listn[i] in listn[listdup[1][0]:listdup[1][0]+len(listdup[1])]:
       newdd.append(pow(9/8*eps*eps0*meanmu2/listmeanAa[i],1/3)*1e9)
     if((nummol > 2)and(listmu3)): 
      if listn[i] in listn[listdup[2][0]:listdup[2][0]+len(listdup[2])]:
       newdd.append(pow(9/8*eps*eps0*meanmu3/listmeanAa[i],1/3)*1e9)
    with open(txt_path+'calculated thickness.txt', 'w') as f:
        for i in range(0,len(newdd)):
         print(' dd'+str(i)+': '+str(newdd[i])+'\n')
         f.write(' dd'+str(i)+': '+str(newdd[i])+'\n') 		
    ax2.set_ylim(ymin = abs(min(ylg)))
    if(nummol > 1): ax3.set_ylim(ymin = abs(min(ylg)))
    if(nummol > 2): ax4.set_ylim(ymin = abs(min(ylg)))
    x = list(frange(0.1,5.0,0.1))
    y1 = []
    for i in frange(0.1,5.0,0.1):
       y1.append(9/8*eps*eps0*i*i*meanmu1)					
    ax2.loglog(x,y1,label = 'meanMu',linestyle='--')#x 0.1 to 5  
    ax2.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)  
    ax2.set_xlabel("V-Vbi-I*Rs, V")
    ax2.set_ylabel("(I*d^3)/S, A*m")
    with open(txt_path+'Jd3Vmean_1.smc', 'w') as f:
     for i in range(0,len(x)): 		
      f.write(str(x[i])+" "+str(y1[i])+'\n')
    if((nummol > 1)and(listmu2)): 
     y2 = []
     for i in frange(0.1,5.0,0.1):
        y2.append(9/8*eps*eps0*i*i*meanmu2)
     ax3.loglog(x,y2,label = 'meanMu',linestyle='--')#x 0.1 to 5 
     ax3.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
     ax3.set_xlabel("V-Vbi-I*Rs, V")
     ax3.set_ylabel("(I*d^3)/S, A*m")
     with open(txt_path+'Jd3Vmean_2.smc', 'w') as f:
      for i in range(0,len(x)): 		
       f.write(str(x[i])+" "+str(y2[i])+'\n') 
    if((nummol > 2)and(listmu3)):
     y3 = []
     for i in frange(0.1,5.0,0.1):
        y3.append(9/8*eps*eps0*i*i*meanmu3)
     ax4.loglog(x,y3,label = 'meanMu',linestyle='--')#x 0.1 to 5 
     ax4.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
     ax4.set_xlabel("V-Vbi-I*Rs, V")
     ax4.set_ylabel("(I*d^3)/S, A*m")
     with open(txt_path+'Jd3Vmean_3.smc', 'w') as f:
      for i in range(0,len(x)): 		
       f.write(str(x[i])+" "+str(y3[i])+'\n')

    
    
    fig2.savefig(graph_path + '/graph'+str(listn[listdup[0][0]:listdup[0][0]+len(listdup[0])])+'.png')
    if(nummol > 1): fig3.savefig(graph_path + '/graph'+str(listn[listdup[1][0]:listdup[1][0]+len(listdup[1])])+'.png')
    if(nummol > 2): fig4.savefig(graph_path + '/graph'+str(listn[listdup[2][0]:listdup[2][0]+len(listdup[2])])+'.png')
    tablefig2 = """<tr>
          <td><div style='float:left'><table>
          <tr>
            <th>Variable</th>
            <th>Value</th>
          </tr>
          <tr>
            <td>mean mu """+str(n1)+' '+str(n2)+"""(m^2*V^-1*sec^-1)</td>
            <td>"""+'{:.2e}'.format(float(meanmu1))+"""</td>
          </tr>
        </table></div>
        </td>
        <td>
        <div style='float:left'>
        <img src=" """'graph/graph'+str(listn[listdup[0][0]:listdup[0][0]+len(listdup[0])])+'.png'""" " width="750" height="600">
        </div>
        </td>
        </tr>"""
    tablefig3 = ""
    tablefig4 = "" 
    if((nummol > 1)and(listmu2)): tablefig3 = """<tr>
          <td><div style='float:left'><table>
          <tr>
            <th>Variable</th>
            <th>Value</th>
          </tr>
            <td>mean mu """+str(n3)+' '+str(n4)+"""(m^2*V^-1*sec^-1)</td>
            <td>"""+'{:.2e}'.format(float(meanmu2))+"""</td>
          </tr>
        </table></div>
        </td>
        <td>
        <div style='float:left'>
        <img src=" """'graph/graph'+str(listn[listdup[1][0]:listdup[1][0]+len(listdup[1])])+'.png'""" " width="750" height="600">
        </div>
        </td>
        </tr>"""  
    if((nummol > 2)and(listmu3)): tablefig4 = """<tr>
          <td><div style='float:left'><table>
          <tr>
            <th>Variable</th>
            <th>Value</th>
          </tr>
            <td>mean mu """+str(n5)+' '+str(n6)+"""(m^2*V^-1*sec^-1)</td>
            <td>"""'{:.2e}'.format(float(meanmu3))+"""</td>
          </tr>
        </table></div>
        </td>
        <td>
        <div style='float:left'>
        <img src=" """'graph/graph'+str(listn[listdup[2][0]:listdup[2][0]+len(listdup[2])])+'.png'""" " width="750" height="600">
        </div>
        </td>
        </tr>""" 
    f = open(my_path + '/report/'+str(n1)+str(n2)+str(n3)+str(n4)+str(n5)+str(n6)+'/' + str(n1)+' '+str(n2)+' '+str(n3)+' '+str(n4)+' '+str(n5)+' '+str(n6)+'.html','w')
    f.write(tablefull+tablefig2+tablefig3+tablefig4+tableend)
    f.close()
    workbook.close()
    print(listdup)
    raise SystemExit("finish")
