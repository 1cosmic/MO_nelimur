import sys
import time

from math import sin, cos, sqrt
import numpy

from PyQt5.QtWidgets import QDialog, QApplication
from mainGUI import Ui_Dialog


# Main func of searching the roots.
def f(x):
    # User input Params of linur.
    global c_a, c_b, c_c, c_k, c_e
    return (c_a * pow(x, 2) + c_b * x + c_c) * sin(c_k * x + c_e)


def fDif(x):
    # Return answer of difFur.
    global c_a, c_b, c_c, c_k, c_e
    y = c_k * (c_a * pow(x, 2) + c_b * x + c_c) * cos(c_k * x + c_e) + (2 * c_a * x + c_b) * sin(c_k * x + c_e)

    return y

def first_divDiff(x, nextX):
    # First divisor of difference.
    result = (f(x) - f(nextX)) / (x - nextX)

    return result


def second_divDiff(x, nextX, doubleNextX):
    # Second divisor of difference.

    divisor = first_divDiff(x, nextX) - first_divDiff(nextX, doubleNextX)
    denominator = x - doubleNextX
    result = divisor / denominator

    return result


def Q(x, ):
    f_k = f(x)


class MainWin(QDialog):
    ErrorPersent: float

    def __init__(self):
        self.lastTime = None
        self.ErrorPersent = 0.001

        super(QDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonDihotomy.clicked.connect(self.methodDihotomy)
        self.ui.buttonNeuton.clicked.connect(self.methodNeuton)
        self.ui.buttonSecant.clicked.connect(self.methodSecant)
        self.ui.buttonParabola.clicked.connect(self.methodParabol)

    def setUserValues(self):

        # User input Params of linur.
        global c_a, c_b, c_c, c_k, c_e
        c_a = self.ui.boxA.value()
        c_b = self.ui.boxB.value()
        c_c = self.ui.boxC.value()
        c_k = self.ui.boxK.value()
        c_e = self.ui.boxE.value()

    def outputRoots(self, roots, iterations):
        # Output values into the box-field.

        # Shutdown timer
        timing = f'{self.deltaTimer():0.4f}'

        output = self.ui.outputField
        output.clear()
        output.setFocus()

        roots.sort()

        for root in roots:
            out = f"Root: {root}"
            output.appendPlainText(out)

        else:
            output.appendPlainText("")

            # output.appendPlainText(result)
            result = f"Finding of roots: {len(roots)} in {timing}s."
            output.appendHtml(f"<b>{result}</b>")

            result = f"Count of iterations: {iterations}"
            output.appendHtml(f"<b>{result}</b>")

    def isolations(self, ifBack=False):
        isolations = []
        k = 1 / (self.ui.boxK.value() + self.ui.boxE.value())
        print(k)

        if ifBack:
            end = int(self.ui.rangeA.value())
            start = int(self.ui.rangeB.value())
            step = -k

        else:
            start = int(self.ui.rangeA.value())
            end = int(self.ui.rangeB.value())
            step = k

        # Generate of intervals.
        intervals = [(i, i + step) for i in numpy.arange(start, end, step)]

        # Select interval, who have roots.
        for i in intervals:

            left = float(i[0])
            right = float(i[1])
            if f(left) * f(right) < 0:
                isolations.append(i)

        # print(f"Start: {start}\t End: {end}")
        # print(isolations)

        return isolations

    def methodDihotomy(self):
        # output roots into the user range.

        # Get user values of Coefficients.
        self.setUserValues()

        roots = []  # roots of math solver.
        iterations = 0


        self.setTimer()
        for i in self.isolations():

            run = True
            a = i[0]
            b = i[1]

            while run:

                iterations += 1
                c = (a + b) / 2

                if (f(a) * f(c)) <= 0:
                    b = c
                else:
                    a = c

                if abs(b - a) <= self.ErrorPersent:
                    roots.append(round(c, 2))
                    # print(f"Find root: {c}")
                    # cRoots += 1;
                    run = False

        else:
            # print(f"Find of roots: {cRoots}")
            self.outputRoots(roots, iterations)

    def methodNeuton(self):
        # Searching roots using method of Neuton.

        # Get user values of Coefficients.
        self.setUserValues()
        self.setTimer()

        roots = []  # roots of math solver.
        iterations = 0

        reverseOrder = True
        isolations = self.isolations(reverseOrder)
        leftWall = 1

        for i in isolations:

            lastX = i[leftWall]
            h = 1

            while abs(h) > self.ErrorPersent:

                h = (f(lastX) / fDif(lastX))
                lastX -= h
                iterations += 1

                if abs(h) <= self.ErrorPersent:
                    roots.append(round(lastX, 2))


        self.outputRoots(roots, iterations)

        # ============================================================
        # ????????????????!
        # ============================================================
        #
    def methodSecant(self):
        # Calculate roots using method of Secants.
        self.setUserValues()
        self.setTimer()

        roots = []
        iterations = 0

        reverseOrder = True
        isolations = self.isolations(reverseOrder)

        for i in isolations:

            lastX = i[1]
            secondLastX = i[0]
            h = 1

            while abs(lastX - secondLastX) > self.ErrorPersent:

                h = ((f(lastX) * (lastX - secondLastX))) / (f(lastX) - f(secondLastX))
                secondLastX = lastX
                lastX -= h
                iterations += 1

                if abs(lastX - secondLastX) <= self.ErrorPersent:
                    roots.append(round(lastX, 2))

        self.outputRoots(roots, iterations)

        pass
        # ============================================================
        # ============================================================
    def methodParabol(self):
        # Calculate roots using method of Secants.
        self.setUserValues()
        self.setTimer()

        roots = []
        iterations = 0

        reverseOrder = True
        isolations = self.isolations(reverseOrder)

        for i in isolations:

            k = i[1]
            k1 = (i[1] - i[0]) / 2
            k2 = i[0]

            while abs(k1 - k) > self.ErrorPersent:
                a = (first_divDiff(k, k1) - first_divDiff(k1, k2)) / (k - k2)
                b = first_divDiff(k, k1) - second_divDiff(k, k1, k2) * (k + k1)
                c = f(k) - first_divDiff(k, k1) * k + second_divDiff(k, k1, k2) * k * k1

                x1_ = (-b - sqrt(pow(b, 2) - 4 * a * c)) / (2 * a)
                x2_ = (-b + sqrt(pow(b, 2) - 4 * a * c)) / (2 * a)

                k = k1
                k1 = k2
                iterations += 1

                if abs(f(x1_)) < abs(f(x2_)):
                    k2 = x1_
                else:
                    k2 = x2_

            else:
                roots.append(round(k2, 2))

        self.outputRoots(roots, iterations)


    def setTimer(self):
        # Set timer.
        self.lastTime = time.perf_counter()

    def deltaTimer(self):
        # Calculate of delta timer.
        return time.perf_counter() - self.lastTime


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MainWin()
    Window.show()
    sys.exit(app.exec_())
