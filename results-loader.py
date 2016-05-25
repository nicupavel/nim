import numpy
import sys
from evalfuncs import *
from terminaltables import AsciiTable, DoubleTable, SingleTable
import plotly as py
import plotly.graph_objs as go

# 'PSO-evalfuncs.Sixhump-5, GA-evalfuncs.Sixhump-10-True # example key names

tableData = [
    ["Algo", "Rastrigin", "", "", "Griewangk",  "", "",  "Rosenbrock",  "", "", "Sixhump", "", ""],
    [" ", "5", "10", "30", "5", "10", "30", "5", "10", "30", "5", "10", "30"]

]

results = numpy.load(sys.argv[1]).item()
funcs = (Rastrigin, Griewangk, Rosenbrock, Sixhump)
axes = (5, 10, 30)
# GA
for t in [False, True]:
    tableRow = []
    tableRowStdDev = []
    #algoName = str(f).split(".")[1]
    algoName = "GA"
    if t:
        algoName += " Hybrid"
    tableRow.append(algoName)
    tableRowStdDev.append("   Std Dev")
    for f in funcs:

        for a in axes:
            name = "GA-" + str(f) + "-" + str(a)+ "-" + str(t)
            keyMean = name + "-mean"
            keyStdDev = name + "-std"
            m = results[keyMean]
            s = results[keyStdDev]
            #tableRow.append("{:10.2f}".format(m) + "/" + "{:10.2f}".format(s))
            tableRow.append("{:10.2f}".format(m))
            tableRowStdDev.append("{:10.2f}".format(s))

    tableData.append(tableRow)
    tableData.append(tableRowStdDev)


# PSO
tableRow = []
tableRowStdDev = []
#algoName = str(f).split(".")[1]
algoName = "PSO"
tableRow.append(algoName)
tableRowStdDev.append("   Std Dev")
for f in funcs:

    for a in axes:
        name = "PSO-" + str(f) + "-" + str(a)
        keyMean = name + "-mean"
        keyStdDev = name + "-std"
        m = results[keyMean]
        s = results[keyStdDev]
        #tableRow.append("{:10.2f}".format(m) + "/" + "{:10.2f}".format(s))
        tableRow.append("{:10.2f}".format(m))
        tableRowStdDev.append("{:10.2f}".format(s))

tableData.append(tableRow)
tableData.append(tableRowStdDev)

#from pprint import pprint
#pprint(results)
#pprint(tableData)

#table = DoubleTable(tableData, 'Natural Methods')

table = SingleTable(tableData, 'Natural Methods')
table.inner_heading_row_border = False

#table.justify_columns[2] = 'right'
print()
print(table.table)

for f in funcs:
    for a in axes:
        graphData = []
        #GA-evalfuncs.Sixhump-10-True
        nameGA = "GA-" + str(f) + "-" + str(a)+ "-" + "False"
        nameGAHybrid = "GA-" + str(f) + "-" + str(a)+ "-" + "True"
        namePSO = "PSO-" + str(f) + "-" + str(a)

        info = str(f).split(".")[1] + "-" + str(a) + " axes"

        gGA = go.Scatter(y = sorted(results[nameGA], reverse=True), mode='lines', name='GA ' + info )
        gGAHybrid = go.Scatter(y = sorted(results[nameGAHybrid], reverse=True ), mode='lines', name='GA Hybrid ' + info)
        gPSO = go.Scatter(y = sorted(results[namePSO], reverse=True ), mode='lines', name='PSO ' + info)

        graphData.append(gGA)
        graphData.append(gGAHybrid)
        graphData.append(gPSO)

        py.offline.plot(graphData, filename='graph'+ info + '.html')
