# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(515, 336)
        self.verticalLayout_10 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.select_radio = QtGui.QRadioButton(self.groupBox)
        self.select_radio.setObjectName("select_radio")
        self.horizontalLayout_2.addWidget(self.select_radio)
        self.resolution = QtGui.QComboBox(self.groupBox)
        self.resolution.setObjectName("resolution")
        self.horizontalLayout_2.addWidget(self.resolution)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.custom_radio = QtGui.QRadioButton(self.groupBox)
        self.custom_radio.setObjectName("custom_radio")
        self.horizontalLayout.addWidget(self.custom_radio)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.w_edit = QtGui.QLineEdit(self.groupBox)
        self.w_edit.setObjectName("w_edit")
        self.verticalLayout.addWidget(self.w_edit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.h_edit = QtGui.QLineEdit(self.groupBox)
        self.h_edit.setObjectName("h_edit")
        self.verticalLayout_2.addWidget(self.h_edit)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_6.addWidget(self.groupBox)
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_7.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_8.addWidget(self.label_5)
        self.start_frame = QtGui.QLineEdit(self.groupBox_3)
        self.start_frame.setText("")
        self.start_frame.setObjectName("start_frame")
        self.verticalLayout_8.addWidget(self.start_frame)
        self.horizontalLayout_7.addLayout(self.verticalLayout_8)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_7 = QtGui.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_9.addWidget(self.label_7)
        self.end_frame = QtGui.QLineEdit(self.groupBox_3)
        self.end_frame.setObjectName("end_frame")
        self.verticalLayout_9.addWidget(self.end_frame)
        self.horizontalLayout_7.addLayout(self.verticalLayout_9)
        self.verticalLayout_6.addWidget(self.groupBox_3)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.mov_select = QtGui.QCheckBox(self.groupBox_2)
        self.mov_select.setObjectName("mov_select")
        self.verticalLayout_4.addWidget(self.mov_select)
        self.seq_select = QtGui.QCheckBox(self.groupBox_2)
        self.seq_select.setObjectName("seq_select")
        self.verticalLayout_4.addWidget(self.seq_select)
        self.verticalLayout_6.addWidget(self.groupBox_2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_6)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.note_box = QtGui.QTextEdit(Dialog)
        self.note_box.setObjectName("note_box")
        self.verticalLayout_5.addWidget(self.note_box)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.verticalLayout_10.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.tail_lineedit = QtGui.QLineEdit(Dialog)
        self.tail_lineedit.setObjectName("tail_lineedit")
        self.horizontalLayout_3.addWidget(self.tail_lineedit)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.file_name_label = QtGui.QLabel(Dialog)
        self.file_name_label.setObjectName("file_name_label")
        self.horizontalLayout_4.addWidget(self.file_name_label)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6.addLayout(self.verticalLayout_7)
        self.playblast = QtGui.QPushButton(Dialog)
        self.playblast.setObjectName("playblast")
        self.horizontalLayout_6.addWidget(self.playblast)
        self.verticalLayout_10.addLayout(self.horizontalLayout_6)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Resolution", None, QtGui.QApplication.UnicodeUTF8))
        self.select_radio.setText(QtGui.QApplication.translate("Dialog", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.custom_radio.setText(QtGui.QApplication.translate("Dialog", "Custom", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Width", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Height", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Dialog", "Frame Range", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "End", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Export Type", None, QtGui.QApplication.UnicodeUTF8))
        self.mov_select.setText(QtGui.QApplication.translate("Dialog", "Mov", None, QtGui.QApplication.UnicodeUTF8))
        self.seq_select.setText(QtGui.QApplication.translate("Dialog", "Sequence", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Note", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Tail name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Preview :", None, QtGui.QApplication.UnicodeUTF8))
        self.file_name_label.setText(QtGui.QApplication.translate("Dialog", "File name", None, QtGui.QApplication.UnicodeUTF8))
        self.playblast.setText(QtGui.QApplication.translate("Dialog", "Playblast", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc