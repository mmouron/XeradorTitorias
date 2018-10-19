import os
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

class xeradorInforme(QtWidgets.QMainWindow):

    def xerar_informe(self, dic_titores):
        doc = QtGui.QTextDocument()
        #Creamos un cursos no inicio do documento
        cursor = QtGui.QTextCursor(doc)
        #Insertamos a primeira liña de texto
        cursor.insertText('Listado de titores\n')
        num_grupos=len(dic_titores)
        #Creamos unha táboa e insertamos os titores nela
        cursor.insertTable(num_grupos, 2)
        for grupo in dic_titores:
            cursor.insertText(grupo)
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(dic_titores[grupo])
            cursor.movePosition(QtGui.QTextCursor.NextCell)
        #Creamos un writer para salvar o documento
        writer = QtGui.QTextDocumentWriter()
        #writer.supportedDocumentFormats()
        #[PyQt4.QtCore.QByteArray(b'HTML'), PyQt4.QtCore.QByteArray(b'ODF'), PyQt4.QtCore.QByteArray(b'plaintext')]
        odf_format = writer.supportedDocumentFormats()[1]
        writer.setFormat(odf_format)
        fileName = QFileDialog.getSaveFileName(self, 'Salvar listado de titores', '', "*.odt")
        if fileName[0]:
            if fileName[0].endswith(".odt"):
                nombre_fichero=fileName[0]
            else:
                nombre_fichero=fileName[0]+".odt"
            writer.setFileName(nombre_fichero)
            writer.write(doc) # Devolve True si foi correcto