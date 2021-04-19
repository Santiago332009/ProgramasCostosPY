import pandas as pd
import calendar

#Desmarcación de 30000 transformadores
def FP(SalarioBasico,SMMLV,AuxilioTransporte):
    #Prestaciones
    Cesantias=8.33
    InteresCesantias=1
    PrimaServ=8.33
    EPS = 8.5
    Vacaciones = 4.17
    AFP = 12
    ARL = 6.96
    CostoMes = 0

    # Parafiscales
    Sena = 2
    CajaCompesacion = 4
    ICBF = 3

    if SalarioBasico <= 2 * SMMLV:
        print("Salario<=2SMMLV")
        ParaFiscales = CajaCompesacion - EPS
        CostoMes = AuxilioTransporte
    elif SalarioBasico > 2 * SMMLV and SalarioBasico <= 10 * SMMLV:
        print("Salario>2SMMLV y Salario<10SMMLV")
        ParaFiscales = CajaCompesacion - EPS
        CostoMes = 0
    elif SalarioBasico > 10 * SMMLV:
        print("Salario>10SMMLV")
        ParaFiscales = Sena + CajaCompesacion + ICBF  # Sena, Caja de compesación, ICBF
        CostoMes = 0
    FP = Cesantias + InteresCesantias + PrimaServ + EPS + Vacaciones + AFP + ARL + ParaFiscales + 100  # Factor prestacional
    FP = FP / 100
    CostoMes=SalarioBasico*FP+CostoMes
    CostoHora=CostoMes/240
    return FP,CostoMes,CostoHora

def Cantidad(a,b):
    if a%b==0:
        #donde TrafoDia2 corresponde a la cantidad de trafos que marca una pareja en un día, es una cte del inicio
        return int(a/b)
    else:
        return int(a/b)+1

#Constantes
SMMLV=908526 #
AuxilioTransporte=106454

SMDLV=SMMLV/30

NumTrafos=30e3     #Transformadores a marcar

#Viaticos
Desayuno=0.47*SMDLV
Almuerzo=0.47*SMDLV
Cena=0.47*SMDLV
Hospedaje=1.06*SMDLV

ViaticosDia=Desayuno+Almuerzo+Cena+Hospedaje

TrafoDia2=7

#Plazo del proyecto
PlazoProyecto=120 #Días calendario sin domingo, ni festivos, ni recargo
MesesProyecto=PlazoProyecto/30
Dominicales=PlazoProyecto/30*4

holyDays=pd.DataFrame(columns=["Months","Holy Days"])
months = ["Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
holyDays["Months"]=months
holyDays["Holy Days"]=[2,0,1,3,2,2,2,2,0,1,2,2]
holydays=sum(holyDays["Holy Days"][3:7])
holydays=0

DiasActivos=PlazoProyecto-Dominicales-holydays

#Costos por unidad
Cu=pd.DataFrame(columns=["Oficio","SB","fp","CuMesNomina","CuMesViaticos","CuMes"]) #Donde SB--> Salario básico tope, es decir, mínimo
Cu["Oficio"]=["Admistrador o ingeniero","supervisor","Oficial Operativo","Ayudante Operativo","Digitador"]
Cu["SB"]=[5*SMMLV,4*SMMLV,2.5*SMMLV,1.7*SMMLV,2*SMMLV]

fp=[]
CostoU=[]
CuViaticos=[]
for i in Cu["SB"]:
    fp1,Vmes1,Vhora1=FP(i,SMMLV,AuxilioTransporte)
    fp.append(fp1)
    CostoU.append(Vmes1)
    CuViaticos.append(ViaticosDia*30*fp1)

Cu["fp"]=fp #Factor de prestaciones
Cu["CuMesNomina"]=CostoU
Cu["CuMesViaticos"]=CuViaticos
Cu["CuMes"]=Cu["CuMesNomina"]+Cu["CuMesViaticos"]

###################################################Herramientas
Tools=pd.DataFrame(columns=["Descripción","Valor"])
Tools["Descripción"]=["Escal 11pel, fibraVidrio","EquipoProteccion","Dotación P,C,Z","PlacaDemarcacionTrafo"]
Tools["Valor"]=[12e5,7e4,15e4,785e2]

#####################################################Personal necesario

Persona=pd.DataFrame(columns=["Tipo de empleado","Qty","$ Mes","$ Proyecto"])

TypeEmployee=["Oficial","Ayudante","SupervisorCampo","Ingeniero","Digitador","OficialImprovisto","AyudanteImprovisto"]
Persona["Tipo de empleado"]=TypeEmployee

#Defino la cantidad trafos por día, quedo realizar, para cumplir proyecto
TrafosDia=Cantidad(NumTrafos,DiasActivos)

#defino la cantidad de parejas opertivas para marcar trafos
Qty=[]
Qty.append(Cantidad(TrafosDia,TrafoDia2))
Qty.append(Cantidad(TrafosDia,TrafoDia2))

#Defino supervisores de campo
Qty.append(Cantidad(Qty[0],3))

#Defino Ingenieto
Qty.append(Cantidad(Qty[-1],2))

#Defino Digitador
Qty.append(Cantidad(Qty[-2],4))

#Defino Oficial y ayudante improvisto
Qty.append(Cantidad(Qty[0],12))
Qty.append(Cantidad(Qty[0],12))

Persona["Qty"]=Qty

Vmes_personal=[]
VPersonProyec=[]

KeyPerson=Persona.keys()

Persona[KeyPerson[2]]=[Cu["CuMes"][2],Cu["CuMes"][3],Cu["CuMes"][1],Cu["CuMes"][0],Cu["CuMes"][4],Cu["CuMes"][2],Cu["CuMes"][3]]
Persona[KeyPerson[3]]=Persona[KeyPerson[1]]*Persona[KeyPerson[2]]

NominaPersonal=sum(Persona[KeyPerson[-1]])*MesesProyecto

#########################################################Transporte
Transporte=0
"Transporte Operarios"
Busetas=Cantidad(Qty[0],4)
CostoDiarioBuseta=25e4
CostoDiaBus=CostoDiarioBuseta*Busetas
CostoProyectoBus=CostoDiaBus*DiasActivos
CostoMesBus=CostoProyectoBus/MesesProyecto

Transporte=CostoProyectoBus

"TransporteIngenieros"
TransporteInge=50000
TransporteIngeProyecto=TransporteInge*DiasActivos*Persona["Qty"][3]

Transporte=Transporte+TransporteIngeProyecto
GastoRepresentacion=10e3*DiasActivos*Persona["Qty"][3]

"Transporte Supervisores"
CdMoto=40000
CuMoto=CdMoto*DiasActivos
MotoProyect=CuMoto*Persona["Qty"][2]
CamarasSupervisor=Persona["Qty"][2]*250000

Transporte=Transporte+MotoProyect

CuPlanMinutos=90e3
PlanMinutosProyect=CuPlanMinutos*MesesProyecto*(Persona["Qty"][3]+Persona["Qty"][4]+Persona["Qty"][2])
PcPorttatil=12e5*(Persona["Qty"][3]+Persona["Qty"][4]+Persona["Qty"][2])
Celular=65e4*(Persona["Qty"][3]+Persona["Qty"][4]+Persona["Qty"][2])
Arriendo=55e5*MesesProyecto
Vigilancia=350e3*MesesProyecto

TotalProyect=NominaPersonal+Transporte+GastoRepresentacion+CamarasSupervisor+PlanMinutosProyect+PcPorttatil+Celular+Arriendo+Vigilancia

#Resumen info
print("\nResumenInfo")
print("\nDías de trabajo:",DiasActivos )
print("Viático_día:",ViaticosDia)
print("Viático_día*FP:",ViaticosDia*Cu["fp"][0])
print("Total Nomina Proyecto:",NominaPersonal)
print("Transporte:",Transporte)
print("\nTotalProyect",TotalProyect)
