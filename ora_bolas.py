# Bibliotecas
import time
from math import sqrt, tan, atan, pow
from sympy import symbols
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as Buttom
import matplotlib.animation as animation
from tkinter import *
from tkinter.ttk import Combobox

from sympy.core.core import Registry

x = symbols('x')

# Indicar o frame de observação [TERMPORARIO]

frame = int(input("Digite um frame: "))
inicio = time.time()

# Abrir o arquivo (tempo) e encontrar e printar o tempo correto

with open("tempo.txt", "r") as arquivo:
  templist = []
  tempo = []
  arq = arquivo.readlines()
  arquivo.close()
  for line in range(len(arq)):
    n = float(arq[line])
    templist.append(n)
    if line < 461:
      tempo.append(n)
  arquivo.close()

# Abrir o arquivo (x) e encontrar a linha (coordenada) na qual está localizada o tempo

with open("x.txt", "r") as arquivo:
  coordxlist = []
  XBola = []
  arq = arquivo.readlines()
  arquivo.close()
  for line in range(len(arq)):
    n = float(arq[line])
    coordxlist.append(n) 
    XBola.append(n)
  arquivo.close()

# Abrir o arquivo (y) e encontrar a linha (coordenada) na qual está localizada o tempo

with open("y.txt", "r") as arquivo:
  coordylist = []
  YBola = []
  arq = arquivo.readlines()
  arquivo.close()
  for line in range(len(arq)):
    n = float(arq[line])
    coordylist.append(n)   
    YBola.append(n) 
  arquivo.close()

# Inputs coordenadas X e Y do robô e declaração de variáveis

#Rx = float(input("Digite a posição inicial do robô no eixo X: ")) # Coordenada X do robô
#Ry = float(input("Digite a posição inicial do robô no eixo Y: ")) # Coordenada Y do robô

# [Tkinter]

def main(Rx, Ry):
    # [Arrays]

  D = [] # Distância entre o robô e a bola
  final_inicial = [] # Diferença entre o final e inicial dos pontos da bola entre pontos
  DF = [] # Distância entre o robô e a trajetória futura

  Fx = [] # Trajetória da bola "futura" em X
  Fy = [] # Trajetória da bola "futura" em Y

  Vxbola = [1.5] # Velocidade da bola em X 
  Vybola = [1] # Velocidade da bola em Y

  Axbola = [1.5] # Aceleração da bola em X
  Aybola = [1] # Aceleração da bola em Y

  Dx = [] # Distância S do robô em X | (S = So + vt)
  Dy = [] # Distância S do robô em Y | (S = So + vt)

  Vi = [] # Velocidade instantânea da bola

  vir = []
  Vx = [] # Velocidade do robô em X | (Vx = ΔxS / Δt)
  Vy = [] # Velocidade do robô em Y | (Vy = ΔyS / Δt)

  aBola = [] # Aceleração do robô 

  cos = [] # Cosseno entre a bola e o robô
  sen = [] # Seno entre a bola e o robô

  t = [] # Tempo do alcance do robô na bola
  Dt = [] # Diferenca dos tempos
  Dfuture = []

  framelist = []

  dist_data = [] # teste
  Robo_data = []
  Bola_data = []

  Posx = []
  Posy = []

  distanciacertaconfia = []

  distanciaX = []
  distanciaY = []

  acc = []
  # [Variáveis] 

  # Bola
  vob = 0.09 # Velocidade inicial da bola
  vox = 0.05 # Velocidade inicial da bola em X
  voy = 0.04 # Velocidade inicial da bola em Y
  aceleracao_bola = 0.06 # Aceleração da bola
  futuro = 30
  # Robô
  v = 0 # Velocidade inicial do robô
  a = 0 #  Aceleração inicial do robô

  y = 0.0303*x**2 + 0.0878*x + 1.0275
  Cofa = tan(0.0303)

  for i in range(0, (len(arq)-1)):
    if(i < len(arq)-futuro):
      Fx.append(coordxlist[i+futuro])
      Fy.append(coordylist[i+futuro])
      #Calcular a distância entre o robô e a trajetória Futura
      DF.append(sqrt(((Fx[i]-coordxlist[i])*(Fx[i]-coordxlist[i])) + ((Fy[i]-coordylist[i])*(Fy[i]-coordylist[i]))))
    else:
      Fx.append(coordxlist[460])
      Fy.append(coordylist[460])
      #Calcular a distância entre o robô e a trajetória Futura
      DF.append(sqrt(((Fx[i]-coordxlist[i])*(Fx[i]-coordxlist[i])) + ((Fy[i]-coordylist[i])*(Fy[i]-coordylist[i]))))
    # Velocidades X e Y da bola
    Vxbola.append(vox + aceleracao_bola*templist[i])
    Vybola.append(voy + aceleracao_bola*templist[i])

    framelist.append(i)

  menor = 10
  for i in range(0, (len(arq)-2)):

    # Calcular a distância 
    D.append(sqrt(((Rx-coordxlist[i])*(Rx-coordxlist[i])) + ((Ry-coordylist[i])*(Ry-coordylist[i]))))
    if i <= 430:
      Dfuture.append(sqrt(((Rx-coordxlist[i+futuro])*(Rx-coordxlist[i+futuro])) + ((Ry-coordylist[i+futuro])*(Ry-coordylist[i+futuro]))))
      if Dfuture[i] < menor:
        menor = Dfuture[i]
    else:
      Dfuture.append(sqrt(((Rx-coordxlist[460])*(Rx-coordxlist[460])) + ((Ry-coordylist[460])*(Ry-coordylist[460]))))
      if Dfuture[i] < menor:
        menor = Dfuture[i]
    # Diferença entre Xf-Xi, Yf-Yi
    final_inicial.append(sqrt(((coordxlist[i+1]-coordxlist[i])*((coordxlist[i+1]-coordxlist[i])) + (coordylist[i+1]-coordylist[i])*(coordylist[i+1]-coordylist[i]))))
    
    aBola.append(2*(D[i] - v * templist[i])/templist[i]*templist[i]) 
    # Calcular a aceleração X e Y da bola
    bolaacc = final_inicial[i]/0.02
    Vi.append(aBola[i]*templist[i])

    if(i <= 430):
      Dt.append(templist[i+futuro]-templist[i])
    else:
      Dt.append(templist[460]-templist[i])
    
    if a >= 2:
      t.append(sqrt(2*(D[i])/a))
      acc.append(a)
    else:
      acc.append(a)
      a += 0.2
      t.append(sqrt(2*(D[i])/a))

  intercept_time_robot = 10
  intercept_timelist = 10
  for i in range(0, (len(arq)-2)):

    if t[i] < templist[i] and templist[i] < intercept_timelist:
      intercept_time_robot = t[i]
      intercept_timelist = templist[i]
      index = i
      Distance_Intercept = sqrt(((Rx-coordxlist[i])*(Rx-coordxlist[i])) + ((Ry-coordylist[i])*(Ry-coordylist[i])))

  Posx.append(Rx)
  Posy.append(Ry)
  distanciaX.append(Rx)
  distanciaY.append(Ry)
  a = 1
  for i in range(0, (len(arq)-2)):

    a += 0.2

    if a >= 2:
      a = 2
    # Calcular o Cos e Sen entre o robô e a bola
    vir0 = a*templist[i]
    if vir0 >= 2:
      vir.append(2)
    else:
      vir.append(vir0)
    cos.append((coordxlist[i]-distanciaX[i])/Distance_Intercept)
    sen.append((coordylist[i]-distanciaY[i])/Distance_Intercept)

    distanciaX.append(distanciaX[i] + a*cos[i]*pow(templist[i], 2)/2)
    distanciaY.append(distanciaY[i] + a*sen[i]*pow(templist[i], 2)/2)

    distanciacertaconfia.append(sqrt(((distanciaX[i]-coordxlist[i])*(distanciaX[i]-coordxlist[i])) + ((distanciaY[i]-coordylist[i])*(distanciaY[i]-coordylist[i]))))

  windowII = Tk()
  windowII.title("Inicio")

  def gfBola():
    def atualizar_pontos(i):
      if i%5==0:
        ponto_animado.set_marker("o")
        ponto_animado.set_markersize(12)
        dist.set_marker("o")
        dist_future.set_marker("o")
        robo.set_markersize(12)
      robo.set_data(distx[i], disty[i])
      dist.set_data([x[i], Rx], [y[i], Ry])
      ponto_animado.set_data(x[i], y[i])
      text_frame.set_text("frame: %d"% frame[i])  
      text_pt.set_text("x: %.3f, y = %.3f"%(x[i], y[i]))
      text_temp.set_text("t: %.3fs"% temp[i])
      dist_txt.set_text("dist: %.3fm"% distancia[i])
      dist_t_intercept.set_text("t intercept future: %.3f"% tempofuturo[i])
      tempo_desloc_future.set_text("t robo<>future: %.3f"% tempodeslocfuture[i])
      menor_distancia.set_text("Menor distância: %.3f"% menordist)
      intercept_timeR.set_text("Menor tempo de interceptação: %.3f | %.3f"% (time_intercept, time_intercep_list))
      Vbola.set_text("Velocidade da bola: %.3f"% velocidadebola[i])
      if temp[i] >= intercept_timelist:
        animado.event_source.stop()
        intercept_txt.set_text("BOLA INTERCEPTADA!!!")
      if i < 430:
        dist_future.set_data([x[i+futuro], Rx], [y[i+futuro], Ry])
        dist_future_txt.set_text("dist future: %.3fm"% distanciafuturo[i])
      if i >= 430:
        dist_future.set_data([x[460], Rx], [y[460], Ry])
        dist_future_txt.set_text("dist future: %.3fm"% distanciafuturo[460-futuro])
      return ponto_animado,text_pt, text_temp, text_frame, dist, dist_txt, dist_future, dist_future_txt, dist_t_intercept, tempo_desloc_future, intercept_timeR, robo,

    # Variaveis
    distx = distanciaX
    disty = distanciaY
    velocidadebola = Vi
    time_intercept = intercept_time_robot
    time_intercep_list = intercept_timelist
    menordist = menor
    distancia = D
    distanciafuturo = Dfuture
    tempofuturo = Dt
    x = XBola
    y = YBola
    temp = templist
    frame = framelist
    tempodeslocfuture = t
    fig = plt.figure(tight_layout=True)
    plt.plot(Rx, Ry)
    robo, = plt.plot(distanciaX[0], distanciaY[0],  "o", color="orange")
    plt.plot(x,y)
    ponto_animado, = plt.plot(x[0], y[0], "o", color="blue")
    plt.plot(x, y, Rx, Ry)
    dist, = plt.plot([x[0], Rx], [y[0], Ry], marker="o")
    plt.plot(x, y, Rx, Ry)
    dist_future, = plt.plot([x[futuro], Rx], [y[futuro], Ry], marker="o", color="green")
    plt.plot(x, y, Rx, Ry)
    dist_intercept = plt.plot([x[index], Rx], [y[index], Ry],  marker="o", color="yellow")
    plt.grid(ls="-")
    text_frame = plt.text(1.1, 4.6, '', fontsize=8)
    text_temp = plt.text(1.1, 4.4, '', fontsize=8)
    text_pt = plt.text(1.1, 4.2, '', fontsize=8)
    dist_txt = plt.text(1.1, 4.0, '', fontsize=8, color="red")
    dist_future_txt = plt.text(1.1, 3.8, '', fontsize=8, color="green")
    dist_t_intercept = plt.text(1.1, 3.6, '', fontsize=8)
    tempo_desloc_future = plt.text(1.1, 3.4, '', fontsize=8)
    menor_distancia = plt.text(1.1, 3.2, '', fontsize=8)
    intercept_timeR = plt.text(1.1, 3.0, '', fontsize=8)
    intercept_txt = plt.text(1.1, 2.8, '', fontsize=8)
    Vbola = plt.text(1.1, 2.6, '', fontsize=8)
    animado = animation.FuncAnimation(fig, atualizar_pontos, np.arange(0, 460), interval=5, blit=True)
    plt.show()

  def trajetoriax():
    plt.plot(tempo[0:index], XBola[0:index])
    plt.show()

  def trajetoriay():
    plt.plot(tempo[0:index], YBola[0:index])
    plt.show()

  def velocidaderobo():
    plt.plot(tempo[0:index], vir[0:index])
    plt.show()

  def velocidadebola():
    plt.plot(tempo[0:index], Vi[0:index])
    plt.show()

  def dist_bola_robo():
    plt.plot(tempo[0:index], distanciacertaconfia[0:index])
    plt.show()

  def aceleracaobola():
    plt.plot(tempo[0:index], aBola[0:index])
    plt.show()

  def aceleracaorobo():
    plt.plot(tempo[0:index], acc[0:index])
    plt.show()

  tit = Label(windowII, text = "Escolha o gráfico", font = ('Arial Bold', 15))
  tit.place(relx = 0.5, rely = 0.05, anchor = CENTER)

  pltbola = Button(windowII, text = "Bola", command = gfBola).place(relx = 0.10, rely = 0.20)

  pltx = Button(windowII, text = "Trajetória no Y", command = trajetoriax).place(relx = 0.10, rely = 0.25)

  plty = Button(windowII, text = "Trajetória no X", command = trajetoriay).place(relx = 0.30, rely = 0.25)

  pltvx = Button(windowII, text = "Velocidade do robô", command = velocidaderobo).place(relx = 0.10, rely = 0.30)

  pltvy = Button(windowII, text = "Velocidade da bola", command = velocidadebola).place(relx = 0.35, rely = 0.30)

  plta = Button(windowII, text = "Aceleração do robô", command = aceleracaorobo).place(relx = 0.10, rely = 0.35)

  plta2 = Button(windowII, text = "Aceleração da bola", command = aceleracaobola).place(relx = 0.35, rely = 0.35)

  pltd = Button(windowII, text = "Distância", command = dist_bola_robo).place(relx = 0.10, rely = 0.40)

  windowII.geometry("500x500")
  windowII.mainloop()

  j = 0
  k = 0
  for i in range(0, frame):
    if i >= 453:
      j += 1
      if i >= 461:
        k += 1
      if i == 463:
        break
    if D[i-k] == 0:
      print("Bola Interceptada!")
      break
    print("""
    (!) Frame [{0:003d}]

    (:) - Tempo: {tempo:.3f}s

    [#] - Bola
    (+) X: {X:.3f} | Y: {Y:.3f}
    (/) V: {V:.3f} | Vx: {Vx:.3f} | Vy: {Vy:.3f}
    (/) A: {A:.3f} """.format(
      (i+1), 
      tempo = templist[i],
      X = coordxlist[i],
      Y = coordylist[i],
      V = Vi[i],
      Vx = Vxbola[i],
      Vy = Vybola[i],
      A = aBola[i]))
    print("""
    [#] - Robô
    (+) X: {0:.3f} | Y: {Ry:.3f}""".format(
      Rx,
      Ry = Ry))
    print("""
    [#] Distancias
    (/) Robô <> bola: {0:.3f} | Robô <> bolaFutura {futuro:.3f}
    (/) Sen: {Sen:.3f} | Cos: {Cos:.3f}

    -----------------------------------------------------""".format(
      D[i],
      futuro = Dfuture[i],
      Sen = sen[i-k],
      Cos = cos[i-k]))



XRobo = []
YRobo = []
XRoboV = []
YRoboV = []
XRoboA = []
YRoboA = []
window = Tk()
window.title("Inicio")

titulos = Label(window, text = "Dados", font = ('Arial Bold', 15))
titulos.place(relx = 0.5, rely = 0.05, anchor = CENTER)

XRobbo = Label(window, text = "Posição X", font = ('Arial Bold', 15))
XRobbo.place(relx = 0.2, rely= 0.1, anchor = CENTER)
Rx = DoubleVar()

XRoboII = Entry(window, width = 16, font=('Arial Bold', 12), textvariable = Rx)
XRoboII.place(relx = 0.5, rely = 0.1, anchor = CENTER)


YRobbo = Label(window, text = "Posição Y", font = ('Arial Bold', 15))
YRobbo.place(relx = 0.2, rely= 0.17, anchor = CENTER)
Ry = DoubleVar()

YRoboII = Entry(window, width = 16, font=('Arial Bold', 12), textvariable = Ry)
YRoboII.place(relx = 0.5, rely = 0.17, anchor = CENTER)

nomeDaniel0 = Label(window, text = "Daniel Alves Cunha | RA: 22.121.008-1", font = ('Arial Bold', 15))
nomeDaniel0.place(relx = 0.5, rely = 0.25, anchor = CENTER)

nomeDaniel1 = Label(window, text = "Daniel Giovanni Lombardo | RA: 22.121.009-9", font = ('Arial Bold', 15))
nomeDaniel1.place(relx = 0.5, rely = 0.30, anchor = CENTER)

kenzo = Label(window, text = "Kenzo Sugai | RA: 22.121.005-7", font = ('Arial Bold', 15))
kenzo.place(relx = 0.5, rely = 0.35, anchor = CENTER)

def Verificar_Robo():
  pontos = {
    'Rx': Rx.get(),
    'Ry': Ry.get()
  }
  print("O Robo está no ponto X: ", pontos['Rx'], " e no ponto Y: ", pontos['Ry'])

  main(pontos['Rx'], pontos['Ry'])

pltveri = Button(window, text = "Verificar", command = Verificar_Robo).place(relx = 0.67, rely = 0.14)

window.geometry("500x500")
window.mainloop()