#Importamos as clases de procesado XML, as de GUI e outras necesarias
import os
import collections
from functools import partial
from GUI.frmPrincipal import Ui_frmPrincipal
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QFileDialog, QMessageBox
from xeradorInforme import xeradorInforme

class ComboBoxNoWheel(QtWidgets.QComboBox):
    def wheelEvent (self, event):
        event.ignore()

class ventanaXeradorTitorias(QtWidgets.QMainWindow, Ui_frmPrincipal):

    def __init__(self, parent=None):
        super(ventanaXeradorTitorias, self).__init__(parent)
        self.setupUi(self)
        #Conectamos los eventos con los slots
        self.btnCargarDatos.clicked.connect(self.cargar_datos)
        self.mnuCargarDatos.triggered.connect(self.cargar_datos)
        self.btnGardarDatos.clicked.connect(self.salvar_datos)
        self.mnuGardarDatos.triggered.connect(self.salvar_datos)
        self.btnNovoGrupo.clicked.connect(self.engadir_grupo)
        self.btnXerarTitores.clicked.connect(self.xerar_titores)
        self.mnuXerarTitores.triggered.connect(self.xerar_titores)
        self.mnuSair.triggered.connect(self.salir)
        #Xeramos unha matriz de 1x10 para meter datos iniciais....
        self.table = self.tableWidget
        self.table.setColumnCount(10)
        self.cargar_listado_profes()
        #Engadimos unha fila para 1º de ESO A
        self.table.setRowCount(1)
        self.table.horizontalHeader().setVisible(False)
        fila_grupo1 = QtWidgets.QTableWidgetItem("1ESOA")
        # Poñermos o nome do grupo soma só lectura na primeira columna
        fila_grupo1.setFlags(QtCore.Qt.ItemIsEnabled)
        self.table.setItem(0, 0, fila_grupo1)
        #Introducimos combos en branco para os nomes dos profes
        for index in range(1,10):
            #Nas seguintes columnas insertamos un combo co listado de profes (neste caso só nomes en branco)
            #combo = QtWidgets.QComboBox()
            combo=ComboBoxNoWheel()
            combo.setEditable(True)
            combo.setFocusPolicy(QtCore.Qt.StrongFocus)
            #Preparamos o menú contextual dos combo
            combo.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            #Outro xeito de pasar parámetros adicionais aos manexadores... ;)
            combo.customContextMenuRequested.connect(partial(self.mostrar_menu_contextual,combo, 0, index))
            #Engadimos un primeiro nome baleiro
            combo.addItem("--")
            #Agora engadimos os profes recollidos do ficheiro de profes
            for t in self.listaprofes:
                combo.addItem(t)
            self.table.setCellWidget(0, index, combo)
            #Axustamos o ancho das columnas para que se vexan os nomes
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(index, QtWidgets.QHeaderView.ResizeToContents)
            #Interceptamos o sinal de índice cambiado para facer comprobacións cando se seleccione outro profesor
            combo.currentIndexChanged.connect(lambda state, fila=0, columna=index: self.refrescar_datos_tabla(fila,columna))
        self.leer_datos_tabla()

    def mostrar_menu_contextual(self, combo, n_fila, n_col, pos):
        menu = QtWidgets.QMenu()
        clear_action = menu.addAction("Limpiar candidato")
        block_action = menu.addAction("Bloquear candidato")
        unblock_action = menu.addAction("Desbloquear candidato")
        #action = menu.exec_(self.mapToGlobal(QtCore.QPoint(combo.x(),combo.y())))
        action = menu.exec_(self.mapToParent(QtCore.QPoint(combo.x(),combo.y())))
        if action == clear_action:
            #Mover todos os candidatos da dereita cara a esquerda para tapar esta nova posición baleira
            if n_col == 9 or self.table.cellWidget(n_fila, n_col+1).currentText() == "--":
                self.table.cellWidget(n_fila, n_col).setCurrentIndex(0)
            else:
                for pos in range(n_col,9):
                    self.leer_datos_tabla()
                    if self.table.cellWidget(n_fila, pos+1).currentText() != "--":
                        nome_profesor=self.table.cellWidget(n_fila, pos+1).currentText()
                        self.table.cellWidget(n_fila, pos + 1).setCurrentIndex(0)
                        self.table.cellWidget(n_fila, pos).setCurrentIndex(combo.findText(nome_profesor, QtCore.Qt.MatchFixedString))

        if action == block_action:
            combo.setItemIcon(combo.currentIndex(),QtGui.QIcon("iconos/block.png"))
            #QMessageBox.information(self, 'Menú de contexto', 'Función non implementada... :(')
        if action == unblock_action:
            #QMessageBox.information(self, 'Menú de contexto', 'Función non implementada... :(')
            combo.setItemIcon(combo.currentIndex(),QtGui.QIcon(""))

    def cargar_listado_profes(self):
        self.listaprofes = sorted(open("profesores.txt").read().splitlines())

    def cargar_datos(self):
        fileName = QFileDialog.getOpenFileName(self, 'Salvar estado do programa', '', "*.xt")
        if fileName:
            f1 = open(fileName[0], 'r')
            #Limpamos a táboa
            self.table.setRowCount(0)
            #Engadimos unha fila para o primeiro grupo
            self.table.insertRow(0)
            self.table.horizontalHeader().setVisible(False)
            linea_fichero=f1.readline()
            existe_grupo=False
            if linea_fichero:
                fila_grupo1 = QtWidgets.QTableWidgetItem(linea_fichero.strip(os.linesep))
                # Poñemos o nome do grupo coma só lectura na primeira columna
                fila_grupo1.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.setItem(0, 0, fila_grupo1)
                existe_grupo=True
            while existe_grupo:
                num_fila = self.table.rowCount() - 1
                #Introducimos combos para os nomes dos profes, pero cargando os datos do ficheiro gardado
                for index in range(1,10):
                    #Nas seguintes columnas insertamos un combo co listado de profes (neste caso só nomes en branco)
                    #combo = QtWidgets.QComboBox()
                    combo=ComboBoxNoWheel()
                    #Preparamos o menú contextual dos combo
                    combo.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                    combo.customContextMenuRequested.connect(partial(self.mostrar_menu_contextual, combo, num_fila, index))
                    combo.setEditable(True)
                    #Engadimos un primeiro nome baleiro
                    combo.addItem("--")
                    #Agora engadimos os profes recollidos do ficheiro de profes
                    for t in self.listaprofes:
                        combo.addItem(t)
                    self.table.setCellWidget(num_fila, index, combo)
                    #Axustamos o ancho das columnas para que se vexan os nomes
                    header = self.table.horizontalHeader()
                    header.setSectionResizeMode(index, QtWidgets.QHeaderView.ResizeToContents)
                    #Seleccionamos o nome do profesor desa columna segundo o lido no ficheiro (ou introducímolo se non está)
                    nome_profesor=f1.readline().strip()
                    #Comprobamos is o profesor está bloqueado
                    bloqueado=False
                    if nome_profesor.endswith("{B}"):
                        bloqueado=True
                        nome_profesor=nome_profesor.replace("{B}","")
                    busca_profe = combo.findText(nome_profesor, QtCore.Qt.MatchFixedString)
                    if busca_profe >= 0:
                        combo.setCurrentIndex(busca_profe)
                    else:
                        #Engadimos o nome do profesor que cargamos nesa posición
                        combo.addItem(nome_profesor)
                        #Seleccionar o novo profesor engadido coma profesor activo
                        combo.setCurrentIndex(combo.findText(nome_profesor,QtCore.Qt.MatchFixedString))
                    #Si estaba bloqueado engadimos o icono
                    if bloqueado:
                        combo.setItemIcon(combo.currentIndex(), QtGui.QIcon("iconos/block.png"))
                    #Interceptamos o sinal de índice cambiado para facer comprobacións cando se seleccione outro profesor
                    combo.currentIndexChanged.connect(lambda state, fila=num_fila, columna=index: self.refrescar_datos_tabla(fila,columna))
                #Intentamos ler outra liña para saber si existen máis grupos
                linea_fichero = f1.readline()
                if linea_fichero:
                    #Si existe grupo engadimos unha nova fila na táboa
                    self.table.insertRow(self.table.rowCount())
                    novo_grupo = QtWidgets.QTableWidgetItem(linea_fichero.strip(os.linesep))
                    # Poñemos o nome do grupo coma só lectura na primeira columna
                    novo_grupo.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table.setItem(self.table.rowCount() - 1, 0, novo_grupo)
                else:
                    #Se non existe terminamos
                    existe_grupo = False
            f1.close()
            #Unha vez cargados os datos actualizamos o diccionario_candidatos
            self.leer_datos_tabla()

    def salvar_datos(self):
        fileName = QFileDialog.getSaveFileName(self, 'Salvar estado do programa', '', "*.xt")
        if fileName[0]:
            if fileName[0].endswith(".xt"):
                nombre_fichero=fileName[0]
            else:
                nombre_fichero=fileName[0]+".xt"
            f1 = open(nombre_fichero, 'w')
            for fila in range(self.table.rowCount()):
                nome_grupo=self.table.item(fila,0).text()
                print(nome_grupo)
                f1.write(nome_grupo + os.linesep)
                for columna in range(1,self.table.columnCount()):
                    combo_candidato = self.table.cellWidget(fila,columna)
                    valor_celda=combo_candidato.currentText()
                    #Comprobamos si ese candidato está bloqueado
                    if combo_candidato.itemIcon(combo_candidato.currentIndex()).isNull():
                        #Si non está bloqueado gardámolo de xeito normal
                        print("\t"+valor_celda)
                        f1.write("\t" + valor_celda + os.linesep)
                    else:
                        #Si está bloqueado gardámolo engadindo {B} ao final do nome
                        print("\t"+valor_celda+"{B}")
                        f1.write("\t" + valor_celda+"{B}" + os.linesep)
            f1.close()

    def engadir_grupo(self):
        nome_grupo, okPressed = QInputDialog.getText(self, "Novo grupo", "Introduza o nome do grupo:", QLineEdit.Normal, "")
        if okPressed and nome_grupo != '':
            self.table.insertRow(self.table.rowCount())
            num_fila=self.table.rowCount()-1
            novo_grupo = QtWidgets.QTableWidgetItem(nome_grupo)
            #Poñermos o nome do grupo soma só lectura
            self.table.setItem(self.table.rowCount()-1, 0, novo_grupo)
            novo_grupo.setFlags(QtCore.Qt.ItemIsEnabled)
            for index in range(1,10):
                #Nas seguintes columnas insertamos un combo co listado de profes (neste caso só nomes en branco)
                #combo = QtWidgets.QComboBox()
                combo=ComboBoxNoWheel()
                #Preparamos o menú contextual dos combo
                combo.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                combo.customContextMenuRequested.connect(partial(self.mostrar_menu_contextual, combo, num_fila, index))
                combo.setEditable(True)
                #Engadimos un primeiro nome baleiro
                combo.addItem("--")
                #Agora engadimos os profes recollidos do ficheiro de profes
                for t in self.listaprofes:
                    combo.addItem(t)
                self.table.setCellWidget(num_fila, index, combo)
                #Interceptamos o sinal de índice cambiado para facer comprobacións cando se seleccione outro profesor
                combo.currentIndexChanged.connect(lambda state, fila=num_fila, columna=index: self.refrescar_datos_tabla(fila,columna))
            #Engadimos un listado de candidatos baleiro para o novo grupo
            self.diccionario_candidatos[nome_grupo]=["--","--","--","--","--","--","--","--","--",]

    def buscar_duplicado(self,fila,valor):
        #Obtemos o nome do grupo a partires da fila
        nome_grupo=self.table.item(fila,0).text()
        #Obtemos o listado actual de candidatos para ese grupo no diccionario
        listado_candidatos=self.diccionario_candidatos[nome_grupo]
        #Buscamos si ese candidato xa existía para ese grupo
        if valor != "--" and valor in listado_candidatos:
            mensaje_titores = "Candidato duplicado.\n" + valor + " xa estaba coma candidato/a para o grupo " + nome_grupo \
                                + "\n¿Queres incluílo igual na lista de candidatos?"
            reply=QMessageBox.question(self, 'Revisar candidato', mensaje_titores)
            if reply == QMessageBox.No:
                #Devolvemos false para indicar que non aceptamos ese candidato
                return False
        #Devolvemos true para indicar que o candidato é aceptado
        return True

    def refrescar_datos_tabla(self,n_fila,n_columna):
        print("Modificado grupo: " + str(n_fila+1) + " Columna: " + str(n_columna))
        nome_profesor= self.table.cellWidget(n_fila,n_columna).currentText()
        print("DATO: " + nome_profesor)
        #Comprobar que el nuevo dato seleccionado no está ya cogido en el grupo
        #Si no lo está recargar el diccionario_candidatos para actualizarlo
        if self.buscar_duplicado(n_fila,nome_profesor):
            #Refrescamos o diccionario de candidatos
            self.leer_datos_tabla()
        else:
            #Candidato non aceptado. Volvemos a poñer -- no combo
            self.table.cellWidget(n_fila,n_columna).setEditText("--")

    def escoller_titores(self,fila):
        if fila==self.tableWidget.rowCount():
            return True
        #Obtemos o nome do grupo a partires da fila
        nome_grupo=self.table.item(fila,0).text()
        #Obtemos o listado actual de candidatos para ese grupo no diccionario
        listado_candidatos=self.diccionario_candidatos[nome_grupo]
        #Escollemos o titor do grupo (imos collendo do primeiro ao último candidato do grupo)
        for candidato in listado_candidatos:
            if candidato != "--":
                #Si o candidato non está xa collido en outro grupo collémoslo para este
                if not candidato in self.listado_titores.values() and not candidato.endswith("{B}"):
                    self.listado_titores[nome_grupo]=candidato
                    #Lanzamos recursivamente a busca do titor do seguinte grupo bloqueando os que xa temos seleccionados
                    buscar_resto_titores=self.escoller_titores(fila+1)
                    #Si ten éxito aceptamos este valor
                    if buscar_resto_titores:
                        return True
                    else:
                        #Si con este tutor non completamos o listado limpámolo
                        self.listado_titores[nome_grupo] = ""
                    #Si non ten éxito probamos co seguinte candidato deste grupo e repetimos
            else:
                #Si non hai titor posible devolvemos false
                return False
        # Si rematamos sin ter titor devolvemos false para indicar que non foi posible atopar titor
        return False

    def xerar_titores(self):
        self.leer_datos_tabla()
        #Recorrer diccionario
        for grupo in self.diccionario_candidatos:
            for candidato in self.diccionario_candidatos[grupo]:
                print ("CANDIDATO de " + str(grupo) + ": " + str(candidato))
        #Inicializamos o listado de titores
        self.listado_titores=collections.OrderedDict()
        if self.escoller_titores(0):
            print("TITORES ATOPADOS: \n")
            print(self.listado_titores)
            #Amosamos os titores atopados e preguntamos si se queren gardar
            mensaje_titores = "Titores atopados. ¿Quere salvar o listado nun ficheiro?"
            #Xeramos o texto co listado de titores para amosalo
            cadena_titores="\n\n"
            for grupo in self.listado_titores:
                cadena_titores += grupo + "\t->\t" + self.listado_titores[grupo] + "\n"
            mensaje_titores += cadena_titores
            reply = QMessageBox.question(self, 'Listado de titores', mensaje_titores, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                informe=xeradorInforme()
                informe.xerar_informe(self.listado_titores)
        else:
            print("Non foi posible atopar titores con eses candidatos")
            QMessageBox.information(self, 'Listado de titores', 'Non foi posible atopar titores con eses candidatos')

    def leer_datos_tabla(self):
        #Leemos los datos de la tabla y la almacenamos en un diccionario
        self.diccionario_candidatos = collections.OrderedDict()
        for fila in range(self.table.rowCount()):
            #La clave será el nombre del grupo
            nome_grupo = self.table.item(fila, 0).text()
            lista_candidatos=[]
            for columna in range(1, self.table.columnCount()):
                # Los valores serán los profesores que pueden ser tutores de ese grupo (en una lista)
                combo_candidato = self.table.cellWidget(fila, columna)
                valor_celda = combo_candidato.currentText()
                # Comprobamos si ese candidato está bloqueado
                if combo_candidato.itemIcon(combo_candidato.currentIndex()).isNull():
                    #Si non o está engadímolo á listaxe de xeito normal
                    lista_candidatos.append(valor_celda)
                else:
                    #Si o está engadimos {B} para logo saltalo ao buscar os titores
                    lista_candidatos.append(valor_celda+"{B}")
            self.diccionario_candidatos[nome_grupo]=lista_candidatos

    def salir(self):
        exit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ventanaXeradorTitorias()
    MainWindow.show()
    sys.exit(app.exec_())