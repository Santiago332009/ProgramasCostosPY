import sys
from PyQt5 import uic, QtWidgets
#import main

qtCreatorFile = "CostoHora.ui" # Nombre del archivo aquí

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.Calcular.clicked.connect(self.Values)

    def Values(self):
        Cesantias=float(window.Cesantia.text())
        InteresCesantias=float(window.lineEdit_2.text())
        PrimaServ=float(window.lineEdit_3.text())
        EPS=float(window.lineEdit_5.text())
        Vacaciones=float(window.lineEdit_4.text())
        ARL=float(window.lineEdit_6.text())
        AFP=float(window.lineEdit_12.text())
        CostoMes=0

        #Parafiscales
        Sena=float(window.lineEdit_7.text())
        CajaCompesacion=float(window.lineEdit_8.text())
        ICBF=float(window.lineEdit_9.text())

        SMMLV=float(window.lineEdit.text())
        AuxilioTransporte=float(window.lineEdit_10.text())
        SalarioBasico=float(window.lineEdit_11.text())

        Factor_K=float(window.lineEdit_13.text())

        if SalarioBasico<=2*SMMLV:
            state="Salario<=2SMMLV"
            print(state)
            ParaFiscales=CajaCompesacion-EPS
            CostoMes=AuxilioTransporte
        elif SalarioBasico>2*SMMLV and SalarioBasico<=10*SMMLV:
            state="Salario>2SMMLV y Salario<10SMMLV"
            print(state)
            ParaFiscales=CajaCompesacion-EPS
            CostoMes=0
        elif SalarioBasico>10*SMMLV:
            state="Salario>10SMMLV"
            print(state)
            ParaFiscales=Sena+CajaCompesacion+ICBF #Sena, Caja de compesación, ICBF
            CostoMes=0

        FP=Cesantias+InteresCesantias+PrimaServ+EPS+Vacaciones+AFP+ARL+ParaFiscales+100  #Factor prestacional
        FP=FP/100
        print("Factor Prestacional:",FP)
        CostoMes=SalarioBasico*FP+CostoMes
        print("Costo Mes:",CostoMes)
        CostoHora=CostoMes/240
        Horasuministro=CostoMes/Factor_K
        print("Costo Hora:",CostoHora)
        self.Resultado.setText(state+"\n"
                               "Factor Prestacional: "+str(FP)+"\n"
                                "Costo mes: "+str(CostoMes)+"\n"
                               "Costo hora: "+str(CostoHora)+"\n"
                               "Hora de suministro: "+str(Horasuministro))


if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
