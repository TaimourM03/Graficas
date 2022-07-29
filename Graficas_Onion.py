import time
import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.cbook as cbook
import matplotlib.image as image
import pygal
from svglib.svglib import svg2rlg
from datetime import date, datetime
import pymongo
from completer import *


def elegir_banda():
    meses_n_w={"01":"Enero","02":"Febrero","03":"Marzo","04":"Abril","05":"Mayo","06":"Junio","07":"Julio","08":"Agosto","09":"Septiembre","10":"Octubre",
               "11":"Noviembre","12":"Diciembre"}
    cliente = pymongo.MongoClient("mongodb://garu:garu@10.100.10.90:27017/ransom")
    ransomdb= cliente["ransom"] #nombre BD
    bandas = ransomdb["bandas"] #nombre de la tabla
    todos = bandas.find()
    total_bandas = {}    
    total_bandas_2022 = {}    
    cont = 0
    for t in todos:
        total_bandas[str(cont)]=t["Nombre"]
        cont += 1
    print("0: Generar gráficas de una banda")
    time.sleep(0.3)
    print("1: Generar gráficas de varias bandas")
    time.sleep(0.3)
    print("2: Generar gráficas de todas las bandas")
    time.sleep(0.3)
    cant_graf = input("Escoge una opción: ")
    if cant_graf == "0":
        try:
            banda = complete("bandas")
            bandas = ransomdb["bandas"] #nombre de la tabla
            x = bandas.find_one({"Nombre":banda})
            paises = x["Paises"]
            continentes = x["Continentes"]
            fechas = x["Fechas"]
            print(paises,continentes,fechas)
            input()
        except:
            print("ERROR! Banda inexistente.")
            time.sleep(1)
            print("Vuelve a intentarlo.")
            time.sleep(1)
            elegir_banda()
        else:
            Esquematizador(banda,fechas,paises,continentes)
    
    elif cant_graf == "1":
        nombre_bandas=[]
        print("\nHay un total de",len(total_bandas),"bandas.\n")
        time.sleep(1.5)
        for x in total_bandas:
            time.sleep(0.15)
            frase=str(x)+": "+str(total_bandas[x])
            print(frase)
        cant_graf2 = input("Introduce los numeros de las bandas (separados por comas, ej: 1,2,3): ").split(",")
        for n in cant_graf2:
            for e in total_bandas:
                if e == n:
                    nombre_bandas.append(total_bandas[n])

        datos = []
        for banda in nombre_bandas:
            datos.append(bandas.find_one({"Nombre":banda}))


        directorio="//home//kali//Desktop//Graficas de"
        for banda in nombre_bandas:
            if banda != nombre_bandas[-2] and banda != nombre_bandas[-1]:
                banda_aux = " "+banda+","
            elif banda == nombre_bandas[-2]:
                banda_aux = " "+banda+" y"
            else:
                banda_aux = " "+banda
            directorio += banda_aux
        
        try: #en caso de que la carpeta ya exista, dara error
            os.mkdir(directorio)
            print("Carpeta generada correctamente en el directorio:",directorio)
        except:
            for intento in range(2,100):
                directorio2 = directorio+str(intento)    
                try:
                    os.mkdir(directorio2)
                    directorio = directorio2
                    print("Carpeta generada correctamente en el directorio:",directorio2)
                    time.sleep(1)
                    break
                except:
                    continue
        graf8(datos,directorio)
        #grafica comparativa de los paises atacados de varias bandas
        #grafica de los meses atacados de varias bandas
    
    elif cant_graf == "2":
        print("\n0: Graficas de todas las bandas con datos de un año en concreto.")
        time.sleep(0.3)
        print("1: Graficas de todas las bandas con todos los datos.")
        time.sleep(0.3)
        print("2: Graficas de todas las bandas con ataques en un mes de un año en concreto.")
        time.sleep(0.3)
        elec2 = input("Escoge una opción: ")
        if elec2 == "0":
            nombre_bandas_2=[]
            años_disp_0=[]
            años_disp_d0={}
            for banda in list(total_bandas.values()):
                nombre_bandas_2.append(banda)
                fechas = bandas.find_one({"Nombre":banda})["Fechas"]
                for fecha in fechas:
                    año = fecha[-4:]
                    if año not in años_disp_0 and año!="cido":  #cido=fecha desconocida
                        años_disp_0.append(año)
            print("\n")
            años_disp_0.sort()
            for año in range(len(años_disp_0)):
                sent = str(año)+": "+años_disp_0[año]
                print(sent)
                años_disp_d0[str(año)]=años_disp_0[año]
                time.sleep(0.3)
            elec_año = input("Escoge una opción: ")
            for x in list(años_disp_d0.keys()):
                if elec_año == x:
                    pos = list(años_disp_d0.keys()).index(x)
                    año_elegido = años_disp_0[pos]
            for banda in list(total_bandas.values()):
                fechas_t = bandas.find_one({"Nombre":banda})["Fechas"]
                fechas = []
                for fecha in fechas_t:
                    if fecha[-4:] == año_elegido:
                        fechas.append(fecha)
                if len(fechas)!=0:
                    total_bandas_2022[banda]=len(fechas)
            frase = "Ataques por bandas en el "+año_elegido
            directorio="//home//kali//Desktop//"+"Graficas Ataques por bandas en "+año_elegido
            try: #en caso de que la carpeta ya exista, dara error
                os.mkdir(directorio)
            except:
                for intento in range(2,100):
                    directorio2 = directorio+str(intento)    
                    try:
                        os.mkdir(directorio2)
                        directorio = directorio2
                        print("Carpeta generada correctamente en el directorio:",directorio2)
                        time.sleep(1)
                        break
                    except:
                        continue
            if len(total_bandas_2022)<10:
                param_aux="2"
            else:
                param_aux=False
            graf8(total_bandas_2022,directorio,frase,param_aux)
            graf9(total_bandas_2022,directorio,frase)
            

            todas_las_fechas={}            
            años_disp_da={}
            for banda in nombre_bandas_2:
                fechas = bandas.find_one({"Nombre":banda})["Fechas"]
                for fecha in fechas:
                    mes = fecha[-7:-5]
                    año = fecha[-2:]
                    if año == año_elegido[-2:]:
                        if (año not in años_disp_da or int(mes)<int(años_disp_da[año]))and año != "do":
                            años_disp_da[año]=str(mes)
                        f = str(mes)+"/"+str(año)
                        if f not in todas_las_fechas and f != "on/do":  #fechas desconocidas = on/do
                            todas_las_fechas[f]="1"
                        elif f in todas_las_fechas and f != "on/do":
                            cant = str(int(todas_las_fechas[f])+1)
                            todas_las_fechas[f]=cant
            sysdate = str(date.today())
            for year in años_disp_da:
                if year ==  sysdate[2:4]:
                    mes_final = int(sysdate[5:7])+1
                else:
                    mes_final = 13
                for x in range(int(años_disp_da[year]),mes_final):
                    if len(str(x)) == 1:
                        f_año = "0"+str(x)+"/"+str(year)
                    else:
                        f_año = str(x)+"/"+str(year)
                    if f_año not in todas_las_fechas:
                        todas_las_fechas[f_año]="0"
            #ORDENAR EL DICCIONARIO DE FECHAS 
            orden_f = []
            for fecha in todas_las_fechas:
                año = int(fecha[-2:])
                mes = int(fecha[0:2])
                if len(orden_f)==0:
                    orden_f.append(fecha)
                else:
                    var=0
                    for x in range(len(orden_f)):
                        año2 = int(orden_f[x][-2:])
                        mes2 = int(orden_f[x][0:2])
                        if año2<año:
                            var +=1
                        elif año2>año:
                            orden_f.insert(var,fecha)
                            break
                        elif año2==año and mes<mes2:
                            orden_f.insert(var,fecha)
                            break
                        else: #mes>mes2 and año2==año
                            var+=1
                        if orden_f[x]==orden_f[-1] and fecha not in orden_f:
                            orden_f.insert(len(orden_f),fecha)
            dicci_orden = {}
            for fecha in orden_f:
                for fech in todas_las_fechas:
                    if fecha == fech:
                        valor = todas_las_fechas[fech]
                        dicci_orden[fecha]=valor
                        break
            cambiar_nombre = "bandas"
            x = list(dicci_orden.keys())
            y = list(dicci_orden.values())
            y_o=[]
            for num in y:
                y_o.append(int(num))
            frase_d = "Grafica de ataques por meses de todas las bandas en el "+año_elegido+"."
            nombre_banda = ""
            graf1(cambiar_nombre,x,y_o,frase_d,directorio,nombre_banda)



        elif elec2 == "1":
            nombre_bandas_2=list(total_bandas.values())
            ataques_bandas = {}
            frase = "Ataques por bandas"
            directorio="//home//kali//Desktop//"+"Graficas Ataques por bandas"
            for banda in nombre_bandas_2:
                empresas = (bandas.find_one({"Nombre":banda})["Empresas"])
                ataques_bandas[banda]=len(empresas)
            try: #en caso de que la carpeta ya exista, dara error
                os.mkdir(directorio)
            except:
                for intento in range(2,100):
                    directorio2 = directorio+str(intento)    
                    try:
                        os.mkdir(directorio2)
                        directorio = directorio2
                        print("Carpeta generada correctamente en el directorio:",directorio2)
                        time.sleep(1)
                        break
                    except:
                        continue
            param_aux = "general"
            graf8(ataques_bandas,directorio,frase,param_aux)
            graf9(ataques_bandas,directorio,frase)
            todas_las_fechas={}            
            años_disp_da={}
            for banda in nombre_bandas_2:
                fechas = bandas.find_one({"Nombre":banda})["Fechas"]
                for fecha in fechas:
                    mes = fecha[-7:-5]
                    año = fecha[-2:]
                    if (año not in años_disp_da or int(mes)<int(años_disp_da[año]))and año != "do":
                        años_disp_da[año]=str(mes)
                    f = str(mes)+"/"+str(año)
                    if f not in todas_las_fechas and f != "on/do":  #fechas desconocidas = on/do
                        todas_las_fechas[f]="1"
                    elif f in todas_las_fechas and f != "on/do":
                        cant = str(int(todas_las_fechas[f])+1)
                        todas_las_fechas[f]=cant
            sysdate = str(date.today())
            for year in años_disp_da:
                if year ==  sysdate[2:4]:
                    mes_final = int(sysdate[5:7])+1
                else:
                    mes_final = 13
                for x in range(int(años_disp_da[year]),mes_final):
                    if len(str(x)) == 1:
                        f_año = "0"+str(x)+"/"+str(year)
                    else:
                        f_año = str(x)+"/"+str(year)
                    if f_año not in todas_las_fechas:
                        todas_las_fechas[f_año]="0"
            #ORDENAR EL DICCIONARIO DE FECHAS 
            orden_f = []
            for fecha in todas_las_fechas:
                año = int(fecha[-2:])
                mes = int(fecha[0:2])
                if len(orden_f)==0:
                    orden_f.append(fecha)
                else:
                    var=0
                    for x in range(len(orden_f)):
                        año2 = int(orden_f[x][-2:])
                        mes2 = int(orden_f[x][0:2])
                        if año2<año:
                            var +=1
                        elif año2>año:
                            orden_f.insert(var,fecha)
                            break
                        elif año2==año and mes<mes2:
                            orden_f.insert(var,fecha)
                            break
                        else: #mes>mes2 and año2==año
                            var+=1
                        if orden_f[x]==orden_f[-1] and fecha not in orden_f:
                            orden_f.insert(len(orden_f),fecha)
            dicci_orden = {}
            for fecha in orden_f:
                for fech in todas_las_fechas:
                    if fecha == fech:
                        valor = todas_las_fechas[fech]
                        dicci_orden[fecha]=valor
                        break
            cambiar_nombre = "bandas"
            x = list(dicci_orden.keys())
            y = list(dicci_orden.values())
            y_o=[]
            for num in y:
                y_o.append(int(num))
            frase_d = "Grafica de ataques por meses de todas las bandas."
            nombre_banda = ""
            graf1(cambiar_nombre,x,y_o,frase_d,directorio,nombre_banda)





        elif elec2 == "2":
            bandas_disp_d3 = {}           
            años_disp_d3={}
            meses_disp_d3 = {}            
            años_disp_3=[]
            for banda in list(total_bandas.values()):
                fechas = bandas.find_one({"Nombre":banda})["Fechas"]
                for fecha in fechas:
                    año = fecha[-4:]
                    if año not in años_disp_3 and año!="cido":  #cido=fecha desconocida
                        años_disp_3.append(año)
            print("\n")
            años_disp_3.sort()
            for año in range(len(años_disp_3)):
                sent = str(año)+": "+años_disp_3[año]
                print(sent)
                años_disp_d3[str(año)]=años_disp_3[año]
                time.sleep(0.3)
            elec_año = input("Escoge una opción: ")
            for x in list(años_disp_d3.keys()):
                if elec_año == x:
                    pos = list(años_disp_d3.keys()).index(x)
                    año_elegido = años_disp_3[pos]
            meses_disp_3=[]
            for banda in list(total_bandas.values()):
                fechas = bandas.find_one({"Nombre":banda})["Fechas"]
                for fecha in fechas:
                    año = fecha[-4:]
                    if año == año_elegido:
                        mes = fecha[-7:-5]
                        if mes not in meses_disp_3 and mes != "on":  #on = fecha desconocida
                            meses_disp_3.append(mes)
            meses_disp_3.sort()
            print("\n")
            for mes in range(len(meses_disp_3)):
                sent = str(mes)+": "+meses_disp_3[mes]
                meses_disp_d3[mes]=meses_disp_3[mes]
                print(sent)
                time.sleep(0.3)
            elec_mes = str(input("Escoge una opción: "))
            for x in list(meses_disp_d3.keys()):
                if elec_mes == str(x):
                    pos = list(meses_disp_d3.keys()).index(x)
                    mes_elegido = meses_disp_3[pos]

            for banda in list(total_bandas.values()):
                fechas_correctas_banda=[]
                fechas = bandas.find_one({"Nombre":banda})["Fechas"]
                for fecha in fechas:
                    año = fecha[-4:]
                    mes = fecha[-7:-5]
                    if año == año_elegido and mes == mes_elegido:
                        fechas_correctas_banda.append(fecha)
                if len(fechas_correctas_banda)!=0:
                    bandas_disp_d3[banda]=len(fechas_correctas_banda)
            meses_n_w
            for mes in meses_n_w:
                if mes_elegido == mes:
                    mes_w = meses_n_w[mes]
                    break
            frase = "Ataques por bandas en "+mes_w+" del "+año_elegido
            directorio="//home//kali//Desktop//"+"Graficas Ataques por bandas "+mes_w+"-"+año_elegido
            try: #en caso de que la carpeta ya exista, dara error
                os.mkdir(directorio)
            except:
                for intento in range(2,100):
                    directorio2 = directorio+" "+str(intento)    
                    try:
                        os.mkdir(directorio2)
                        directorio = directorio2
                        print("Carpeta generada correctamente en el directorio:",directorio2)
                        time.sleep(1)
                        break
                    except:
                        continue
            param_aux = True  #esta var servira para cambiar el valor de "Otros" en las grafs a >=4
            graf8(bandas_disp_d3,directorio,frase,param_aux)
            graf9(bandas_disp_d3,directorio,frase)           

                       

            
            

def Esquematizador(nombre_banda,fechas,paises,continentes):
    meses1 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    meses2 = ["/01","/02","/03","/04","/05","/06","/07","/08","/09","/10","/11","/12"]
    meses3 = ["-01","-02","-03","-04","-05","-06","-07","-08","-09","-10","-11","-12"]
    numeros_meses = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    dias_=[]
    meses_=[]
    years_=[]
    for x in range(len(meses3)): #FORMATO XX-MES-XXXX
        dicci = {"Jan":0,"Feb":0,"Mar":0,"Apr":0,"May":0,"Jun":0,"Jul":0,"Aug":0,"Sep":0,"Oct":0,"Nov":0,"Dec":0}
        meses = []
        x = []
        y = []
        for fecha in fechas:
            dias_.append(fecha[0:2])
            meses_.append(fecha[3:5])
            years_.append(fecha[6:11])
            if "null" not in fecha or "NULL" not in fecha:
                f = fecha[3]+fecha[4]
                meses.append(f)
        for mes in meses:
            cant = str(meses.count(mes))
            for s in range(len(meses2)):
                if mes == numeros_meses[s]:
                    dicci[meses1[s]]=cant
        for key in dicci:
            x.append(key)
            y.append(int(dicci[key]))
        break

    frase = "Paises atacados por "+nombre_banda
    frase2 = "Ataques por meses de "+nombre_banda
    frase3 = "Continentes atacados por "+nombre_banda
    frase4 = "Ataques por estaciones del año de "+nombre_banda
    directorio="//home//kali//Desktop//"+"Graficas "+nombre_banda
    opciones = ["0: Salir. \U0001F4A4","1: Mapa mundial con paises atacados y cantidades marcados. \U0001F30D",
                "2: Grafica de ataques por paises. \U0001F4CD","3: Grafica de ataques a un pais en concreto. \U0001F4CD", 
                "4: Grafica de ataques por continentes. \U0001F4CD","5: Grafica de ataques a un continente en concreto. \U0001F4CD",
                "6: Grafica de ataques por meses. \U0001F4C6 ","7: Grafica de ataques en un mes en concreto. \U0001F4C6",
                "8: Grafica de ataques por años. \U0001F4C6","9: Grafica de ataques en un año en concreeto. \U0001F4C6",
                "10: Grafica de atauqes por estaciones del año. \U0001F326", 
                "11: Grafica de ataques en una estación del año en concreto. \U0001F326",
                "12: Generar todas las graficas generales. \U0001F30D \U0001F4CD \U0001F4C6 \U0001F326"]
    eleccion = ""
    try: #en caso de que la carpeta ya exista, dara error
        os.mkdir(directorio)
    except:
        for intento in range(2,100):
            directorio2 = directorio+str(intento)    
            try:
                os.mkdir(directorio2)
                directorio = directorio2
                print("Carpeta generada correctamente en el directorio:",directorio2)
                time.sleep(1)
                break
            except:
                continue
    while eleccion != "0":
        cambiar_nombre = ""
        print("")
        for opcion in opciones:
            print(opcion)
            time.sleep(0.1)
        print("")
        eleccion = input("Escoge una opcion: ")
        if eleccion == "0":
            print("Apagando...")
        elif eleccion == "1":
            colores, n, n, paises_leyenda, iniciales = leyenda_paises(paises)
            graf5(iniciales,frase,directorio,nombre_banda)
            print("Grafica generada correctamente!")
        elif eleccion == "2":
            print("")
            print("1: Grafica de barras. \U0001F4CA")
            time.sleep(0.3)
            print("2: Grafica circular.")
            time.sleep(0.3)
            print("3: Ambas.")
            time.sleep(0.3)
            print("")
            tipo = input("Escoge un tipo de grafica: ")
            if tipo == "1":
                graf3(cambiar_nombre,paises,frase,directorio,nombre_banda)
            elif tipo == "2":
                graf2(cambiar_nombre,paises,frase,directorio,nombre_banda)
            elif tipo == "3":
                graf2(cambiar_nombre,paises,frase,directorio,nombre_banda)
                graf3(cambiar_nombre,paises,frase,directorio,nombre_banda)
            else:
                time.sleep(1)
                print("ERROR! Valor introducido erróneo.")
                time.sleep(0.5)
                print("Vuelve a intentarlo.")
                time.sleep(0.5)
        elif eleccion == "3":
            pass
        elif eleccion == "4":
            graf4(cambiar_nombre,continentes,paises,frase3,directorio,nombre_banda)        
        elif eleccion == "5":
            pass
        elif eleccion == "6":
            graf1(cambiar_nombre,x,y,frase2,directorio,nombre_banda) 
        elif eleccion == "7":
            pass
        elif eleccion == "8":
            años_disp = []
            for fecha in fechas:
                year = fecha[6:11]
                if year not in años_disp and year != "Desconocido":
                    años_disp.append(year)
            if len(años_disp) <= 1:
                print("ERROR! Las fechas disponibles son infiltrables (todas pertenecen al mismo año).")
            else:
                 graf7(fechas,años_disp,meses2,meses1,numeros_meses,nombre_banda,directorio)
        elif eleccion == "9":
            años_disp = []
            for fecha in fechas:
                year = fecha[6:11]
                if year not in años_disp and year != "Desconocido":
                    años_disp.append(year)
            if len(años_disp) <= 1:
                print("ERROR! Las fechas disponibles son infiltrables (todas pertenecen al mismo año).")
            else:
                for año in range(len(años_disp)):
                    print(año,":",años_disp[año])
                e = int(input("Escoge un año: "))
                e = años_disp[e]
                if e in años_disp:
                    paises_año = []
                    fechas_año = []
                    continentes_año = []
                    x_año=[]
                    y_año=[]
                    for pais in range(len(paises)):
                        if fechas[pais][6:11] == e:
                            fechas_año.append(fechas[pais])
                            paises_año.append(paises[pais])
                            continentes_año.append(continentes[pais])
                            dias__año=[]
                            meses__año=[]
                            years__año=[]
                    for x in range(len(meses3)): #FORMATO XX-MES-XXXX
                        dicci_año = {"Jan":0,"Feb":0,"Mar":0,"Apr":0,"May":0,"Jun":0,"Jul":0,"Aug":0,"Sep":0,"Oct":0,"Nov":0,"Dec":0}
                        meses_año = []
                        x_año = []
                        y_año = []
                        for fecha in fechas_año:
                            dias__año.append(fecha[0:2])
                            meses__año.append(fecha[3:5])
                            years__año.append(fecha[6:11])
                            if "Desconocido" not in fecha or "" not in fecha:
                                f = fecha[3]+fecha[4]
                                meses_año.append(f)
                    for mes in meses_año:
                        cant = str(meses_año.count(mes))
                        for s in range(len(meses2)):
                            if mes == numeros_meses[s]:
                                dicci_año[meses1[s]]=cant
                    for key in dicci_año:
                        x_año.append(key)
                        y_año.append(int(dicci_año[key]))
                    frase_año = "Paises atacados por "+nombre_banda+" en "+str(e)
                    frase2_año = "Ataques por meses de "+nombre_banda+" en "+str(e)
                    frase3_año = "Continentes atacados por "+nombre_banda+" en "+str(e)
                    frase4_año = "Ataques por estaciones del año de "+nombre_banda+" en "+str(e)

                    cambiar_nombre = str(e)
                    colores, n, n, paises_leyenda, iniciales = leyenda_paises(paises_año)
                    graf5(cambiar_nombre,iniciales,frase_año,directorio,nombre_banda)
                    graf2(cambiar_nombre,paises_año,frase_año,directorio,nombre_banda)
                    graf3(cambiar_nombre,paises_año,frase_año,directorio,nombre_banda)
                    graf1(cambiar_nombre,x_año,y_año,frase2_año,directorio,nombre_banda)
                    graf6(cambiar_nombre,paises_año,frase4_año,fechas_año,directorio,nombre_banda)
                    graf4(cambiar_nombre,continentes_año,paises_año,frase3_año,directorio,nombre_banda)                 
                    cambiar_nombre = ""
                else: 
                    print("ERROR! el año introducido no se encuentra en ninguna fecha.")
        elif eleccion == "10":
            graf6(cambiar_nombre,paises,frase4,fechas,directorio,nombre_banda)        
        elif eleccion == "11":
            pass
        elif eleccion == "12":
            colores, n, n, paises_leyenda, iniciales = leyenda_paises(paises)
            graf5(cambiar_nombre,iniciales,frase,directorio,nombre_banda)
            graf2(cambiar_nombre,paises,frase,directorio,nombre_banda)
            graf3(cambiar_nombre,paises,frase,directorio,nombre_banda)
            graf1(cambiar_nombre,x,y,frase2,directorio,nombre_banda)
            graf6(cambiar_nombre,paises,frase4,fechas,directorio,nombre_banda)
            graf4(cambiar_nombre,continentes,paises,frase3,directorio,nombre_banda)        
        else:
            print("Ha introducido un valor erróneo.")
            time.sleep(2)
            print("Vuelve a intentarlo") 
            time.sleep(1)
            Esquematizador(nombre_banda,fechas,paises,continentes)

def graf1(cambiar_nombre,x,y,frase2,directorio,nombre_banda):
    #1ª GRAFICA MESES ATAQUE MONTAÑA
    plt.rcParams["figure.figsize"] = (25.5,8.61)
    fig, ax = plt.subplots() 
    plt.title(label=frase2,fontsize=20,color = "purple",style="italic",y=1.05)
    plt.xlabel("Meses")
    plt.ylabel("Cantidad de ataques")
    ax.plot(x,y, '-o', mfc='orange')
    plt.grid(color = '#19dce6', linestyle = 'dotted')
    plt.text(0, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    if cambiar_nombre == "bandas":
        plt.savefig(directorio+"//Grafico de linias de todas las bandas.png") 
    elif cambiar_nombre != "":
        plt.savefig(directorio+'//Grafico de linias'+nombre_banda+" en "+cambiar_nombre+".png")    
    else:
        plt.savefig(directorio+'//Grafico de linias'+nombre_banda+".png")    
    sys.stdout.flush()
   

def graf2(cambiar_nombre,paises,frase,directorio,nombre_banda):
    #2ª grafica: circulo paises
    plt.rcParams["figure.figsize"] = (25.5,8.61)
    x,y,colores,paises_leyenda,iniciales = leyenda_paises(paises)
    fig, ax = plt.subplots()    
    graf1 = np.array(y)
    distanciado = []
    for p in range(len(x)):
        distanciado.append(0.1)
    plt.title(label=frase,fontsize=20,color = "purple",style="italic",y=1.05)
    plt.pie(graf1,labels = x, explode=distanciado, shadow=True)
    plt.grid(color = '#19dce6', linestyle = 'dotted')
    plt.text(2, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(2, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(2, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(2, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(-1, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(-1, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(-1, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(-1, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.legend(paises_leyenda ,bbox_to_anchor = (1.10,1))
    if cambiar_nombre != "":
        plt.savefig(directorio+'//Grafica paises atacados '+nombre_banda+" en "+cambiar_nombre+".png")    
    else:
        plt.savefig(directorio+'//Grafica paises atacados '+nombre_banda+".png")
    sys.stdout.flush()


def graf3(cambiar_nombre,paises,frase,directorio,nombre_banda):
    x,y,colores,paises_leyenda,iniciales=leyenda_paises(paises)
    #3ª GRAFICA barras paises
    plt.rcParams["figure.figsize"] = (25.5,8.61) #cambiar tamaño a mas grande la grafica, por defecto los valores son (6,4.4,8)
    fig, ax = plt.subplots()    
    plt.title(label=frase,fontsize=20,color = "purple",style="italic",y=1.05)
    plt.xlabel("Paises")
    plt.ylabel("Cantidad de ataques")
    plt.grid(color = '#19dce6', linestyle = 'dotted')
    plt.text(0, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    for lp in range(len(paises_leyenda)):
        try:
            plt.bar(x[lp], y[lp], color = colores[lp], label=x[lp])
        except:
            pass
    plt.legend(paises_leyenda, bbox_to_anchor = (1.10,1))
    if cambiar_nombre != "":
        plt.savefig(directorio+'//Grafica de barras '+nombre_banda+" en "+cambiar_nombre+".png")     
    else:
        plt.savefig(directorio+'//Grafica de barras '+nombre_banda+".png")   
    sys.stdout.flush()


def graf4(cambiar_nombre,continentes,paises,frase3,directorio,nombre_banda):
    #4ª graf: barras continentes
    plt.rcParams["figure.figsize"] = (25.5,8.61) 
    fig, ax = plt.subplots()    
    lista_x,lista_y = leyenda_continentes(continentes)
    x,y,colores,paises_leyenda,iniciales = leyenda_paises(paises)
    plt.title(label=frase3,fontsize=20,color = "purple",style="italic",y=1.05)
    plt.xlabel("Continentes")
    plt.ylabel("Cantidad de ataques")
    plt.grid(color = '#19dce6', linestyle = 'dotted')
    plt.text(0, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    for lp in range(len(lista_x)):
        try:
            plt.bar(lista_x[lp], lista_y[lp], color = colores[lp], label=lista_x[lp])
        except:
            pass
    plt.legend(lista_x ,bbox_to_anchor = (1.10,1))
    if cambiar_nombre != "":
        plt.savefig(directorio+'//Grafica de Barras continentes '+nombre_banda+" en "+cambiar_nombre+".png")
    else:
        plt.savefig(directorio+'//Grafica de Barras continentes '+nombre_banda+".png")
    sys.stdout.flush() 
    

def graf5(cambiar_nombre,iniciales,frase,directorio,nombre_banda):
    #5ª graf: mapamundi paises
    dicci_worldmap={}
    for x in iniciales:
        keys = dicci_worldmap.keys()
        if x not in keys:
            cantidad = iniciales.count(x)
            dicci_worldmap[x]=int(cantidad)
    worldmap =  pygal.maps.world.World()
    worldmap.title = frase
    worldmap.add('Ataques', dicci_worldmap)
    if cambiar_nombre != "":
        worldmap.render_to_file(directorio+'//Grafica Mapamundi '+nombre_banda+" en "+cambiar_nombre+".svg")      
    else:
        worldmap.render_to_file(directorio+'//Grafica Mapamundi '+nombre_banda+".svg")    


def graf6(cambiar_nombre,paises,frase4,fechas,directorio,nombre_banda):
    #6ª graf: grafica epocas del año:
    plt.rcParams["figure.figsize"] = (25.5,8.61)
    fig, ax = plt.subplots()    
    lista_y = estacion_meteorologica(fechas)
    lista_x= ["Primavera","Verano","Otoño","Invierno"]
    x,y,colores,paises_leyenda,iniciales = leyenda_paises(paises)

    plt.title(label=frase4,fontsize=20,color = "purple",style="italic",y=1.05)
    plt.xlabel("Estaciones")
    plt.ylabel("Cantidad de ataques")
    plt.grid(color = '#19dce6', linestyle = 'dotted')
    plt.text(0, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    for lp in range(len(paises_leyenda)):
        try:
            plt.bar(lista_x[lp], lista_y[lp], color = colores[lp], label=lista_x[lp])
        except:
            pass
    plt.legend(lista_x ,bbox_to_anchor = (1.10,1))
    if cambiar_nombre != "":
        plt.savefig(directorio+'//Grafica barras continentes '+nombre_banda+" en "+cambiar_nombre+".png")    
    else:
        plt.savefig(directorio+'//Grafica barras continentes '+nombre_banda+".png")    
    sys.stdout.flush() 
        

#GRAFICA COMPARATIVA AÑOS
def graf7(fechas,años_disp,meses2,meses1,numeros_meses,nombre_banda,directorio):
    dicci_años_c={}    
    for año_disp in años_disp:
        dicci = {"Jan":0,"Feb":0,"Mar":0,"Apr":0,"May":0,"Jun":0,"Jul":0,"Aug":0,"Sep":0,"Oct":0,"Nov":0,"Dec":0}
        fechas_año_c = []
        meses_año_c = []
        for fecha in fechas:
            mes = fecha[3:5]            
            año = fecha[6:11]
            if año == año_disp:
                fechas_año_c.append(fecha)
                meses_año_c.append(mes)
        for mes in meses_año_c:
            cant = str(meses_año_c.count(mes))
            for s in range(len(meses2)):
                if mes == numeros_meses[s]:
                    dicci[meses1[s]]=cant
        dicci_años_c[año_disp]=dicci
    
    plt.rcParams["figure.figsize"] = (25.5,8.61)
    fig, ax = plt.subplots()
    
    plt.title(label="Comparativa de ataques por meses en cada año de "+nombre_banda,fontsize=20,color = "purple",style="italic",y=1.05)
    plt.xlabel("Meses")
    plt.ylabel("Cantidad de ataques")
    plt.grid(color = '#19dce6', linestyle = 'dotted')
    plt.text(0, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    colores = []
    while len(colores)!=len(años_disp):
        color = "#"+"%06x" % random.randint(0, 0xFFFFFF)
        if color not in colores:
            colores.append(color)
    cont = 0
    for key in dicci_años_c:
        valores = [] 
        for v in list(dicci_años_c[key].values()):
            valores.append(int(v))
        plt.plot(meses1,valores,color = colores[cont],label = key)    
        cont +=1
    plt.legend(años_disp ,bbox_to_anchor = (1.10,1))
    plt.savefig(directorio+'//Grafica linias por años '+nombre_banda+".png") 
    sys.stdout.flush() 

    fig, ax = plt.subplots()    
    
    frase = "Paises atacados por"
    for n in nombre_bandas:
        for banda in n:
            if banda != nombre_bandas[-2][0] and banda != nombre_bandas[-1][0]:
                banda_aux = " "+banda+","
            elif banda == nombre_bandas[-2][0]:
                banda_aux = " "+banda+" y"
            else:
                banda_aux = " "+banda
            frase += banda_aux
    plt.title(frase)
    plt.xlabel("Paises")
    plt.ylabel("Cantidad de ataques")
    plt.grid(color = '#19dce6', linestyle = 'dotted')
    
    plt.text(0, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    
    x = np.arange(len(cantidades[0]))
    width = 0.2
    veces = len(nombre_bandas)
    despl=[]
    if (veces%2)==0: #es par 6
        mitad = int(veces/2)
        negativo = -0.2
        positivo = 0.2
        for me in range(0,mitad):
            despl.append(negativo)
            negativo += negativo
        for mu in range(mitad,veces):
            despl.append(positivo)
            positivo += positivo
    else: #es impar 
        mitad = int((veces/2)+0.5)
        negativo = -0.2
        positivo = 0.2
        for mi in range(1,mitad):#aqui se añaden los que tienen distanciado negativo
            despl.append(negativo)
            negativo += negativo
        despl.append(0.0) #el distanciado en el del medio es nulo
        for ma in range((mitad+1),(veces+1)):
            despl.append(positivo)
            positivo += positivo
    despl = sorted(despl)
    colores = ["green","blue","black","pink","red","purple","grey","yellow","cyan","orange","brown","navy","lime","darkolivegreen","lightblue","thistle",
               "rosybrown","indigo"] 
    for z in range(len(nombre_bandas)):
        plt.bar(x+despl[z],cantidades[z],width,color=colores[z],label=nombre_bandas[z][0])
    leyenda = []
    for elmnt in nombre_bandas:
        leyenda.append(elmnt[0])

    plt.xticks(x,iniciales)
    plt.legend(leyenda, bbox_to_anchor = (1.10,1))
    plt.show() 
    plt.savefig(directorio+'//Grafica de barras de los '+frase+".png")   
    sys.stdout.flush()

def graf8(bandas,directorio,frase,aux):
    #GRAFICA 8: CIRCULO DE TODAS LAS BANDAS
    bandas2=[]
    otros = {}    
    otras_bandas=""
    cant_o = 0
    total = 0
    x = list(bandas.keys())
    y= list(bandas.values())
    for e in range(len(x)):
        total += int(y[e])
        w = x[e]+" ["+str(y[e])+"]"
        bandas2.append(w)
    if aux == "2":
        var_aux = 0
    elif aux == True:
        var_aux = 5
    elif aux == "general":
        var_aux = 11
    else:
        var_aux = 10
    for q in range(len(x)):
        if y[q]<=var_aux:
            otros[x[q]]=y[q]
            cant_o += int(y[q])
            for banda in bandas2:
                if x[q] in banda:
                    bandas2.remove(banda)
    if cant_o > 0:
        otros_grupos = "Otros"+" ["+str(cant_o)+"]"
        for banda in otros:
            extra = banda+"  ["+str(otros[banda])+"]  "
            otras_bandas += extra
            if banda in x:
                x.remove(banda)
            if otros[banda] in y:
                y.remove(otros[banda])
        bandas2.append(otros_grupos)
        x.append("Otros")
        y.append(cant_o)
    
    graf1 = np.array(y)
    plt.rcParams["figure.figsize"] = (25,9) 
    fig, ax = plt.subplots() 
    distanciado = []
    for p in range(len(y)):
        distanciado.append(0.1)
    plt.title(label=frase,fontsize=20,color = "purple",style="italic",x=1.32,y=1.05)
    plt.grid(color = '#19dce6', linestyle = 'dotted')
    plt.text(2, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(2, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(2, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(2, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(-1, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(-1, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(-1, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(-1, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1.32,1.01,"Total: "+str(total),transform=ax.transAxes,
            fontsize=15, color='blue', ha='center', va='center',style="italic")
    if var_aux != 0:
        plt.text(-0.1,-1.45,"Otros",weight='bold')
    t_x = len(str(otras_bandas))/-80 #este calculo es para calcular la posicion en el medio del eje x del texto "Otros" 
    plt.text(t_x,-1.55,str(otras_bandas))
    wedgeprops = {"linewidth":1, "edgecolor":"black"}    
    x_2 = []
    y_2 = []
    for e in range(len(x)):
        y_2.append(y[e])
    y_2.sort()
    for elmnt in range(len(y_2)):
        for elm in range(len(y)):
            if y_2[elmnt]==y[elm]:
                if x[elm] not in x_2:
                    x_2.append(x[elm])
                    break
    
    x_legend=[]
    for e in range(len(x_2)):
        total += int(y_2[e])
        w = x_2[e]+" ["+str(y_2[e])+"]"
        x_legend.append(w)


    graf1 = np.array(y_2)
    _,__,a = plt.pie(graf1,labels = x_2,autopct='%1.1f%%',pctdistance=10.9,explode=distanciado, rotatelabels = 270, wedgeprops=wedgeprops,labeldistance=1.02)
    pcts=[]
    bandas3=[]
    pos = -1
    for pct in a:
        pos += 1
        banda = x_legend[pos]    
        try:
            pct = str(pct).split("'")[-2]
        except:
            pct = str(pct).split("'")[-1]
        banda2 = banda+" ("+pct+")"            
        bandas3.append(banda2)
    plt.legend(bandas3 ,bbox_to_anchor = (1.5,1))
    plt.savefig(directorio+"//Grafica circular de todas las bandas.png")    
    sys.stdout.flush()


def graf9(bandas,directorio,frase):
    #grafica 9: graf de barras de todas las bandas
    x=[]
    y=[]
    for banda in bandas:
        x.append(banda)
        y.append(bandas[banda])
    null,null,colores,null,null = leyenda_paises(x)
    plt.rcParams["figure.figsize"] = (25.5,8.61)
    fig, ax = plt.subplots()    
    plt.title(label=frase,fontsize=20,color = "purple",style="italic",y=1.05)
    plt.ylabel("Cantidad de ataques")
    plt.grid(color = '#19dce6', linestyle = 'dotted')
    plt.text(0, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.25, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.5, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(0.75, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 1, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.7, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0.3, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    plt.text(1, 0, 'GARU', transform=ax.transAxes,
            fontsize=100, color='grey', alpha=0.05, ha='center', va='center', rotation='30')
    for lp in range(len(x)):
        plt.bar(x[lp], y[lp], color = colores[lp], label=x[lp])
        plt.xticks(rotation='90',fontsize=8)
    plt.savefig(directorio+"//Grafica de Barras por bandas.png")
    sys.stdout.flush() 



def leyenda_continentes(continentes):
    EU = continentes.count("Europe")
    AS = continentes.count("Asia")
    AF = continentes.count("Africa")
    AMN = continentes.count("North America")
    AMS = continentes.count("South America")
    OC = continentes.count("Oceania")
    lista_x= ["Africa","Asia","Europe","North America","Oceania","South America"]
    lista_y= [AF,AS,EU,AMN,OC,AMS]
    return lista_x, lista_y


def leyenda_paises(paises): 
    countries = [
{'timezones': ['Europe/Andorra'], 'code': 'AD', 'continent': 'Europe', 'name': 'Andorra', 'capital': 'Andorra la Vella'},
{'timezones': ['Asia/Kabul'], 'code': 'AF', 'continent': 'Asia', 'name': 'Afghanistan', 'capital': 'Kabul'},
{'timezones': ['America/Antigua'], 'code': 'AG', 'continent': 'North America', 'name': 'Antigua and Barbuda', 'capital': "St. John's"},
{'timezones': ['Europe/Tirane'], 'code': 'AL', 'continent': 'Europe', 'name': 'Albania', 'capital': 'Tirana'},
{'timezones': ['Asia/Yerevan'], 'code': 'AM', 'continent': 'Asia', 'name': 'Armenia', 'capital': 'Yerevan'},
{'timezones': ['Africa/Luanda'], 'code': 'AO', 'continent': 'Africa', 'name': 'Angola', 'capital': 'Luanda'},
{'timezones': ['America/Argentina/Buenos_Aires', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/Tucuman', 'America/Argentina/Catamarca', 'America/Argentina/La_Rioja', 'America/Argentina/San_Juan', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Ushuaia'], 'code': 'AR', 'continent': 'South America', 'name': 'Argentina', 'capital': 'Buenos Aires'},
{'timezones': ['Europe/Vienna'], 'code': 'AT', 'continent': 'Europe', 'name': 'Austria', 'capital': 'Vienna'},
{'timezones': ['Australia/Lord_Howe', 'Australia/Hobart', 'Australia/Currie', 'Australia/Melbourne', 'Australia/Sydney', 'Australia/Broken_Hill', 'Australia/Brisbane', 'Australia/Lindeman', 'Australia/Adelaide', 'Australia/Darwin', 'Australia/Perth'], 'code': 'AU', 'continent': 'Oceania', 'name': 'Australia', 'capital': 'Canberra'},
{'timezones': ['Asia/Baku'], 'code': 'AZ', 'continent': 'Asia', 'name': 'Azerbaijan', 'capital': 'Baku'},
{'timezones': ['America/Barbados'], 'code': 'BB', 'continent': 'North America', 'name': 'Barbados', 'capital': 'Bridgetown'},
{'timezones': ['Asia/Dhaka'], 'code': 'BD', 'continent': 'Asia', 'name': 'Bangladesh', 'capital': 'Dhaka'},
{'timezones': ['Europe/Brussels'], 'code': 'BE', 'continent': 'Europe', 'name': 'Belgium', 'capital': 'Brussels'},
{'timezones': ['Africa/Ouagadougou'], 'code': 'BF', 'continent': 'Africa', 'name': 'Burkina Faso', 'capital': 'Ouagadougou'},
{'timezones': ['Europe/Sofia'], 'code': 'BG', 'continent': 'Europe', 'name': 'Bulgaria', 'capital': 'Sofia'},
{'timezones': ['Asia/Bahrain'], 'code': 'BH', 'continent': 'Asia', 'name': 'Bahrain', 'capital': 'Manama'},
{'timezones': ['Africa/Bujumbura'], 'code': 'BI', 'continent': 'Africa', 'name': 'Burundi', 'capital': 'Bujumbura'},
{'timezones': ['Africa/Porto-Novo'], 'code': 'BJ', 'continent': 'Africa', 'name': 'Benin', 'capital': 'Porto-Novo'},
{'timezones': ['Asia/Brunei'], 'code': 'BN', 'continent': 'Asia', 'name': 'Brunei Darussalam', 'capital': 'Bandar Seri Begawan'},
{'timezones': ['America/La_Paz'], 'code': 'BO', 'continent': 'South America', 'name': 'Bolivia', 'capital': 'Sucre'},
{'timezones': ['America/Noronha', 'America/Belem', 'America/Fortaleza', 'America/Recife', 'America/Araguaina', 'America/Maceio', 'America/Bahia', 'America/Sao_Paulo', 'America/Campo_Grande', 'America/Cuiaba', 'America/Porto_Velho', 'America/Boa_Vista', 'America/Manaus', 'America/Eirunepe', 'America/Rio_Branco'], 'code': 'BR', 'continent': 'South America', 'name': 'Brazil', 'capital': 'Brasilia'},
{'timezones': ['America/Nassau'], 'code': 'BS', 'continent': 'North America', 'name': 'Bahamas', 'capital': 'Nassau'},
{'timezones': ['Asia/Thimphu'], 'code': 'BT', 'continent': 'Asia', 'name': 'Bhutan', 'capital': 'Thimphu'},
{'timezones': ['Africa/Gaborone'], 'code': 'BW', 'continent': 'Africa', 'name': 'Botswana', 'capital': 'Gaborone'},
{'timezones': ['Europe/Minsk'], 'code': 'BY', 'continent': 'Europe', 'name': 'Belarus', 'capital': 'Minsk'},
{'timezones': ['America/Belize'], 'code': 'BZ', 'continent': 'North America', 'name': 'Belize', 'capital': 'Belmopan'},
{'timezones': ['America/St_Johns', 'America/Halifax', 'America/Glace_Bay', 'America/Moncton', 'America/Goose_Bay', 'America/Blanc-Sablon', 'America/Montreal', 'America/Toronto', 'America/Nipigon', 'America/Thunder_Bay', 'America/Pangnirtung', 'America/Iqaluit', 'America/Atikokan', 'America/Rankin_Inlet', 'America/Winnipeg', 'America/Rainy_River', 'America/Cambridge_Bay', 'America/Regina', 'America/Swift_Current', 'America/Edmonton', 'America/Yellowknife', 'America/Inuvik', 'America/Dawson_Creek', 'America/Vancouver', 'America/Whitehorse', 'America/Dawson'], 'code': 'CA', 'continent': 'North America', 'name': 'Canada', 'capital': 'Ottawa'},
{'timezones': ['Africa/Kinshasa', 'Africa/Lubumbashi'], 'code': 'CD', 'continent': 'Africa', 'name': 'Democratic Republic of the Congo', 'capital': 'Kinshasa'},
{'timezones': ['Africa/Brazzaville'], 'code': 'CG', 'continent': 'Africa', 'name': 'Republic of the Congo', 'capital': 'Brazzaville'},
{'timezones': ['Africa/Abidjan'], 'code': 'CI', 'continent': 'Africa', 'name': "Ivory Coast", 'capital': 'Yamoussoukro'},
{'timezones': ['America/Santiago', 'Pacific/Easter'], 'code': 'CL', 'continent': 'South America', 'name': 'Chile', 'capital': 'Santiago'},
{'timezones': ['Africa/Douala'], 'code': 'CM', 'continent': 'Africa', 'name': 'Cameroon', 'capital': 'Yaoundé'},
{'timezones': ['Asia/Shanghai', 'Asia/Harbin', 'Asia/Chongqing', 'Asia/Urumqi', 'Asia/Kashgar'], 'code': 'CN', 'continent': 'Asia', 'name': "China", 'capital': 'Beijing'},
{'timezones': ['America/Bogota'], 'code': 'CO', 'continent': 'South America', 'name': 'Colombia', 'capital': 'Bogotá'},
{'timezones': ['America/Costa_Rica'], 'code': 'CR', 'continent': 'North America', 'name': 'Costa Rica', 'capital': 'San José'},
{'timezones': ['America/Havana'], 'code': 'CU', 'continent': 'North America', 'name': 'Cuba', 'capital': 'Havana'},
{'timezones': ['Atlantic/Cape_Verde'], 'code': 'CV', 'continent': 'Africa', 'name': 'Cape Verde', 'capital': 'Praia'},
{'timezones': ['Asia/Nicosia'], 'code': 'CY', 'continent': 'Asia', 'name': 'Cyprus', 'capital': 'Nicosia'},
{'timezones': ['Europe/Prague'], 'code': 'CZ', 'continent': 'Europe', 'name': 'Czech Republic', 'capital': 'Prague'},
{'timezones': ['Europe/Berlin'], 'code': 'DE', 'continent': 'Europe', 'name': 'Germany', 'capital': 'Berlin'},
{'timezones': ['Africa/Djibouti'], 'code': 'DJ', 'continent': 'Africa', 'name': 'Djibouti', 'capital': 'Djibouti City'},
{'timezones': ['Europe/Copenhagen'], 'code': 'DK', 'continent': 'Europe', 'name': 'Denmark', 'capital': 'Copenhagen'},
{'timezones': ['America/Dominica'], 'code': 'DM', 'continent': 'North America', 'name': 'Dominica', 'capital': 'Roseau'},
{'timezones': ['America/Santo_Domingo'], 'code': 'DO', 'continent': 'North America', 'name': 'Dominican Republic', 'capital': 'Santo Domingo'},
{'timezones': ['America/Guayaquil', 'Pacific/Galapagos'], 'code': 'EC', 'continent': 'South America', 'name': 'Ecuador', 'capital': 'Quito'},
{'timezones': ['Europe/Tallinn'], 'code': 'EE', 'continent': 'Europe', 'name': 'Estonia', 'capital': 'Tallinn'},
{'timezones': ['Africa/Cairo'], 'code': 'EG', 'continent': 'Africa', 'name': 'Egypt', 'capital': 'Cairo'},
{'timezones': ['Africa/Asmera'], 'code': 'ER', 'continent': 'Africa', 'name': 'Eritrea', 'capital': 'Asmara'},
{'timezones': ['Africa/Addis_Ababa'], 'code': 'ET', 'continent': 'Africa', 'name': 'Ethiopia', 'capital': 'Addis Ababa'},
{'timezones': ['Europe/Helsinki'], 'code': 'FI', 'continent': 'Europe', 'name': 'Finland', 'capital': 'Helsinki'},
{'timezones': ['Pacific/Fiji'], 'code': 'FJ', 'continent': 'Oceania', 'name': 'Fiji', 'capital': 'Suva'},
{'timezones': ['Europe/Paris'], 'code': 'FR', 'continent': 'Europe', 'name': 'France', 'capital': 'Paris'},
{'timezones': ['Africa/Libreville'], 'code': 'GA', 'continent': 'Africa', 'name': 'Gabon', 'capital': 'Libreville'},
{'timezones': ['Asia/Tbilisi'], 'code': 'GE', 'continent': 'Asia', 'name': 'Georgia', 'capital': 'Tbilisi'},
{'timezones': ['Africa/Accra'], 'code': 'GH', 'continent': 'Africa', 'name': 'Ghana', 'capital': 'Accra'},
{'timezones': ['Africa/Banjul'], 'code': 'GM', 'continent': 'Africa', 'name': 'The Gambia', 'capital': 'Banjul'},
{'timezones': ['Africa/Conakry'], 'code': 'GN', 'continent': 'Africa', 'name': 'Guinea', 'capital': 'Conakry'},
{'timezones': ['Europe/Athens'], 'code': 'GR', 'continent': 'Europe', 'name': 'Greece', 'capital': 'Athens'},
{'timezones': ['America/Guatemala'], 'code': 'GT', 'continent': 'North America', 'name': 'Guatemala', 'capital': 'Guatemala City'},
{'timezones': ['America/Guatemala'], 'code': 'HT', 'continent': 'North America', 'name': 'Haiti', 'capital': 'Port-au-Prince'},
{'timezones': ['Africa/Bissau'], 'code': 'GW', 'continent': 'Africa', 'name': 'Guinea-Bissau', 'capital': 'Bissau'},
{'timezones': ['America/Guyana'], 'code': 'GY', 'continent': 'South America', 'name': 'Guyana', 'capital': 'Georgetown'},
{'timezones': ['America/Tegucigalpa'], 'code': 'HN', 'continent': 'North America', 'name': 'Honduras', 'capital': 'Tegucigalpa'},
{'timezones': ['Europe/Budapest'], 'code': 'HU', 'continent': 'Europe', 'name': 'Hungary', 'capital': 'Budapest'},
{'timezones': ['Asia/Jakarta', 'Asia/Pontianak', 'Asia/Makassar', 'Asia/Jayapura'], 'code': 'ID', 'continent': 'Asia', 'name': 'Indonesia', 'capital': 'Jakarta'},
{'timezones': ['Europe/Dublin'], 'code': 'IE', 'continent': 'Europe', 'name': 'Republic of Ireland', 'capital': 'Dublin'},
{'timezones': ['Asia/Jerusalem'], 'code': 'IL', 'continent': 'Asia', 'name': 'Israel', 'capital': 'Jerusalem'},
{'timezones': ['Asia/Calcutta'], 'code': 'IN', 'continent': 'Asia', 'name': 'India', 'capital': 'New Delhi'},
{'timezones': ['Asia/Baghdad'], 'code': 'IQ', 'continent': 'Asia', 'name': 'Iraq', 'capital': 'Baghdad'},
{'timezones': ['Asia/Tehran'], 'code': 'IR', 'continent': 'Asia', 'name': 'Iran', 'capital': 'Tehran'},
{'timezones': ['Atlantic/Reykjavik'], 'code': 'IS', 'continent': 'Europe', 'name': 'Iceland', 'capital': 'Reykjavík'},
{'timezones': ['Europe/Rome'], 'code': 'IT', 'continent': 'Europe', 'name': 'Italy', 'capital': 'Rome'},
{'timezones': ['America/Jamaica'], 'code': 'JM', 'continent': 'North America', 'name': 'Jamaica', 'capital': 'Kingston'},
{'timezones': ['Asia/Amman'], 'code': 'JO', 'continent': 'Asia', 'name': 'Jordan', 'capital': 'Amman'},
{'timezones': ['Asia/Tokyo'], 'code': 'JP', 'continent': 'Asia', 'name': 'Japan', 'capital': 'Tokyo'},
{'timezones': ['Africa/Nairobi'], 'code': 'KE', 'continent': 'Africa', 'name': 'Kenya', 'capital': 'Nairobi'},
{'timezones': ['Asia/Bishkek'], 'code': 'KG', 'continent': 'Asia', 'name': 'Kyrgyzstan', 'capital': 'Bishkek'},
{'timezones': ['Pacific/Tarawa', 'Pacific/Enderbury', 'Pacific/Kiritimati'], 'code': 'KI', 'continent': 'Oceania', 'name': 'Kiribati', 'capital': 'Tarawa'},
{'timezones': ['Asia/Pyongyang'], 'code': 'KP', 'continent': 'Asia', 'name': 'North Korea', 'capital': 'Pyongyang'},
{'timezones': ['Asia/Seoul'], 'code': 'KR', 'continent': 'Asia', 'name': 'South Korea', 'capital': 'Seoul'},
{'timezones': ['Asia/Kuwait'], 'code': 'KW', 'continent': 'Asia', 'name': 'Kuwait', 'capital': 'Kuwait'},
{'timezones': ['Asia/Beirut'], 'code': 'LB', 'continent': 'Asia', 'name': 'Lebanon', 'capital': 'Beirut'},
{'timezones': ['Europe/Vaduz'], 'code': 'LI', 'continent': 'Europe', 'name': 'Liechtenstein', 'capital': 'Vaduz'},
{'timezones': ['Africa/Monrovia'], 'code': 'LR', 'continent': 'Africa', 'name': 'Liberia', 'capital': 'Monrovia'},
{'timezones': ['Africa/Maseru'], 'code': 'LS', 'continent': 'Africa', 'name': 'Lesotho', 'capital': 'Maseru'},
{'timezones': ['Europe/Vilnius'], 'code': 'LT', 'continent': 'Europe', 'name': 'Lithuania', 'capital': 'Vilnius'},
{'timezones': ['Europe/Luxembourg'], 'code': 'LU', 'continent': 'Europe', 'name': 'Luxembourg', 'capital': 'Luxembourg City'},
{'timezones': ['Europe/Riga'], 'code': 'LV', 'continent': 'Europe', 'name': 'Latvia', 'capital': 'Riga'},
{'timezones': ['Africa/Tripoli'], 'code': 'LY', 'continent': 'Africa', 'name': 'Libya', 'capital': 'Tripoli'},
{'timezones': ['Indian/Antananarivo'], 'code': 'MG', 'continent': 'Africa', 'name': 'Madagascar', 'capital': 'Antananarivo'},
{'timezones': ['Pacific/Majuro', 'Pacific/Kwajalein'], 'code': 'MH', 'continent': 'Oceania', 'name': 'Marshall Islands', 'capital': 'Majuro'},
{'timezones': ['Europe/Skopje'], 'code': 'MK', 'continent': 'Europe', 'name': 'Macedonia', 'capital': 'Skopje'},
{'timezones': ['Africa/Bamako'], 'code': 'ML', 'continent': 'Africa', 'name': 'Mali', 'capital': 'Bamako'},
{'timezones': ['Asia/Rangoon'], 'code': 'MM', 'continent': 'Asia', 'name': 'Myanmar', 'capital': 'Naypyidaw'},
{'timezones': ['Asia/Ulaanbaatar', 'Asia/Hovd', 'Asia/Choibalsan'], 'code': 'MN', 'continent': 'Asia', 'name': 'Mongolia', 'capital': 'Ulaanbaatar'},
{'timezones': ['Africa/Nouakchott'], 'code': 'MR', 'continent': 'Africa', 'name': 'Mauritania', 'capital': 'Nouakchott'},
{'timezones': ['Europe/Malta'], 'code': 'MT', 'continent': 'Europe', 'name': 'Malta', 'capital': 'Valletta'},
{'timezones': ['Indian/Mauritius'], 'code': 'MU', 'continent': 'Africa', 'name': 'Mauritius', 'capital': 'Port Louis'},
{'timezones': ['Indian/Maldives'], 'code': 'MV', 'continent': 'Asia', 'name': 'Maldives', 'capital': 'Male'},
{'timezones': ['Africa/Blantyre'], 'code': 'MW', 'continent': 'Africa', 'name': 'Malawi', 'capital': 'Lilongwe'},
{'timezones': ['America/Mexico_City', 'America/Cancun', 'America/Merida', 'America/Monterrey', 'America/Mazatlan', 'America/Chihuahua', 'America/Hermosillo', 'America/Tijuana'], 'code': 'MX', 'continent': 'North America', 'name': 'Mexico', 'capital': 'Mexico City'},
{'timezones': ['Asia/Kuala_Lumpur', 'Asia/Kuching'], 'code': 'MY', 'continent': 'Asia', 'name': 'Malaysia', 'capital': 'Kuala Lumpur'},
{'timezones': ['Africa/Maputo'], 'code': 'MZ', 'continent': 'Africa', 'name': 'Mozambique', 'capital': 'Maputo'},
{'timezones': ['Africa/Windhoek'], 'code': 'NA', 'continent': 'Africa', 'name': 'Namibia', 'capital': 'Windhoek'},
{'timezones': ['Africa/Niamey'], 'code': 'NE', 'continent': 'Africa', 'name': 'Niger', 'capital': 'Niamey'},
{'timezones': ['Africa/Lagos'], 'code': 'NG', 'continent': 'Africa', 'name': 'Nigeria', 'capital': 'Abuja'},
{'timezones': ['America/Managua'], 'code': 'NI', 'continent': 'North America', 'name': 'Nicaragua', 'capital': 'Managua'},
{'timezones': ['Europe/Amsterdam'], 'code': 'NL', 'continent': 'Europe', 'name': 'Kingdom of the Netherlands', 'capital': 'Amsterdam'},
{'timezones': ['Europe/Oslo'], 'code': 'NO', 'continent': 'Europe', 'name': 'Norway', 'capital': 'Oslo'},
{'timezones': ['Asia/Katmandu'], 'code': 'NP', 'continent': 'Asia', 'name': 'Nepal', 'capital': 'Kathmandu'},
{'timezones': ['Pacific/Nauru'], 'code': 'NR', 'continent': 'Oceania', 'name': 'Nauru', 'capital': 'Yaren'},
{'timezones': ['Pacific/Auckland', 'Pacific/Chatham'], 'code': 'NZ', 'continent': 'Oceania', 'name': 'New Zealand', 'capital': 'Wellington'},
{'timezones': ['Asia/Muscat'], 'code': 'OM', 'continent': 'Asia', 'name': 'Oman', 'capital': 'Muscat'},
{'timezones': ['America/Panama'], 'code': 'PA', 'continent': 'North America', 'name': 'Panama', 'capital': 'Panama City'},
{'timezones': ['America/Lima'], 'code': 'PE', 'continent': 'South America', 'name': 'Peru', 'capital': 'Lima'},
{'timezones': ['Pacific/Port_Moresby'], 'code': 'PG', 'continent': 'Oceania', 'name': 'Papua New Guinea', 'capital': 'Port Moresby'},
{'timezones': ['Asia/Manila'], 'code': 'PH', 'continent': 'Asia', 'name': 'Philippines', 'capital': 'Manila'},
{'timezones': ['Asia/Karachi'], 'code': 'PK', 'continent': 'Asia', 'name': 'Pakistan', 'capital': 'Islamabad'},
{'timezones': ['Europe/Warsaw'], 'code': 'PL', 'continent': 'Europe', 'name': 'Poland', 'capital': 'Warsaw'},
{'timezones': ['Europe/Lisbon', 'Atlantic/Madeira', 'Atlantic/Azores'], 'code': 'PT', 'continent': 'Europe', 'name': 'Portugal', 'capital': 'Lisbon'},
{'timezones': ['Pacific/Palau'], 'code': 'PW', 'continent': 'Oceania', 'name': 'Palau', 'capital': 'Ngerulmud'},
{'timezones': ['America/Asuncion'], 'code': 'PY', 'continent': 'South America', 'name': 'Paraguay', 'capital': 'Asunción'},
{'timezones': ['Asia/Qatar'], 'code': 'QA', 'continent': 'Asia', 'name': 'Qatar', 'capital': 'Doha'},
{'timezones': ['Europe/Bucharest'], 'code': 'RO', 'continent': 'Europe', 'name': 'Romania', 'capital': 'Bucharest'},
{'timezones': ['Europe/Kaliningrad', 'Europe/Moscow', 'Europe/Volgograd', 'Europe/Samara', 'Asia/Yekaterinburg', 'Asia/Omsk', 'Asia/Novosibirsk', 'Asia/Krasnoyarsk', 'Asia/Irkutsk', 'Asia/Yakutsk', 'Asia/Vladivostok', 'Asia/Sakhalin', 'Asia/Magadan', 'Asia/Kamchatka', 'Asia/Anadyr'], 'code': 'RU', 'continent': 'Europe', 'name': 'Russia', 'capital': 'Moscow'},
{'timezones': ['Africa/Kigali'], 'code': 'RW', 'continent': 'Africa', 'name': 'Rwanda', 'capital': 'Kigali'},
{'timezones': ['Asia/Riyadh'], 'code': 'SA', 'continent': 'Asia', 'name': 'Saudi Arabia', 'capital': 'Riyadh'},
{'timezones': ['Pacific/Guadalcanal'], 'code': 'SB', 'continent': 'Oceania', 'name': 'Solomon Islands', 'capital': 'Honiara'},
{'timezones': ['Indian/Mahe'], 'code': 'SC', 'continent': 'Africa', 'name': 'Seychelles', 'capital': 'Victoria'},
{'timezones': ['Africa/Khartoum'], 'code': 'SD', 'continent': 'Africa', 'name': 'Sudan', 'capital': 'Khartoum'},
{'timezones': ['Europe/Stockholm'], 'code': 'SE', 'continent': 'Europe', 'name': 'Sweden', 'capital': 'Stockholm'},
{'timezones': ['Asia/Singapore'], 'code': 'SG', 'continent': 'Asia', 'name': 'Singapore', 'capital': 'Singapore'},
{'timezones': ['Europe/Ljubljana'], 'code': 'SI', 'continent': 'Europe', 'name': 'Slovenia', 'capital': 'Ljubljana'},
{'timezones': ['Europe/Bratislava'], 'code': 'SK', 'continent': 'Europe', 'name': 'Slovakia', 'capital': 'Bratislava'},
{'timezones': ['Africa/Freetown'], 'code': 'SL', 'continent': 'Africa', 'name': 'Sierra Leone', 'capital': 'Freetown'},
{'timezones': ['Europe/San_Marino'], 'code': 'SM', 'continent': 'Europe', 'name': 'San Marino', 'capital': 'San Marino'},
{'timezones': ['Africa/Dakar'], 'code': 'SN', 'continent': 'Africa', 'name': 'Senegal', 'capital': 'Dakar'},
{'timezones': ['Africa/Mogadishu'], 'code': 'SO', 'continent': 'Africa', 'name': 'Somalia', 'capital': 'Mogadishu'},
{'timezones': ['America/Paramaribo'], 'code': 'SR', 'continent': 'South America', 'name': 'Suriname', 'capital': 'Paramaribo'},
{'timezones': ['Asia/Damascus'], 'code': 'SY', 'continent': 'Asia', 'name': 'Syria', 'capital': 'Damascus'},
{'timezones': ['Africa/Lome'], 'code': 'TG', 'continent': 'Africa', 'name': 'Togo', 'capital': 'Lomé'},
{'timezones': ['Asia/Bangkok'], 'code': 'TH', 'continent': 'Asia', 'name': 'Thailand', 'capital': 'Bangkok'},
{'timezones': ['Asia/Dushanbe'], 'code': 'TJ', 'continent': 'Asia', 'name': 'Tajikistan', 'capital': 'Dushanbe'},
{'timezones': ['Asia/Ashgabat'], 'code': 'TM', 'continent': 'Asia', 'name': 'Turkmenistan', 'capital': 'Ashgabat'},
{'timezones': ['Africa/Tunis'], 'code': 'TN', 'continent': 'Africa', 'name': 'Tunisia', 'capital': 'Tunis'},
{'timezones': ['Pacific/Tongatapu'], 'code': 'TO', 'continent': 'Oceania', 'name': 'Tonga', 'capital': 'Nukualofa'},
{'timezones': ['Europe/Istanbul'], 'code': 'TR', 'continent': 'Asia', 'name': 'Turkey', 'capital': 'Ankara'},
{'timezones': ['America/Port_of_Spain'], 'code': 'TT', 'continent': 'North America', 'name': 'Trinidad and Tobago', 'capital': 'Port of Spain'},
{'timezones': ['Pacific/Funafuti'], 'code': 'TV', 'continent': 'Oceania', 'name': 'Tuvalu', 'capital': 'Funafuti'},
{'timezones': ['Africa/Dar_es_Salaam'], 'code': 'TZ', 'continent': 'Africa', 'name': 'Tanzania', 'capital': 'Dodoma'},
{'timezones': ['Europe/Kiev', 'Europe/Uzhgorod', 'Europe/Zaporozhye', 'Europe/Simferopol'], 'code': 'UA', 'continent': 'Europe', 'name': 'Ukraine', 'capital': 'Kyiv'},
{'timezones': ['Africa/Kampala'], 'code': 'UG', 'continent': 'Africa', 'name': 'Uganda', 'capital': 'Kampala'},
{'timezones': ['America/New_York', 'America/Detroit', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Indiana/Indianapolis', 'America/Indiana/Marengo', 'America/Indiana/Knox', 'America/Indiana/Vevay', 'America/Chicago', 'America/Indiana/Vincennes', 'America/Indiana/Petersburg', 'America/Menominee', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Denver', 'America/Boise', 'America/Shiprock', 'America/Phoenix', 'America/Los_Angeles', 'America/Anchorage', 'America/Juneau', 'America/Yakutat', 'America/Nome', 'America/Adak', 'Pacific/Honolulu'], 'code': 'US', 'continent': 'North America', 'name': 'United States', 'capital': 'Washington, D.C.'},
{'timezones': ['America/New_York', 'America/Detroit', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Indiana/Indianapolis', 'America/Indiana/Marengo', 'America/Indiana/Knox', 'America/Indiana/Vevay', 'America/Chicago', 'America/Indiana/Vincennes', 'America/Indiana/Petersburg', 'America/Menominee', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Denver', 'America/Boise', 'America/Shiprock', 'America/Phoenix', 'America/Los_Angeles', 'America/Anchorage', 'America/Juneau', 'America/Yakutat', 'America/Nome', 'America/Adak', 'Pacific/Honolulu'], 'code': 'USA', 'continent': 'North America', 'name': 'United States', 'capital': 'Washington, D.C.'},
{'timezones': ['America/Montevideo'], 'code': 'UY', 'continent': 'South America', 'name': 'Uruguay', 'capital': 'Montevideo'},
{'timezones': ['Asia/Samarkand', 'Asia/Tashkent'], 'code': 'UZ', 'continent': 'Asia', 'name': 'Uzbekistan', 'capital': 'Tashkent'},
{'timezones': ['Europe/Vatican'], 'code': 'VA', 'continent': 'Europe', 'name': 'Vatican City', 'capital': 'Vatican City'},
{'timezones': ['America/Caracas'], 'code': 'VE', 'continent': 'South America', 'name': 'Venezuela', 'capital': 'Caracas'},
{'timezones': ['Asia/Saigon'], 'code': 'VN', 'continent': 'Asia', 'name': 'Vietnam', 'capital': 'Hanoi'},
{'timezones': ['Pacific/Efate'], 'code': 'VU', 'continent': 'Oceania', 'name': 'Vanuatu', 'capital': 'Port Vila'},
{'timezones': ['Asia/Aden'], 'code': 'YE', 'continent': 'Asia', 'name': 'Yemen', 'capital': "Sana'a"},
{'timezones': ['Africa/Lusaka'], 'code': 'ZM', 'continent': 'Africa', 'name': 'Zambia', 'capital': 'Lusaka'},
{'timezones': ['Africa/Harare'], 'code': 'ZW', 'continent': 'Africa', 'name': 'Zimbabwe', 'capital': 'Harare'},
{'timezones': ['Africa/Algiers'], 'code': 'DZ', 'continent': 'Africa', 'name': 'Algeria', 'capital': 'Algiers'},
{'timezones': ['Europe/Sarajevo'], 'code': 'BA', 'continent': 'Europe', 'name': 'Bosnia and Herzegovina', 'capital': 'Sarajevo'},
{'timezones': ['Asia/Phnom_Penh'], 'code': 'KH', 'continent': 'Asia', 'name': 'Cambodia', 'capital': 'Phnom Penh'},
{'timezones': ['Africa/Bangui'], 'code': 'CF', 'continent': 'Africa', 'name': 'Central African Republic', 'capital': 'Bangui'},
{'timezones': ['Africa/Ndjamena'], 'code': 'TD', 'continent': 'Africa', 'name': 'Chad', 'capital': "N'Djamena"},
{'timezones': ['Indian/Comoro'], 'code': 'KM', 'continent': 'Africa', 'name': 'Comoros', 'capital': 'Moroni'},
{'timezones': ['Europe/Zagreb'], 'code': 'HR', 'continent': 'Europe', 'name': 'Croatia', 'capital': 'Zagreb'},
{'timezones': ['Asia/Dili'], 'code': 'TL', 'continent': 'Asia', 'name': 'East Timor', 'capital': 'Dili'},
{'timezones': ['America/El_Salvador'], 'code': 'SV', 'continent': 'North America', 'name': 'El Salvador', 'capital': 'San Salvador'},
{'timezones': ['Africa/Malabo'], 'code': 'GQ', 'continent': 'Africa', 'name': 'Equatorial Guinea', 'capital': 'Malabo'},
{'timezones': ['America/Grenada'], 'code': 'GD', 'continent': 'North America', 'name': 'Grenada', 'capital': "St. George's"},
{'timezones': ['Asia/Almaty', 'Asia/Qyzylorda', 'Asia/Aqtobe', 'Asia/Aqtau', 'Asia/Oral'], 'code': 'KZ', 'continent': 'Asia', 'name': 'Kazakhstan', 'capital': 'Astana'},
{'timezones': ['Asia/Vientiane'], 'code': 'LA', 'continent': 'Asia', 'name': 'Laos', 'capital': 'Vientiane'},
{'timezones': ['Pacific/Truk', 'Pacific/Ponape', 'Pacific/Kosrae'], 'code': 'FM', 'continent': 'Oceania', 'name': 'Federated States of Micronesia', 'capital': 'Palikir'},
{'timezones': ['Europe/Chisinau'], 'code': 'MD', 'continent': 'Europe', 'name': 'Moldova', 'capital': 'Chisinau'},
{'timezones': ['Europe/Monaco'], 'code': 'MC', 'continent': 'Europe', 'name': 'Monaco', 'capital': 'Monaco'},
{'timezones': ['Europe/Podgorica'], 'code': 'ME', 'continent': 'Europe', 'name': 'Montenegro', 'capital': 'Podgorica'},
{'timezones': ['Africa/Casablanca'], 'code': 'MA', 'continent': 'Africa', 'name': 'Morocco', 'capital': 'Rabat'},
{'timezones': ['America/St_Kitts'], 'code': 'KN', 'continent': 'North America', 'name': 'Saint Kitts and Nevis', 'capital': 'Basseterre'},
{'timezones': ['America/St_Lucia'], 'code': 'LC', 'continent': 'North America', 'name': 'Saint Lucia', 'capital': 'Castries'},
{'timezones': ['America/St_Vincent'], 'code': 'VC', 'continent': 'North America', 'name': 'Saint Vincent and the Grenadines', 'capital': 'Kingstown'},
{'timezones': ['Pacific/Apia'], 'code': 'WS', 'continent': 'Oceania', 'name': 'Samoa', 'capital': 'Apia'},
{'timezones': ['Europe/Belgrade'], 'code': 'RS', 'continent': 'Europe', 'name': 'Serbia', 'capital': 'Belgrade'},
{'timezones': ['Africa/Johannesburg'], 'code': 'ZA', 'continent': 'Africa', 'name': 'South Africa', 'capital': 'Pretoria'},
{'timezones': ['Europe/Madrid', 'Africa/Ceuta', 'Atlantic/Canary'], 'code': 'ES', 'continent': 'Europe', 'name': 'Spain', 'capital': 'Madrid'},
{'timezones': ['Europe/Madrid', 'Africa/Ceuta', 'Atlantic/Canary'], 'code': 'CAT', 'continent': 'Europe', 'name': 'Spain', 'capital': 'Madrid'},
{'timezones': ['Asia/Colombo'], 'code': 'LK', 'continent': 'Asia', 'name': 'Sri Lanka', 'capital': 'Sri Jayewardenepura Kotte'},
{'timezones': ['Africa/Mbabane'], 'code': 'SZ', 'continent': 'Africa', 'name': 'Swaziland', 'capital': 'Mbabane'},
{'timezones': ['Europe/Zurich'], 'code': 'CH', 'continent': 'Europe', 'name': 'Switzerland', 'capital': 'Bern'},
{'timezones': ['Asia/Dubai'], 'code': 'AE', 'continent': 'Asia', 'name': 'United Arab Emirates', 'capital': 'Abu Dhabi'},
{'timezones': ['Europe/London'], 'code': 'GB', 'continent': 'Europe', 'name': 'United Kingdom', 'capital': 'London'},
{'timezones': ['Europe/London'], 'code': 'UK', 'continent': 'Europe', 'name': 'United Kingdom', 'capital': 'London'},
{'timezones': ['Europe/London'], 'code': 'HK', 'continent': 'Asia', 'name': 'Honk Kong', 'capital': 'Honk Kong'},
{'timezones': ['Europe/London'], 'code': 'PR', 'continent': 'South America', 'name': 'Puerto Rico', 'capital': 'Puerto Rico'},
{'timezones': ['Europe/London'], 'code': 'DSC', 'continent': 'Desconocido', 'name': 'Desconocido', 'capital': 'Desconocido'},
{'timezones': ['America'], 'code': 'GF', 'continent': 'South America', 'name': 'French Guiana', 'capital': 'Caiena'},
{'timezones': ['Europe/Amsterdam'], 'code': 'NL', 'continent': 'Europe', 'name': 'Netherlands', 'capital': 'Amsterdam'}]
    colores = []
    while len(colores)!=len(paises):
        color = "#"+"%06x" % random.randint(0, 0xFFFFFF)
        if color not in colores:
            colores.append(color)
    x = []
    y = []
    dicci_pais = {}    
    iniciales = []
    paises_leyenda = []
    
    for pais in paises:
        if pais not in paises_leyenda:
            paises_leyenda.append(pais)
        for pai in countries:
            if pai['name'] == pais:
                iniciales.append(pai['code'].casefold())
                cant = paises.count(pais)
                dicci_pais[pai['code']]=cant
                break
    for key in dicci_pais:
        x.append(key)
        y.append(dicci_pais[key])

    return x,y,colores,paises_leyenda,iniciales


def estacion_meteorologica(fechas):   #0 al inico= minimo, 0 a la derecha= maximo, xx = cualquier numero
    
    Primavera = {"03":"021",
                 "04":"xx",
                 "05":"xx",
                 "06":"210",}
    
    Verano = {"06":"022",
              "07":"xx",
              "08":"xx",
              "09":"230"}
    
    Otonio = {"09":"023",
              "10":"xx",
              "11":"xx",
              "12":"210"}

    Invierno = {"12":"022",
                "01":"xx",
                "02":"xx",
                "03":"200",} 
    cant_p= 0
    cant_v= 0
    cant_o= 0
    cant_i= 0
    for fecha in fechas:
        mes = fecha[3:5]
        dia = fecha[0:2]
        
        pk= list(Primavera.keys()) 
        pv= list(Primavera.values())
        #######PRIMAVERA#########
        vk= list(Verano.keys())
        vv= list(Verano.values())
        #########VERANO##########
        ok= list(Otonio.keys())
        ov= list(Otonio.values())
        ##########OTONIO#########
        ik= list(Invierno.keys())
        iv= list(Invierno.values())
        #########INVIERNO########
        if mes in pk:
            if mes == pk[0] and int(dia) >= int(pv[0][1]+pv[0][2]): #puede o no ser de primavera, depende del dia.
                cant_p += 1
                continue
            elif mes == pk[3] and int(dia) <= int(pv[3][0]+pv[3][1]) : #puede o no ser de primavera, depende del dia.
                cant_p += 1
                continue
            elif mes == pk[1] or mes == pk[2]: #pertenece a primavera independientemente del dia
                cant_p += 1
                continue 
        elif mes in vk:
            if mes == vk[0] and int(dia) >= int(vv[0][1]+vv[0][2]): #puede o no ser de verano, depende del dia.
                cant_v +=1
                continue
            elif mes == vk[3] and int(dia) <= int(vv[3][0]+vv[3][1]) : #puede o no ser de verano, depende del dia.
                cant_v += 1
                continue
            elif mes == vk[1] or mes == vk[2]: #pertenece a verano independientemente del dia
                cant_v += 1 
                continue
        elif mes in ok:
            if mes == ok[0] and int(dia) >= int(ov[0][1]+ov[0][2]): #puede o no ser de otoño, depende del dia.
                cant_o += 1
                continue
            elif mes == ok[3] and int(dia) <= int(ov[3][0]+ov[3][1]) : #puede o no ser de otoño, depende del dia.
                cant_o += 1
                continue
            elif mes == ok[1] or mes == ok[2]: #pertenece a otoño independientemente del dia
                cant_o += 1
                continue
        else: #por descarte tiene que ser invierno si o si.
            cant_i += 1
    cantidades=[cant_p,cant_v,cant_o,cant_i]
    return cantidades


elegir_banda()
