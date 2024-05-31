import sys
import cmath
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6 import QtWidgets
import design1  # Importă design-ul

def Trig2Cart(rho, theta):
    x = rho * cmath.cos(theta)
    y = rho * cmath.sin(theta)
    return x + y * 1j

def Cart2Trig(z):
    x = z.real
    y = z.imag
    modul = math.sqrt(x**2 + y**2)
    argument = cmath.phase(z)
    return (modul, argument)

def DeseneazaLista(ax, ListaZ, culoare='blue', marime=10):
    x = [z.real for z in ListaZ]
    y = [z.imag for z in ListaZ]
    ax.plot(x, y, color=culoare)
    ax.scatter(x, y, color=culoare, s=marime)

def DeseneazaCerc(z0, r, NumarPuncte=100):
    ListaZ = []
    for k in range(NumarPuncte):
        theta = 2 * math.pi * k / NumarPuncte
        z = z0 + Trig2Cart(r, theta)
        ListaZ.append(z)
    ListaZ.append(ListaZ[0])  # Închide cercul
    return ListaZ
def DeseneazaSemicerc(z0, r, NumarPuncte=100):
    ListaZ = []
    for k in range(NumarPuncte // 2 + 1):  # Desenăm doar jumătate din puncte pentru semicerc
        theta = math.pi * k / (NumarPuncte // 2)
        z = z0 + Trig2Cart(r, theta)
        ListaZ.append(z)
    return ListaZ
def DeseneazaDisc(ax, z0, r, culoare='blue', NumarPuncte=100):
    ListaZ = []
    for k in range(NumarPuncte):
        theta = 2 * math.pi * k / NumarPuncte
        z = z0 + Trig2Cart(r, theta)
        ListaZ.append(z)
    x = [z.real for z in ListaZ]
    y = [z.imag for z in ListaZ]
    ax.fill(x, y, color=culoare)

def DeseneazaSegment(z1, z2, NumarPuncte=100):
    ListaZ = []
    for k in range(NumarPuncte + 1):  # Adăugat +1 pentru a include punctul final
        t = k / NumarPuncte
        z = (1 - t) * z1 + t * z2
        ListaZ.append(z)
    return ListaZ

def DeseneazaTriunghi(z1, z2, z3):
    return DeseneazaSegment(z1, z2) + DeseneazaSegment(z2, z3)[1:] + DeseneazaSegment(z3, z1)[1:]

def DeseneazaPatrulater(z1, z2, z3, z4):
    return DeseneazaSegment(z1, z2) + DeseneazaSegment(z2, z3)[1:] + DeseneazaSegment(z3, z4)[1:] + DeseneazaSegment(z4, z1)[1:]

def DeseneazaPoligon(z0, r, num_sides):
    ListaZ = []
    for k in range(num_sides):
        theta = 2 * math.pi * k / num_sides
        z = z0 + Trig2Cart(r, theta)
        ListaZ.append(z)
    ListaZ.append(ListaZ[0])  # Închide poligonul
    Segmente = []
    for i in range(len(ListaZ) - 1):
        Segmente += DeseneazaSegment(ListaZ[i], ListaZ[i + 1])
    return Segmente


def DeseneazaCoronaCirculara(z0, r1, r2, NumarPuncte=100):
    ListaZ = []
    for r in [r1, r2]:
        for k in range(NumarPuncte):
            theta = 2 * math.pi * k / NumarPuncte
            z = z0 + Trig2Cart(r, theta)
            ListaZ.append(z)
        ListaZ.append(ListaZ[0])  # Închide cercul
    return ListaZ
def DeseneazaUnghi(z1, z2, z3):
    # z1 este vârful unghiului
    # z2 și z3 sunt punctele de final ale segmentelor ce formează unghiul
    segment1 = DeseneazaSegment(z1, z2)
    segment2 = DeseneazaSegment(z1, z3)
    return segment1 + segment2


# Funcții pentru transformări
def translatie(ListaZ, t):
    return [z + t for z in ListaZ]

def rotatie(ListaZ, theta):
    return [cmath.exp(1j * theta) * z for z in ListaZ]

def omotetie(ListaZ, lambd):
    return [lambd * z for z in ListaZ]

def simetrieConj(ListaZ):
    return [z.conjugate() for z in ListaZ]

def inversiune(ListaZ):
    return [1 / z for z in ListaZ if z != 0]
def transformare_power_alpha(ListaZ, alpha):
    return [z**alpha for z in ListaZ]

def transformare_sin(ListaZ):
    return [cmath.sin(z) for z in ListaZ]

def transformare_cos(ListaZ):
    return [cmath.cos(z) for z in ListaZ]

def transformare_log(ListaZ):
    return [cmath.log(z) for z in ListaZ if z != 0]

def transformare_e20(ListaZ):
    return [1j * (z**2 + 2j*z + 1) / (z**2 - 2j*z + 1) for z in ListaZ]
class MainApp(QtWidgets.QMainWindow, design1.Ui_Dialog):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)

        # Initializare canvas matplotlib pentru fiecare QGraphicsView
        self.figure1, self.ax1 = plt.subplots()
        self.canvas1 = FigureCanvas(self.figure1)
        self.graphicsView.setScene(QtWidgets.QGraphicsScene())
        self.graphicsView.scene().addWidget(self.canvas1)

        self.figure2, self.ax2 = plt.subplots()
        self.canvas2 = FigureCanvas(self.figure2)
        self.graphicsView_2.setScene(QtWidgets.QGraphicsScene())
        self.graphicsView_2.scene().addWidget(self.canvas2)

        # Adăugarea opțiunilor în combobox
        self.comboBox.addItems(["Cerc","Semicerc", "Segment", "Triunghi", "Patrulater", "Pentagon", "Hexagon", "Coronă Circulară", "Disc", "Unghi"])

        # Conectarea butoanelor la funcții
        self.pushButton.clicked.connect(self.apply_transformation)
        self.pushButton_2.clicked.connect(self.save_image)
        self.comboBox.currentIndexChanged.connect(self.draw_figure)

        self.pushButton_3.clicked.connect(self.save_function)
        self.comboBox.currentIndexChanged.connect(self.draw_figure)
        self.functions_list = []
    def draw_figure(self):
        try:
            self.ax1.clear()
            self.ax1.axhline(y=0, color='r', linestyle='-')
            self.ax1.axvline(x=0, color='r', linestyle='-')
            figure_type = self.comboBox.currentText()
            ListaZ = []

            if figure_type == 'Cerc':
                z0 = 0 + 0j
                r = 1.5
                ListaZ = DeseneazaCerc(z0, r)
            elif figure_type == 'Semicerc':
                z0 = 0 + 0j
                r = 1
                ListaZ=DeseneazaSemicerc(z0,r)
            elif figure_type == 'Segment':
                z1 = -2 + 1j
                z2 = 2 + 1j
                ListaZ = DeseneazaSegment(z1, z2)
            elif figure_type == 'Triunghi':
                z1 = 0 + 0j
                z2 = 1 + 0j
                z3 = 0.5 + 1j
                ListaZ = DeseneazaTriunghi(z1, z2, z3)
            elif figure_type == 'Patrulater':
                z1 = 0 + 0j
                z2 = 1 + 0j
                z3 = 1 + 1j
                z4 = 0 + 1j
                ListaZ = DeseneazaPatrulater(z1, z2, z3, z4)
            elif figure_type == 'Pentagon':
                z0 = 0 + 0j
                r = 1
                ListaZ = DeseneazaPoligon(z0, r, 5)
            elif figure_type == 'Hexagon':
                z0 = 0 + 0j
                r = 1
                ListaZ = DeseneazaPoligon(z0, r, 6)
            elif figure_type == 'Coronă Circulară':
                z0 = 0 + 0j
                r1 = 1
                r2 = 2
                ListaZ = DeseneazaCoronaCirculara(z0, r1, r2)
            elif figure_type == 'Disc':
                z0 = 0 + 0j
                r = 1
                DeseneazaDisc(self.ax1, z0, r, culoare='blue')
            elif figure_type == 'Unghi':
                z1 = 0 + 0j  # Vârful unghiului
                z2 = 1 + 0j  # Punct final al primului segment
                z3 = 0.5 + 1j  # Punct final al celui de-al doilea segment
                ListaZ = DeseneazaUnghi(z1, z2, z3)

            DeseneazaLista(self.ax1, ListaZ)
            self.original_figura = ListaZ  # Salvează figura originală
            self.ax1.set_aspect('equal')
            self.canvas1.draw()
        except Exception as e:
            print(f"A apărut o eroare: {e}")

    def apply_transformation(self):
        try:
            self.ax2.clear()
            self.ax2.axhline(y=0, color='r', linestyle='-')
            self.ax2.axvline(x=0, color='r', linestyle='-')
            transformation = self.textEdit.toPlainText()
            ListaZ = self.original_figura[:]  # Copiază figura originală

            # Aplicați transformarea specificată
            if transformation == "translatie":
                ListaZ = translatie(ListaZ, 1 + 1j)
            elif transformation == "rotatie":
                ListaZ = rotatie(ListaZ, math.pi / 4)
            elif transformation == "omotetie":
                ListaZ = omotetie(ListaZ, 1.5)
            elif transformation == "simetrieConj":
                ListaZ = simetrieConj(ListaZ)
            elif transformation == "inversiune":
                ListaZ = inversiune(ListaZ)
            elif transformation == "e20":
                ListaZ = transformare_e20(ListaZ)
            elif transformation.startswith("power_alpha"):
                try:
                    _, alpha_str = transformation.split()
                    alpha = float(alpha_str)
                    if alpha > 0:
                        ListaZ = transformare_power_alpha(ListaZ, alpha)
                except ValueError:
                    print("Eroare: specificați un alpha valid pentru transformarea power_alpha")
            elif transformation == "sin":
                ListaZ = transformare_sin(ListaZ)
            elif transformation == "cos":
                ListaZ = transformare_cos(ListaZ)
            elif transformation == "log":
                ListaZ = transformare_log(ListaZ)
            else:
                # Evaluarea funcției personalizate introduse de utilizator
                try:
                    func = eval(f"lambda z: {transformation}", {"cmath": cmath, "math": math})
                    ListaZ = [func(z) for z in ListaZ]
                except Exception as e:
                    print(f"Eroare în evaluarea funcției: {e}")

            DeseneazaLista(self.ax2, ListaZ, 'red')
            self.ax2.set_aspect('equal')
            self.canvas2.draw()
        except Exception as e:
            print(f"A apărut o eroare: {e}")

    def save_image(self):
        # Salvarea imaginii din graphicsView_2
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Salvează Imaginea", "", "PNG Files (*.png);;All Files (*)")
        if file_path:
            self.figure2.savefig(file_path)

    def save_function(self):
        try:
            function_text = self.textEdit.toPlainText()
            if function_text:
                self.functions_list.append(function_text)
                self.listWidget.addItem(function_text)
                self.textEdit.clear()
        except Exception as e:
            print(f"A apărut o eroare: {e}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
