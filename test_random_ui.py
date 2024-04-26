import sys
import maya.cmds as cmds
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import random
import os
import importlib

class Windowui(QMainWindow):
    """
        Class UI for show window in MAYA 
    """
    def __init__(self, *args, **kwargs):
        """
            Create main window UI and link with class function MinandMaxValues.
                *args = get non keyword arguments
                **kwargs = get keyword arguments 
            Return 
                show all label, min and max values from rotation and scale to set values 0 or 1.
        """
        super(Windowui, self).__init__(*args, **kwargs)
        self.resize(450, 150)
        self.setWindowTitle('TEST RANDOM')

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.getVertex()
        self.main_layout.addWidget(self.getVertex_widget)
        
        self.snap_label = QLabel('Snap with vertex:')
        self.snap_input = QLineEdit()

        self.main_layout.addWidget(self.snap_label)
        self.main_layout.addWidget(self.snap_input)
        
        self.rotatex_label = QLabel('Rotate X:')
        self.rotatey_label = QLabel('Rotate Y:')
        self.rotatez_label = QLabel('Rotate Z:')
        self.scalex_label = QLabel('Scale X:')
        self.scaley_label = QLabel('Scale Y:')
        self.scalez_label = QLabel('Scale Z:')

        self.create_button = QPushButton('Generate')
        self.create_button.setMinimumHeight(50)

        self.main_layout.addWidget(self.rotatex_label)
        self.rotatex_main_initDisplay_min = MinandMaxValues(value_type='Min', minValueRange=0, initvalue=0)
        self.rotatex_main_initDisplay_max = MinandMaxValues(value_type='Max', minValueRange=0, initvalue=0)
        self.main_layout.addWidget(self.rotatex_main_initDisplay_min)
        self.main_layout.addWidget(self.rotatex_main_initDisplay_max)
        
        self.main_layout.addWidget(self.rotatey_label)
        self.rotatey_main_initDisplay_min = MinandMaxValues(value_type='Min', minValueRange=0, initvalue=0)
        self.rotatey_main_initDisplay_max = MinandMaxValues(value_type='Max', minValueRange=0, initvalue=0)
        self.main_layout.addWidget(self.rotatey_main_initDisplay_min)
        self.main_layout.addWidget(self.rotatey_main_initDisplay_max)
        
        self.main_layout.addWidget(self.rotatez_label)
        self.rotatez_main_initDisplay_min = MinandMaxValues(value_type='Min', minValueRange=0, initvalue=0)
        self.rotatez_main_initDisplay_max = MinandMaxValues(value_type='Max', minValueRange=0, initvalue=0)
        self.main_layout.addWidget(self.rotatez_main_initDisplay_min)
        self.main_layout.addWidget(self.rotatez_main_initDisplay_max)
        
        self.main_layout.addWidget(self.scalex_label)
        self.scalex_main_initDisplay_min = MinandMaxValues(value_type='Min', minValueRange=0, initvalue=1)
        self.scalex_main_initDisplay_max = MinandMaxValues(value_type='Max', minValueRange=0, initvalue=1)
        self.main_layout.addWidget(self.scalex_main_initDisplay_min)
        self.main_layout.addWidget(self.scalex_main_initDisplay_max)
        
        self.main_layout.addWidget(self.scaley_label)
        self.scaley_main_initDisplay_min = MinandMaxValues(value_type='Min', minValueRange=0, initvalue=1)
        self.scaley_main_initDisplay_max = MinandMaxValues(value_type='Max', minValueRange=0, initvalue=1)
        self.main_layout.addWidget(self.scaley_main_initDisplay_min)
        self.main_layout.addWidget(self.scaley_main_initDisplay_max)
        
        self.main_layout.addWidget(self.scalez_label)
        self.scalez_main_initDisplay_min = MinandMaxValues(value_type='Min', minValueRange=0, initvalue=1)
        self.scalez_main_initDisplay_max = MinandMaxValues(value_type='Max', minValueRange=0, initvalue=1)
        self.main_layout.addWidget(self.scalez_main_initDisplay_min)
        self.main_layout.addWidget(self.scalez_main_initDisplay_max)

        self.main_layout.addWidget(self.create_button)

        self.create_button.clicked.connect(self.generate_objects)

    def getVertex(self):
        """
            Create get button and label Name object for output object
            Return
                the name of object and button get.
        """
        self.getVertex_widget = QWidget()
        self.getVertex_layout = QHBoxLayout()
        self.getVertex_widget.setLayout(self.getVertex_layout)

        self.getVertex_label = QLabel('Name Object: ')
        self.getVertex_lineEdit = QLineEdit()
        self.getVertex_button = QPushButton('Get')

        self.getVertex_button.clicked.connect(self.getbutton_object)

        self.getVertex_layout.addWidget(self.getVertex_label)
        self.getVertex_layout.addWidget(self.getVertex_lineEdit)
        self.getVertex_layout.addWidget(self.getVertex_button)

    def generate_objects(self, *args):
        """
            Return value rotation and scale X Y Z to spinbox and input name to build, return trn = terrain to LineEidt.
                link placement with class ObjectPlacementOnTerrain for show min and max values.
                Return
                    values of min and max to spinbox and slider from ratation XYZ also scale XYZ. then create name object.
        """
        # Retrieve rotation values from spin boxes
        minrotation_values = [
            self.rotatex_main_initDisplay_min.minandmaxValues_spinbox.value(),
            self.rotatey_main_initDisplay_min.minandmaxValues_spinbox.value(),
            self.rotatez_main_initDisplay_min.minandmaxValues_spinbox.value()
        ]
        maxrotation_values = [
            self.rotatex_main_initDisplay_max.minandmaxValues_spinbox.value(),
            self.rotatey_main_initDisplay_max.minandmaxValues_spinbox.value(),
            self.rotatez_main_initDisplay_max.minandmaxValues_spinbox.value()
        ]

        # Retrieve scale values from spin boxes
        scale_min_values = [
            self.scalex_main_initDisplay_min.minandmaxValues_spinbox.value(),
            self.scaley_main_initDisplay_min.minandmaxValues_spinbox.value(),
            self.scalez_main_initDisplay_min.minandmaxValues_spinbox.value()
        ]
        scale_max_values = [
            self.scalex_main_initDisplay_max.minandmaxValues_spinbox.value(),
            self.scaley_main_initDisplay_max.minandmaxValues_spinbox.value(),
            self.scalez_main_initDisplay_max.minandmaxValues_spinbox.value()
        ]
        
        # Retrieve snap value from line edit
        snap_value = int(self.snap_input.text()) if self.snap_input.text() else None

        # Retrieve vertex and terrain information
        name = 'build'
        trn = self.getVertex_lineEdit.text()

        # Create an instance of ObjectPlacementOnTerrain and place objects
        placement = ObjectPlacementOnTerrain(name, trn)
        placement.place_objects(minrotation_values, maxrotation_values, scale_min_values, scale_max_values, snap_value)

    def getbutton_object(self, *args):
        """
            Select the object and show name object
            Return
                return name of object from the selected.
        """
        sel = cmds.ls(sl=True)[0]
        self.getVertex_lineEdit.setText(sel)
        

class MinandMaxValues(QWidget):
    """
        Create for min and max values for controle rotation and scale
    """
    def __init__(self, value_type='min/max', minValueRange=0.0, initvalue=0.0):
        """
            For this function to create layout, spinbox, slider min and max.
                connect values spinbox and slider.

            value_type = 'min/max' are set type of value
            minValueRange=0.0 is the minimum value range for the value being initialized.
            initvalue=0.0 is represents the initial value to be set. If no value is provided, 0.0 will be used.

            Return
                connected min and max values spinbox and slider.
        """
        super(MinandMaxValues, self).__init__()

        self.minandmaxType = value_type
        self.initvalue = initvalue 

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.minandmaxValues_widget = QWidget()
        self.minandmaxValues_layout = QHBoxLayout()
        self.minandmaxValues_widget.setLayout(self.minandmaxValues_layout)

        self.minandmaxValues_type_label = QLabel(self.minandmaxType)
        self.minandmaxValues_spinbox = QSpinBox()
        self.minandmaxValues_spinbox.setRange(-100,360)
        
        self.minandmaxValues_slider = QSlider(Qt.Horizontal)
        self.minandmaxValues_slider.setRange(-100,360)
        
        self.minandmaxValues_spinbox.setValue(self.initvalue)
        self.minandmaxValues_slider.setValue(self.initvalue)
        
        self.main_layout.addWidget(self.minandmaxValues_type_label)
        self.main_layout.addWidget(self.minandmaxValues_spinbox)
        self.main_layout.addWidget(self.minandmaxValues_slider)
        
        self.minandmaxValues_spinbox.valueChanged.connect(self.minandmaxValues_slider.setValue)
        self.minandmaxValues_slider.valueChanged.connect(self.minandmaxValues_spinbox.setValue)

def run():
    """
        For run all of them and show output.
    """
    global ui
    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QWidget)
    ui = Windowui(parent=ptr)
    ui.show()

run()