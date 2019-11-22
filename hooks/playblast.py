
import os
import platform
import maya.cmds as cmds

import sgtk
from sgtk.platform.qt import QtGui

HookClass = sgtk.get_hook_baseclass()

if platform.system() == "Linux":

    FFMPEG="/westworld/inhouse/tool/ffmpeg/ffmpeg"
else:
    FFMPEG="\\\\10.0.40.42\\inhouse\\window_inhouse\\tool\\ffmpeg\\bin\\ffmpeg"

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
        

        elif operation == "create_turntable":
            turn_table = self._create_turntable()
            return turn_table    

        elif operation == "append_slate":
            pass

        elif operation == "create_mov":
            self._create_mov(seq_path,mov_path,mov_file)

        elif operation == "delete_seq":
            pass
        elif operation == "upload_shotgun":
            self._upload_version(mov_path,mov_file,note)

    
    def _create_turntable(self):
        
        sel = cmds.ls(sl=1)
	bBox = cmds.exactWorldBoundingBox(sel)
	v1 = [bBox[0], bBox[1], bBox[2]]
	v2 = [bBox[3], bBox[4], bBox[5]]
	v3 = [v2[0]- v1[0], v2[1]-v1[1], v2[2]-v1[2]]
        height = (bBox[4] - bBox[1])/2.0
        radius = bBox[3] * 0.8 * 7
        if not platform.system() == "Linux":
            radius = bBox[3] * 0.9 * 8

        #if radius < bBox[4]:
        #    radius = bBox[4] * 2.4 

        #if radius < (bBox[5] *3):
        #    radius = bBox[5] * 3 
        #print radius
	circle = cmds.circle(radius = radius, sections = 50)
	cmds.setAttr(circle[0] + '.rotateX', 90)
        cmds.setAttr(circle[0] + '.translateY', height)
        cmds.setAttr(circle[0] + '.visibility', 0)
	cmds.reverseCurve(circle[0])

	turnCamera = cmds.camera()
	cameraShape = turnCamera[1]
        focal_length = bBox
	cmds.camera(cameraShape, edit = True, focalLength = 50)
	cmds.camera(cameraShape, edit = True, fStop = 5.6)
	#cmds.setAttr(cameraShape + '.aiApertureSize', ((50.0/5.6)/2)/10)
	#cmds.setAttr(cameraShape + '.aiApertureSize', 20)

	direction = 'Clockwise'
	direction_value = 1
	animationLength = 120
	cmds.pathAnimation(turnCamera[0], circle[0], fractionMode = True, follow = True, followAxis = 'x', upAxis = 'y', 
	worldUpType = 'vector', worldUpVector = [0, 1, 0], inverseUp = False, inverseFront = False, bank = False,
	startTimeU = 1, endTimeU = animationLength)

	con = cmds.listConnections(turnCamera)
	motionpath = con[6]
	cmds.keyframe(motionpath, edit = True, time=(0, 1), valueChange = 1)
	cmds.keyframe(motionpath, edit = True, time=(animationLength - 1, animationLength), valueChange = 0)
	cmds.keyTangent(motionpath, inTangentType = 'linear', outTangentType = 'linear', time = (0, animationLength + 1))

        
	cmds.select(circle)
	cmds.select(turnCamera, add = True)
	turntableContainer = cmds.group()
    
        cmds.lookThru(turnCamera)
        self._create_slider_window(turnCamera,circle)
        
        return turntableContainer
        
    def _create_slider_window(self,camera,circle):
        window = cmds.window(title="Control TurnTable View",iconName="CTV",widthHeight=(250,100))
        cmds.columnLayout( adjustableColumn=True )
        cmds.text(label='Tilt', align='left')
        cmds.floatSlider("tilt",min=-10.0,max=10.0,value=cmds.getAttr(camera[0]+".rotateX"))
        cmds.connectControl( "tilt", "%s.rotateX"%camera[0] )
        cmds.text(label='Zoom', align='left')
        circle_size = cmds.getAttr(circle[1]+".radius")
        cmds.floatSlider("zoom",min=circle_size/2 ,max=circle_size*2,value=cmds.getAttr(circle[1]+".radius"))
        cmds.connectControl( "zoom", "%s.radius"%circle[1] )
        cmds.setParent( '..' )
        cmds.showWindow( window )

    
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
        print cmd
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



