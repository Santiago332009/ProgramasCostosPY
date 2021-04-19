SMMLV=908526 #
SalarioBasico=19e5
SalarioBasico=15e5
SalarioBasico=45e5
AuxilioTransporte=106454

Cesantias=8.33
InteresCesantias=1
PrimaServ=8.33
EPS=8.5
Vacaciones=4.17
AFP=12
ARL=6.96
CostoMes=0

#Parafiscale
Sena=2
CajaCompesacion=4
ICBF=3

if SalarioBasico<=2*SMMLV:
    print("Salario<=2SMMLV")
    ParaFiscales=CajaCompesacion-EPS
    CostoMes=AuxilioTransporte
elif SalarioBasico>2*SMMLV and SalarioBasico<=10*SMMLV:
    print("Salario>2SMMLV y Salario<10SMMLV")
    ParaFiscales=CajaCompesacion-EPS
    CostoMes=0
elif SalarioBasico>10*SMMLV:
    print("Salario>10SMMLV")
    ParaFiscales=Sena+CajaCompesacion+ICBF #Sena, Caja de compesación, ICBF
    CostoMes=0

FP=Cesantias+InteresCesantias+PrimaServ+EPS+Vacaciones+AFP+ARL+ParaFiscales+100  #Factor prestacional
FP=FP/100
print("Factor Prestacional:",FP)
CostoMes=SalarioBasico*FP+CostoMes
print("Costo Mes:",CostoMes)
CostoHora=CostoMes/240
print("Costo Hora:",CostoHora)