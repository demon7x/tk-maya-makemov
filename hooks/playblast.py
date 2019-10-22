
import os
import platform
import maya.cmds as cmds

import sgtk
from sgtk.platform.qt import QtGui

HookClass = sgtk.get_hook_baseclass()

if platform.system() == "Linux":

    FFMPEG="/westworld/inhouse/tool/ffmpeg/ffmpeg"
else:
    FFMPEG="//10.0.20.148/inhouse/window_inhouse/tool/ffmpeg/bin/ffmpeg"

class PlayBlast(HookClass):
    """
    Hook called to perform an operation with the
    current scene
    """

    def execute(self, operation,mov_path,mov_file,seq_path,seq_file_name,width,height,note,sframe,eframe,*kwargs):
        

        if operation == "create_seq":

            if not os.path.exists(seq_path):       
                os.makedirs(seq_path)
                os.chmod(seq_path , 0777 )

            image_format = cmds.getAttr("defaultRenderGlobals.imageFormat")
            ratio = cmds.getAttr("defaultResolution.deviceAspectRatio")
            cmds.setAttr("defaultRenderGlobals.imageFormat", 8)

            if not int(width)%2 == 0:
                width = int(width) + 1

            if not int(height)%2 == 0:
                height = int(height) + 1

            cmds.playblast(startTime=str(sframe), endTime=str(eframe), format="image",
                            percent = 100 , qlt = 100,
                            filename=str(os.path.join(seq_path,seq_file_name)), 
                            showOrnaments=False, viewer=False,
                            sequenceTime=False,forceOverwrite=True,
                            widthHeight=[int(width), int(height)],
                            compression="jpg" ,os=1  )

            cmds.setAttr("defaultRenderGlobals.imageFormat", image_format)

        elif operation == "append_slate":
            pass

        elif operation == "create_mov":
            self._create_mov(seq_path,mov_path,mov_file)

        elif operation == "delete_seq":
            pass
        elif operation == "upload_shotgun":
            self._upload_version(mov_path,mov_file,note)


    
    def _create_mov(self,seq_path,mov_path,mov_file):
        import sys
        sys.path.append(self.disk_location)
        import pyseq
        seq_info = pyseq.get_sequences(seq_path)[0]

        command = [FFMPEG]
        command.append("-i")
        command.append( seq_info.format("%D%h%p%t"))
        command.append("-vcodec")
        command.append("libx264")
        command.append("-r")
        command.append("24")
        command.append("-pix_fmt")
        command.append("yuv420p")
        #command.append("-preset")
        #command.append("veryslow")
        command.append("-crf")
        command.append("18")
        command.append("-vf")
        command.append("pad='ceil(iw/2)*2:ceil(ih/2)*2'")
        command.append(os.path.join(mov_path,mov_file))
        cmd = " ".join(command)
        os.system(cmd)


    def _upload_version(self,mov_path,mov_file,note):
        app = self.parent
        sg = app.sgtk.shotgun


        ctx = app.context

        project = ctx.project
        entity = ctx.entity
        task = ctx.task
        user = ctx.user
        
        filters = [
                   ['entity', "is", entity],
                   ['code', "is", mov_file]
                  ]
                    
        
        version = sg.find_one("Version",filters)
        if version:
            sg.upload( 'Version', version['id'],
                        os.path.join(mov_path,mov_file), 'sg_uploaded_movie' )
        else:
            version_data = {
                    "project" : project,
                    "entity" : entity,
                    "sg_task" : task,
                    "code" : mov_file,
                    "user" : user,
                    "description" : note ,
                    "sg_path_to_movie" : os.path.join(mov_path,mov_file)
                    }
            version = sg.create("Version",version_data)
            sg.upload( 'Version', version['id'],
                        os.path.join(mov_path,mov_file), 'sg_uploaded_movie' )



