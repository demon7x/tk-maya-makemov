
import os
import maya.cmds as cmds

import sgtk
from sgtk.platform.qt import QtGui

HookClass = sgtk.get_hook_baseclass()
FFMPEG="/westworld/inhouse/tool/ffmpeg/ffmpeg"

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
            path = os.path.join(seq_path,seq_file_name+".%04d.jpg")
            cmd = ' '.join( [FFMPEG,'-framerate 24', '-start_number 0001', '-y -i',path,
                            '-b:v 100000000k -pix_fmt yuv420p -c:v libx264',
                            os.path.join(mov_path,mov_file)])

            os.system(cmd)

        elif operation == "delete_seq":
            pass
        elif operation == "upload_shotgun":
            self._upload_version(mov_path,mov_file,note)




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



