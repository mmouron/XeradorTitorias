# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmPrincipal.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmPrincipal(object):
    def setupUi(self, frmPrincipal):
        frmPrincipal.setObjectName("frmPrincipal")
        frmPrincipal.resize(1081, 740)
        self.centralwidget = QtWidgets.QWidget(frmPrincipal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnNovoGrupo = QtWidgets.QPushButton(self.centralwidget)
        self.btnNovoGrupo.setObjectName("btnNovoGrupo")
        self.horizontalLayout.addWidget(self.btnNovoGrupo)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnCargarDatos = QtWidgets.QPushButton(self.centralwidget)
        self.btnCargarDatos.setObjectName("btnCargarDatos")
        self.horizontalLayout.addWidget(self.btnCargarDatos)
        self.btnGardarDatos = QtWidgets.QPushButton(self.centralwidget)
        self.btnGardarDatos.setObjectName("btnGardarDatos")
        self.horizontalLayout.addWidget(self.btnGardarDatos)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnXerarTitores = QtWidgets.QPushButton(self.centralwidget)
        self.btnXerarTitores.setObjectName("btnXerarTitores")
        self.horizontalLayout.addWidget(self.btnXerarTitores)
        self.verticalLayout.addLayout(self.horizontalLayout)
        frmPrincipal.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(frmPrincipal)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1081, 24))
        self.menubar.setObjectName("menubar")
        self.menuAplicaci_n = QtWidgets.QMenu(self.menubar)
        self.menuAplicaci_n.setObjectName("menuAplicaci_n")
        frmPrincipal.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(frmPrincipal)
        self.statusbar.setObjectName("statusbar")
        frmPrincipal.setStatusBar(self.statusbar)
        self.mnuCargarDatos = QtWidgets.QAction(frmPrincipal)
        self.mnuCargarDatos.setObjectName("mnuCargarDatos")
        self.mnuGardarDatos = QtWidgets.QAction(frmPrincipal)
        self.mnuGardarDatos.setObjectName("mnuGardarDatos")
        self.mnuXerarTitores = QtWidgets.QAction(frmPrincipal)
        self.mnuXerarTitores.setObjectName("mnuXerarTitores")
        self.mnuSair = QtWidgets.QAction(frmPrincipal)
        self.mnuSair.setObjectName("mnuSair")
        self.menuAplicaci_n.addAction(self.mnuCargarDatos)
        self.menuAplicaci_n.addAction(self.mnuGardarDatos)
        self.menuAplicaci_n.addSeparator()
        self.menuAplicaci_n.addAction(self.mnuXerarTitores)
        self.menuAplicaci_n.addSeparator()
        self.menuAplicaci_n.addAction(self.mnuSair)
        self.menubar.addAction(self.menuAplicaci_n.menuAction())

        self.retranslateUi(frmPrincipal)
        QtCore.QMetaObject.connectSlotsByName(frmPrincipal)

    def retranslateUi(self, frmPrincipal):
        _translate = QtCore.QCoreApplication.translate
        frmPrincipal.setWindowTitle(_translate("frmPrincipal", "Asignación de titorías"))
        self.btnNovoGrupo.setText(_translate("frmPrincipal", "Engadir grupo"))
        self.btnCargarDatos.setText(_translate("frmPrincipal", "Cargar datos..."))
        self.btnGardarDatos.setText(_translate("frmPrincipal", "Gardar datos..."))
        self.btnXerarTitores.setText(_translate("frmPrincipal", "Xerar listado de titorías"))
        self.menuAplicaci_n.setTitle(_translate("frmPrincipal", "Aplicación"))
        self.mnuCargarDatos.setText(_translate("frmPrincipal", "Cargar datos..."))
        self.mnuGardarDatos.setText(_translate("frmPrincipal", "Gardar datos..."))
        self.mnuXerarTitores.setText(_translate("frmPrincipal", "Xerar lista de titores"))
        self.mnuSair.setText(_translate("frmPrincipal", "Sair"))

