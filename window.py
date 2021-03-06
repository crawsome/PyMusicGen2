from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(877, 686)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_5)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 841, 81))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.playbutton = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.playbutton.setObjectName("playbutton")
        self.gridLayout_4.addWidget(self.playbutton, 0, 0, 1, 1)
        self.playmeasurebutton = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.playmeasurebutton.setObjectName("playmeasurebutton")
        self.gridLayout_4.addWidget(self.playmeasurebutton, 2, 1, 1, 1)
        self.backbutton = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.backbutton.setObjectName("backbutton")
        self.gridLayout_4.addWidget(self.backbutton, 2, 0, 1, 1)
        self.deletebutton = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.deletebutton.setObjectName("deletebutton")
        self.gridLayout_4.addWidget(self.deletebutton, 0, 3, 1, 1)
        self.insertbutton = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.insertbutton.setObjectName("insertbutton")
        self.gridLayout_4.addWidget(self.insertbutton, 0, 1, 1, 1)
        self.forwardbutton = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.forwardbutton.setObjectName("forwardbutton")
        self.gridLayout_4.addWidget(self.forwardbutton, 2, 3, 1, 1)
        self.gridLayout.addWidget(self.groupBox_5, 6, 0, 1, 5)
        self.groupBox_7 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_7)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 20, 301, 81))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 1, 1, 1)
        self.spinbox_bpmeasure = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.spinbox_bpmeasure.setObjectName("spinbox_bpmeasure")
        self.gridLayout_5.addWidget(self.spinbox_bpmeasure, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 1, 1, 1, 1)
        self.spinbox_bpminute = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.spinbox_bpminute.setObjectName("spinbox_bpminute")
        self.spinbox_bpminute.setMaximum(220)
        self.gridLayout_5.addWidget(self.spinbox_bpminute, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox_7, 1, 3, 1, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.tensionwidget = QtWidgets.QListWidget(self.groupBox_2)
        self.tensionwidget.setGeometry(QtCore.QRect(0, 20, 151, 281))
        self.tensionwidget.setObjectName("tensionwidget")
        item = QtWidgets.QListWidgetItem()
        self.tensionwidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.tensionwidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.tensionwidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.tensionwidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.tensionwidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.tensionwidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.tensionwidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.tensionwidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.tensionwidget.addItem(item)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 3, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 20, 161, 281))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.spinbox_32 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinbox_32.setObjectName("spinbox_32")
        self.gridLayout_2.addWidget(self.spinbox_32, 1, 1, 1, 1)
        self.notebox_32 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.notebox_32.setObjectName("notebox_32")
        self.gridLayout_2.addWidget(self.notebox_32, 1, 0, 1, 1)
        self.notebox_4 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.notebox_4.setObjectName("notebox_4")
        self.gridLayout_2.addWidget(self.notebox_4, 4, 0, 1, 1)
        self.notebox_16 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.notebox_16.setObjectName("notebox_16")
        self.gridLayout_2.addWidget(self.notebox_16, 2, 0, 1, 1)
        self.spinbox_4 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinbox_4.setObjectName("spinbox_4")
        self.gridLayout_2.addWidget(self.spinbox_4, 4, 1, 1, 1)
        self.spinbox_16 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinbox_16.setObjectName("spinbox_16")
        self.gridLayout_2.addWidget(self.spinbox_16, 2, 1, 1, 1)
        self.notebox_2 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.notebox_2.setObjectName("notebox_2")
        self.gridLayout_2.addWidget(self.notebox_2, 5, 0, 1, 1)
        self.spinbox_8 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinbox_8.setObjectName("spinbox_8")
        self.gridLayout_2.addWidget(self.spinbox_8, 3, 1, 1, 1)
        self.spinbox_1 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinbox_1.setObjectName("spinbox_1")
        self.gridLayout_2.addWidget(self.spinbox_1, 6, 1, 1, 1)
        self.notebox_8 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.notebox_8.setObjectName("notebox_8")
        self.gridLayout_2.addWidget(self.notebox_8, 3, 0, 1, 1)
        self.notebox_1 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.notebox_1.setObjectName("notebox_1")
        self.gridLayout_2.addWidget(self.notebox_1, 6, 0, 1, 1)
        self.spinbox_2 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinbox_2.setObjectName("spinbox_2")
        self.gridLayout_2.addWidget(self.spinbox_2, 5, 1, 1, 1)
        self.notebox_chord = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.notebox_chord.setObjectName("notebox_chord")
        self.gridLayout_2.addWidget(self.notebox_chord, 0, 0, 1, 1)
        self.spinbox_chord = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinbox_chord.setObjectName("spinbox_chord")
        self.gridLayout_2.addWidget(self.spinbox_chord, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 2, 3, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.keywidget = QtWidgets.QListWidget(self.groupBox_3)
        self.keywidget.setGeometry(QtCore.QRect(10, 20, 141, 281))
        self.keywidget.setObjectName("keywidget")
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.keywidget.addItem(item)
        self.gridLayout.addWidget(self.groupBox_3, 0, 0, 3, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_4)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 311, 80))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.randomseedbutton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.randomseedbutton.setObjectName("randomseedbutton")
        self.gridLayout_3.addWidget(self.randomseedbutton, 0, 0, 1, 1)
        self.seedtextbox = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.seedtextbox.setObjectName("seedtextbox")
        self.gridLayout_3.addWidget(self.seedtextbox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_4, 0, 3, 1, 2)
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName("groupBox_6")
        self.outputlabel = QtWidgets.QLabel(self.groupBox_6)
        self.outputlabel.setGeometry(QtCore.QRect(10, 20, 841, 161))
        self.outputlabel.setText("")
        self.outputlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.outputlabel.setObjectName("outputlabel")
        self.gridLayout.addWidget(self.groupBox_6, 4, 0, 2, 5)
        self.groupBox_8 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayoutWidget_5 = QtWidgets.QWidget(self.groupBox_8)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(10, 30, 331, 64))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.randomsettingsbutton = QtWidgets.QPushButton(self.gridLayoutWidget_5)
        self.randomsettingsbutton.setObjectName("randomsettingsbutton")
        self.gridLayout_6.addWidget(self.randomsettingsbutton, 0, 3, 1, 1)
        self.resetsettingsbutton = QtWidgets.QPushButton(self.gridLayoutWidget_5)
        self.resetsettingsbutton.setObjectName("resetsettingsbutton")
        self.gridLayout_6.addWidget(self.resetsettingsbutton, 0, 4, 1, 1)
        self.generatebutton = QtWidgets.QPushButton(self.gridLayoutWidget_5)
        self.generatebutton.setObjectName("generatebutton")
        self.gridLayout_6.addWidget(self.generatebutton, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_8, 2, 3, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 877, 22))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuMeasure = QtWidgets.QMenu(self.menubar)
        self.menuMeasure.setObjectName("menuMeasure")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Song = QtWidgets.QAction(MainWindow)
        self.actionNew_Song.setObjectName("actionNew_Song")
        self.actionOpen_Song = QtWidgets.QAction(MainWindow)
        self.actionOpen_Song.setObjectName("actionOpen_Song")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExport_to_MIDI = QtWidgets.QAction(MainWindow)
        self.actionExport_to_MIDI.setObjectName("actionExport_to_MIDI")
        self.actionAdd_new_Measure = QtWidgets.QAction(MainWindow)
        self.actionAdd_new_Measure.setObjectName("actionAdd_new_Measure")
        self.actionDelete_current_measure = QtWidgets.QAction(MainWindow)
        self.actionDelete_current_measure.setObjectName("actionDelete_current_measure")
        self.actionSave_Song = QtWidgets.QAction(MainWindow)
        self.actionSave_Song.setObjectName("actionSave_Song")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuMenu.addAction(self.actionNew_Song)
        self.menuMenu.addAction(self.actionOpen_Song)
        self.menuMenu.addAction(self.actionSave_Song)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionExport_to_MIDI)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuMeasure.addAction(self.actionAdd_new_Measure)
        self.menuMeasure.addSeparator()
        self.menuMeasure.addAction(self.actionDelete_current_measure)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuMeasure.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Controls"))
        self.playbutton.setText(_translate("MainWindow", "Play Song"))
        self.playmeasurebutton.setText(_translate("MainWindow", "Play Measure"))
        self.backbutton.setText(_translate("MainWindow", "<- Back One Measure"))
        self.deletebutton.setText(_translate("MainWindow", "Delete Measure from song"))
        self.insertbutton.setText(_translate("MainWindow", "Insert Measure into song"))
        self.forwardbutton.setText(_translate("MainWindow", "Forward One Measure ->"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Measure Settings"))
        self.label.setText(_translate("MainWindow", "Beats/measure"))
        self.spinbox_bpmeasure.setValue(4)
        self.label_2.setText(_translate("MainWindow", "Beats/minute"))
        self.spinbox_bpminute.setValue(80)
        self.groupBox_2.setTitle(_translate("MainWindow", "Tension"))
        __sortingEnabled = self.tensionwidget.isSortingEnabled()
        self.tensionwidget.setSortingEnabled(False)
        item = self.tensionwidget.item(0)
        item.setText(_translate("MainWindow", "Major"))
        item = self.tensionwidget.item(1)
        item.setText(_translate("MainWindow", "Natural Minor"))
        item = self.tensionwidget.item(2)
        item.setText(_translate("MainWindow", "Harmonic Minor"))
        item = self.tensionwidget.item(3)
        item.setText(_translate("MainWindow", "Melodic Minor"))
        item = self.tensionwidget.item(4)
        item.setText(_translate("MainWindow", "Dorian Mode"))
        item = self.tensionwidget.item(5)
        item.setText(_translate("MainWindow", "Mixolydian Mode"))
        item = self.tensionwidget.item(6)
        item.setText(_translate("MainWindow", "Phrygian"))
        item = self.tensionwidget.item(7)
        item.setText(_translate("MainWindow", "Pentatonic"))
        item = self.tensionwidget.item(8)
        item.setText(_translate("MainWindow", "Minor Pentatonic"))
        self.tensionwidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("MainWindow", "Note Duration Freq."))
        self.notebox_32.setText(_translate("MainWindow", "32nd"))
        self.notebox_4.setText(_translate("MainWindow", "Quarter"))
        self.notebox_16.setText(_translate("MainWindow", "Sixteenth"))
        self.notebox_2.setText(_translate("MainWindow", "Half"))
        self.notebox_8.setText(_translate("MainWindow", "Eighth"))
        self.notebox_1.setText(_translate("MainWindow", "Whole"))
        self.notebox_chord.setText(_translate("MainWindow", "Chord"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Key"))
        __sortingEnabled = self.keywidget.isSortingEnabled()
        self.keywidget.setSortingEnabled(False)
        item = self.keywidget.item(0)
        item.setText(_translate("MainWindow", "C"))
        item = self.keywidget.item(1)
        item.setText(_translate("MainWindow", "C#/Db"))
        item = self.keywidget.item(2)
        item.setText(_translate("MainWindow", "D"))
        item = self.keywidget.item(3)
        item.setText(_translate("MainWindow", "D#/Eb"))
        item = self.keywidget.item(4)
        item.setText(_translate("MainWindow", "E"))
        item = self.keywidget.item(5)
        item.setText(_translate("MainWindow", "F"))
        item = self.keywidget.item(6)
        item.setText(_translate("MainWindow", "F#/Gb"))
        item = self.keywidget.item(7)
        item.setText(_translate("MainWindow", "G"))
        item = self.keywidget.item(8)
        item.setText(_translate("MainWindow", "G#/Ab"))
        item = self.keywidget.item(9)
        item.setText(_translate("MainWindow", "A"))
        item = self.keywidget.item(10)
        item.setText(_translate("MainWindow", "A#/Bb"))
        item = self.keywidget.item(11)
        item.setText(_translate("MainWindow", "B"))
        self.keywidget.setSortingEnabled(__sortingEnabled)
        self.groupBox_4.setTitle(_translate("MainWindow", "Seed (For RNG)"))
        self.randomseedbutton.setText(_translate("MainWindow", "Random Seed"))
        self.seedtextbox.setText(_translate("MainWindow", "555"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Output Area"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Generate / Randomize / Reset"))
        self.randomsettingsbutton.setText(_translate("MainWindow", "Randomize"))
        self.resetsettingsbutton.setText(_translate("MainWindow", "Reset Selection"))
        self.generatebutton.setText(_translate("MainWindow", "Generate!"))
        self.menuMenu.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuMeasure.setTitle(_translate("MainWindow", "Measure"))
        self.actionNew_Song.setText(_translate("MainWindow", "New Song..."))
        self.actionOpen_Song.setText(_translate("MainWindow", "Open Song..."))
        self.actionAbout.setText(_translate("MainWindow", "About..."))
        self.actionExport_to_MIDI.setText(_translate("MainWindow", "Export..."))
        self.actionAdd_new_Measure.setText(_translate("MainWindow", "Add new Measure"))
        self.actionDelete_current_measure.setText(_translate("MainWindow", "Delete current measure"))
        self.actionSave_Song.setText(_translate("MainWindow", "Save Song..."))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
