def FP(SalarioBasico,SMMLV,AuxilioTransporte):
    """
    Este función entrega
    fp --> factor prestacional que aplica según el caso
    CostoMes --> Entrega cuanto le vale el mes a la empresa el empleado
    CostoHora -->  Entrega cuanto le vale la hora a la empresa el empleado
    HoraSuministro --> Entrega cuanto cobrar por la hora  de suminstro, aplicando factor k
    """
    #Prestaciones
    Cesantias=8.33
    InteresCesantias=1
    PrimaServ=8.33
    EPS = 8.5
    Vacaciones = 4.17
    AFP = 12
    ARL = 6.96
    CostoMes = 0

    fk = 194.4

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
    HoraSuministro=CostoMes/fk
    return FP,CostoMes,CostoHora,HoraSuministro

def Cantidad(a,b):
    if a%b==0:
        #donde TrafoDia2 corresponde a la cantidad de trafos que marca una pareja en un día, es una cte del inicio
        return int(a/b)
    else:
        return int(a/b)+1