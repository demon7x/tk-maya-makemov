# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import os
import sys
import threading
from datetime import datetime


from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog
from sgtk import TankError
import pymel.core as pm
import maya.cmds as cmds

task_manager = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "task_manager")

BackgroundTaskManager = task_manager.BackgroundTaskManager

shotgun_globals = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_globals")

spinner_widget = sgtk.platform.import_framework(
    "tk-framework-qtwidgets", "spinner_widget")

TIMESTAMP_FMT = "%Y-%m-%d-%H-%M-%S"

PRESET=[
"1024 x 768",
"1280 x 720",
"1920 x 1080",
"2048 x 872",
"2048 x 1080",
"2048 x 1152",


]

FILETYPE=[
"jpg",
"png",
"tif",
"tga"

]


def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system. 
    
    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Make Mov For Maya", app_instance, AppDialog)
    


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """
    
    def __init__(self):
        """
        Constructor
        """
        QtGui.QWidget.__init__(self)
        
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        
        self._app = sgtk.platform.current_bundle()
        self._preview_task = None

        #init_ui


        self.ui.resolution.addItems(PRESET)
        self.ui.select_radio.click()
        self._set_frame()
        
        self._spinner = spinner_widget.SpinnerWidget(self)
        self._spinner.hide()

        font_colour = self.palette().text().color()
        if font_colour.value() < 0.5:
            preview_colour = font_colour.lighter(140)
        else:
            preview_colour = font_colour.darker(140)
        self._preview_colour = (preview_colour.red(), preview_colour.green(), preview_colour.blue())


        self._bg_task_manager = BackgroundTaskManager(self, max_threads=8)

        if self._preview_task:
            self._bg_task_manager.stop_task(self._preview_task)
            self._preview_task = None
            
        shotgun_globals.register_bg_task_manager(self._bg_task_manager)
        self._bg_task_manager.task_completed.connect(self._on_preview_generation_complete)
        self._bg_task_manager.task_failed.connect(self._on_preview_generation_failed)
        self._bg_task_manager.start_processing()


        self._preview_task = self._bg_task_manager.add_task(self._generate_path,
                                                            priority = 35,
                                                            task_kwargs = {
                                                                           "require_path":False})
        
        self.ui.tail_lineedit.textChanged.connect(self._edit_tail)
        self.ui.playblast.clicked.connect(self._on_playblast)
        self.ui.create_turntable.clicked.connect(self._create_turntable)
    
    def _create_turntable(self):

        turn_group = self._app.execute_hook("hook_playblast",
                                operation="create_turntable",
                                mov_path = "",
                                mov_file="",
                                seq_path="",
                                seq_file_name="",
                                width="",height="",
                                note="",
                                sframe="",eframe="")

        if self.ui.turn_default.isChecked():
            print "Default"
        if self.ui.turn_occlusion.isChecked():
            print "occ"
            cmds.setAttr("hardwareRenderingGlobals.ssaoEnable",True)
            cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable",True)

        if self.ui.turn_wire.isChecked():
            for mp in cmds.getPanel(type="modelPanel"):
                if cmds.modelEditor(mp, q=1, av=1):
                    cmds.modelEditor( mp, edit = True, wireframeOnShaded = True)

            print "wire"

        self.turn_group = turn_group
        
    
    def _delete_turn_set(self):

        
        cmds.lookThru('persp')
        cmds.setAttr("hardwareRenderingGlobals.ssaoEnable",False)
        cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable",False)

        for mp in cmds.getPanel(type="modelPanel"):
            if cmds.modelEditor(mp, q=1, av=1):
                cmds.modelEditor( mp, edit = True, wireframeOnShaded = False)
        
        cmds.delete(self.turn_group)

    def _on_playblast(self):
        
        if self.ui.turn_table_status.isChecked():
            self._create_turntable()

        self._spinner.show()

        mov_path, mov_file = os.path.split(self._path)
        seq_dir = mov_file.rsplit(".",1)[0]
        seq_path = os.path.join(mov_path,seq_dir)
        seq_file_name = mov_file.rsplit(".",1)[0]
        note = ""

        if self.ui.select_radio.isChecked():
            width,height = self.ui.resolution.currentText().split("x")
        else:
            if not self.ui.w_edit.text() or not self.ui.h_edit.text():
                return
            width = self.ui.w_edit.text()
            height = self.ui.h_edit.text()
        
        sframe = self.ui.start_frame.text()
        eframe = self.ui.end_frame.text()

 
        
        self._app.execute_hook("hook_playblast",
                                operation="create_seq",
                                mov_path = mov_path,
                                mov_file=mov_file,
                                seq_path=seq_path,
                                seq_file_name=seq_file_name,
                                width=width,height=height,
                                note=note,
                                sframe=sframe,eframe=eframe)
        
        self._app.execute_hook("hook_playblast",
                                operation="create_mov",
                                mov_path = mov_path,
                                mov_file=mov_file,
                                seq_path=seq_path,
                                seq_file_name=seq_file_name,
                                width=width,height=height,
                                note=note,
                                sframe=sframe,eframe=eframe)

        #self._app.execute_hook("hook_playblast",
        #                        operation="upload_shotgun",
        #                        mov_path = mov_path,
        #                        mov_file=mov_file,
        #                        seq_path=seq_path,
        #                        seq_file_name=seq_file_name,
        #                        width=width,height=height,
        #                        note=note,
        #                        sframe=sframe,eframe=eframe)

        if self.ui.turn_table_status.isChecked():
            self._delete_turn_set()
        self._spinner.hide()

    def _set_frame(self):

        sframe = cmds.playbackOptions(q=1 , min=1)
        eframe = cmds.playbackOptions(q=1 , max=1)

        self.ui.start_frame.setText(str(sframe))
        self.ui.end_frame.setText(str(eframe))

    def _edit_tail(self):
        
        self._preview_task = self._bg_task_manager.add_task(self._generate_path,
                                                            priority = 35,
                                                            task_kwargs = {
                                                                           "require_path":False})


    def _on_preview_generation_failed(self, task_id, group, msg, stack_trace):
        """
        """
        if task_id != self._preview_task:
            return
        self._preview_task = None
        
        print "fail"
        print msg

    def _on_preview_generation_complete(self, task_id, group, result):
        

        if task_id != self._preview_task:
            return
        self._preview_task = None

        name_preview = ""
        path_preview = ""
        self._path = result.get("path")
        

        path_preview, name_preview = os.path.split(self._path)

        self.ui.file_name_label.setText("<p style='color:rgb%s'>%s</p>" 
                                           % (self._preview_colour, name_preview))

    def _generate_path(self,require_path=False):
        """
        :returns:   Tuple containing (path, min_version)
        :raises:    Error if something goes wrong!

        """
        
        scene_file = pm.sceneName()
        app = sgtk.platform.current_bundle()
        ctx = app.engine.context
        tk = app.engine.tank
        
        if ctx.entity['type'] == "Shot":
            scene_file_temp = tk.templates["maya_shot_work"]
            mov_temp = tk.templates['maya_shot_mov']
            fields = scene_file_temp.get_fields(scene_file)
        else:
            scene_file_temp = tk.templates["maya_asset_work"]
            mov_temp = tk.templates['maya_asset_mov']
            fields = scene_file_temp.get_fields(scene_file)

        #fields["timestamp"] = datetime.now().strftime(TIMESTAMP_FMT)
        if self.ui.tail_lineedit.text():
            fields['name'] = self.ui.tail_lineedit.text()
        path = mov_temp.apply_fields(fields)

        return {'path':path}

