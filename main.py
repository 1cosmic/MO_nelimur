import sys
import time

from math import sin, cos

from PyQt5.QtWidgets import QDialog, QApplication
from mainGUI import Ui_Dialog


# Main func of searching the roots.
def f(x):
    # User input Params of linur.
    global c_a, c_b, c_c, c_k, c_e
    return (c_a * pow(x, 2) + c_b * x + c_c) * sin(c_k * x + c_e)


def fDif(x):
    # Return answer of difFur.
    y = (2 * c_a * x + c_b) * sin(c_k * x + c_e) + (c_a * pow(x, 2) + c_b * x + c_c) * cos(c_k * x + c_e)
    return y


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

    def setUserValues(self):

        # User input Params of linur.
        global c_a, c_b, c_c, c_k, c_e
        c_a = self.ui.boxA.value()
        c_b = self.ui.boxB.value()
        c_c = self.ui.boxC.value()
        c_k = self.ui.boxK.value()
        c_e = self.ui.boxE.value()

    def outputRoots(self, roots):
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

            result = f"Finding of roots: {len(roots)} in {timing}s."
            # output.appendPlainText(result)
            output.appendHtml(f"<b>{result}</b>")

    def isolations(self, ifBack=False):
        isolations = []

        if ifBack:
            end = int(self.ui.rangeA.value())
            start = int(self.ui.rangeB.value())
            step = -1

        else:
            start = int(self.ui.rangeA.value())
            end = int(self.ui.rangeB.value())
            step = 1

        # Generate of intervals.
        intervals = [(i, i + step) for i in range(start, end, step)]

        # Select interval, who have roots.
        for i in intervals:

            left = int(i[0])
            right = int(i[1])
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
        cRoots = 0  # count of roots (optimization).

        self.setTimer()
        for i in self.isolations():

            run = True
            a = i[0]
            b = i[1]

            while run:

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
            self.outputRoots(roots)

    def methodNeuton(self):
        # Searching roots using method of Neuton.

        # Get user values of Coefficients.
        self.setUserValues()
        self.setTimer()

        roots = []  # roots of math solver.

        reverseOrder = True
        isolations = self.isolations(reverseOrder)
        leftWall = 1

        for i in isolations:

            lastX = i[leftWall]
            h = 10

            while abs(h) > self.ErrorPersent:

                h = (f(lastX) / fDif(lastX))
                lastX -= h

                if abs(h) <= self.ErrorPersent:
                    roots.append(round(lastX, 2))

        self.outputRoots(roots)

        # ============================================================
        # ДОПИСАТЬ!
        # ============================================================
        #
        # def methodSecant(self):
        #     # Calculate roots using method of Secants.
        #     self.setUserValues()
        #     self.setTimer()
        #
        #     roots = []
        #
        #     reverseOrder = True
        #     leftWall = 1
        #     isolations = self.isolations(reverseOrder)
        #
        #     for i in isolations:
        #
        #         secondLastX = 'ДОПИСАТЬ МЕТОД СЕКУЩИХ'
        #         h = 10
        #
        #         lastX = f(i[leftWall])
        #         secondLastX = f()
        #
        #         while abs(h) > self.ErrorPersent:
        #
        #             h = (f(lastX) / fDif(lastX))
        #             lastX -= h
        #
        #             if abs(h) <= self.ErrorPersent:
        #                 roots.append(round(lastX, 2))
        #
        #     self.outputRoots(roots)
        #
        #     pass
        # ============================================================
        # ============================================================

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
