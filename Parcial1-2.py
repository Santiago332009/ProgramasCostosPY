import numpy as np
import pandas as pd

import ModuloFuncionesCostos as fc

#Constantes
SMMLV=908526 #
SMDLV=SMMLV/30

AuxilioTransporte=106454
SB=SMMLV

fp,CostoMes,CostoHora,HoraSuministro = fc.FP(SB,SMMLV,AuxilioTransporte)

PaintHome = 30500    #Número de fachadas de casas por pintar
PlazoProyecto=180
MesesProyecto=PlazoProyecto/30
Dominicales=MesesProyecto*4

holyDays=[2,0,1,3,2,2,2,2,0,1,2,2]
MeanHoly=int(np.mean(holyDays)*MesesProyecto)
MeanHoly=0

DiasActivos=PlazoProyecto-Dominicales-MeanHoly
#------------------------------------------Viáticos------------------------------------------

#Viaticos por día
Viaticos={"Desayuno":0.45*SMDLV,"Almuerzo":0.47*SMDLV,"Cena":0.45*SMDLV,
          "Hospedaje":1.16*SMDLV}


ViaticosFp={} #Viaticos por día con el factor prestacional

for i in list(Viaticos.keys()):
    ViaticosFp[i]=Viaticos[i]*fp

#---------------------Costos para todo el proyecto

Costos={
    "Transporte Administrativo": 250e3,
    "Exámenes medicos ingreso y egreso": 16e5,
    "Trabajo en alturas":150e3,
    "Capacitaciones salud ocupacional":2e6,
    "Inducción":2e6,
    "Servicios públicos":16e5,
    "Adecuaciones":7e6,
    "Gastos representativos":500e3,
    "PapeleriaEventos":8e5,
    "Correspondecia":1e6,
    "Construcción fuera del proyecto":5e6
}

#---------------------Entrega de la información
Camara=250e3

##---------------------Salario Mano de Obra
SBobra={
    "Ingeniero":6*SMMLV,
    "Supervisor":4.5*SMMLV,
    "Técnico":2*SMMLV,
    "Ayudante":1.6*SMMLV,
    "Digitador":2*SMMLV
}
#---------------------Equipo y herramienta
tools={
    "Escalera":12e5,
    "Equipo de protección":7e5,
    "Dotacion pareja":180e3,
    "Brocha":13000*5,
    "Pintura":78e3
}

#---------------------Anexo técnico, cantiidad de profecionales
#Una pareja pinta 7 casas por día
Casas_dia=round(PaintHome/DiasActivos)

Parejas=round(Casas_dia/7)
#Parejas=30

Supervisores=round(Parejas/3)

ingeniero=round(Supervisores/2)
digitador=round(Supervisores/2)

QtyBuses=fc.Cantidad(Parejas,4)
CostoBuses=280e3

QtyMotos=Supervisores
CostoMoto=30e3

TransporteIngeniero=ingeniero
CostoTransporteInge=50e3
GastoRepresentacion=10e3

OficialAdicional=round(Parejas/12)

PlanMinutos=90e3 #Supervisor,Ingeniero y digitador, precio mes
Portatil=12e5
Celular=650e3

Bodega=55e4
Vigalancia=350e3


#-----------------------------------------------Costo unidad profesional
Cu=pd.DataFrame(columns=["Oficio","SB","CostoHora","HoraSuministro"])

Cu["Oficio"]=SBobra.keys()
Profesionales=SBobra.keys()

SB=[]
CostoHora=[]
HoraSuministro=[]

for i in Cu['Oficio']:
    FP,CostoMes,CostHora,HoraSuministr=fc.FP(SBobra[i],SMMLV,AuxilioTransporte)
    SB.append(CostoMes)
    CostoHora.append(CostHora)
    HoraSuministro.append(HoraSuministr)

Cu["SB"]=SB
Cu["CostoHora"]=CostoHora
Cu["HoraSuministro"]=HoraSuministro

#-------------------------------------------Valor viaticos
ViaticosPersonalDia=0

for i in ViaticosFp.keys():
    if i=="Hospedaje":
        #Agregamos impuesto del 11% al hospedaje
        ViaticosPersonalDia=ViaticosPersonalDia+ViaticosFp[i]*1.11
    else:
        ViaticosPersonalDia = ViaticosPersonalDia + ViaticosFp[i]

ViaticosPersonalMes=ViaticosPersonalDia*30

Cu=Cu.assign(Viaticos=ViaticosPersonalMes)
Cu=Cu.assign(CostoMes=Cu["SB"]+Cu["Viaticos"])

#--------------------------------------Valor Nomina mes
Nomina=pd.DataFrame(columns=["Oficio","Qty","ValorMes"])

Nomina["Oficio"]=Profesionales
Nomina["Qty"]=[ingeniero,Supervisores,Parejas+OficialAdicional,Parejas,digitador]

Nomina["ValorMes"]=Cu["CostoMes"]*Nomina["Qty"]
via=pd.DataFrame.from_dict(ViaticosFp,orient='index').rename(columns={0:'Qunatity'})


tools = pd.DataFrame([[key, tools[key]] for key in tools.keys()], columns=['Tipo', 'Valor'])
tools=tools.assign(Qty=[Parejas,Parejas,Parejas*2,5*PaintHome,PaintHome])

## este coementario

asdasd


dsadsad

asdasd
dsadasd