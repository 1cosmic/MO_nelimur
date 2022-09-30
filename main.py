import sys
from math import sin

from PyQt5.QtWidgets import QDialog, QApplication
from mainGUI import Ui_Dialog


# Main func of searching the roots.
def f(x):
    # User input Params of linur.
    global c_a, c_b, c_c, c_k, c_e
    return (c_a * pow(x, 2) + c_b * x + c_c) * sin(c_k * x + c_e)


class MainWin(QDialog):
    def __init__(self):
        self.ErrorPersent = 0.05

        super(QDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonDihotomy.clicked.connect(self.methodDihotomy)

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

        output = self.ui.outputField
        output.clear()
        output.setFocus()

        for root in roots:
            out = f"Root: {root}"
            output.appendPlainText(out)

        else:
            output.appendPlainText("")
            result = f"Count of roots: {len(roots)}"
            # output.appendPlainText(result)
            output.appendHtml(f"<b>{result}</b>")

    def isolations(self):
        isolations = []

        step = 1
        start = int(self.ui.rangeA.value())
        end = int(self.ui.rangeB.value())

        # Generate of intervals.
        intervals = [(i, i + step) for i in range(start, end, step)]

        # Select interval, who have roots.
        for i in intervals:

            left = int(i[0])
            right = int(i[1])
            if f(left) * f(right) < 0:
                isolations.append(i)

        print(f"Start: {start}\t End: {end}")
        print(isolations)

        return isolations

    def methodDihotomy(self):
        # output roots into the user range.

        # Get user values of Coefficients.
        self.setUserValues()

        roots = []  # roots of math solver.
        cRoots = 0  # count of roots (optimization).

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
                    roots.append(c)
                    # print(f"Find root: {c}")
                    cRoots += 1;
                    run = False

        else:
            print(f"Find of roots: {cRoots}")
            self.outputRoots(roots)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MainWin()
    Window.show()
    sys.exit(app.exec_())
