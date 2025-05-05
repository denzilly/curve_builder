from rateslib import *
import csv
from datetime import datetime
import matplotlib.pyplot as plt


class Curve_Builder():
    def __init__(self):

        self.curve = None
        self.instruments = []
        self.instrument_values = []
        self.nodes = {}

    def import_nodes(self):
        with open('nodes.csv') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                self.nodes[datetime.strptime(row[0], "%Y-%m-%d")] = 1.0

    def import_instruments(self, curve):
        args = dict(calendar="all", frequency="a",
                    convention="act365f", payment_lag=0, curves=curve)
        with open('instruments.csv') as d:
            reader = csv.reader(d, delimiter=',')
            for row in reader:
                self.instruments.append(IRS(datetime.strptime(
                    row[0], "%Y-%m-%d"), datetime.strptime(row[1], "%Y-%m-%d"), **args))
                self.instrument_values.append(float(row[2]))

    def construct_curve(self, t):
        return Curve(
            nodes=self.nodes,
            convention="act365f",
            calendar="all",
            t=t,
        )

    def construct_solver(self, curve):
        return Solver(
            curves=[curve],
            instruments=self.instruments,
            s=self.instrument_values
        )


# new object
cb = Curve_Builder()
# import nodes from file and build empty curve object
cb.import_nodes()
log_linear_curve = cb.construct_curve(t=NoInput(0))

# import instruments, attach curve to IRS objects
cb.import_instruments(log_linear_curve)
cb.construct_solver(log_linear_curve)

log_linear_curve.plot("1b")
plt.show()
