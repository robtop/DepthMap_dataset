import bpy
from bpy import context
from math import sin, cos, radians
import random as rand
import time
#Output resolution (Stereoscopic images & depthmap)
bpy.context.scene.render.resolution_x = 150
bpy.context.scene.render.resolution_y = 100

# Total number of set of stereoscopic images and depth maps
total_scene_number = 100

###################################
#Start iteration to generate scenes
###################################

def CreateCube(CubeName, MatName):
    bpy.ops.mesh.primitive_cube_add(location=((0.3-rand.random())*magn, (0.3-rand.random())*magn, (0.3-rand.random())*magn))
    bpy.ops.transform.rotate(value=rand.random()*3.14, axis=(rand.random(), rand.random(), rand.random()), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.material.new()
    mat1 = bpy.data.materials[MatName]
    mat1.diffuse_color = (rand.random(), rand.random(), rand.random())

    bpy.data.objects[CubeName].data.materials.append(mat1)
    
def CreateCone(ConeName, MatName):
    bpy.ops.mesh.primitive_cone_add(location=((0.5-rand.random())*magn, (0.4-rand.random())*magn, (0.6-rand.random())*magn))
    bpy.ops.transform.rotate(value=rand.random()*3.14, axis=(rand.random(), rand.random(), rand.random()), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.material.new()
    mat1 = bpy.data.materials[MatName]
    mat1.diffuse_color = (rand.random(), rand.random(), rand.random())

    bpy.data.objects[ConeName].data.materials.append(mat1)
    
def CreateTorus(TorusName, MatName):
    bpy.ops.mesh.primitive_torus_add(location=((0.35-rand.random())*magn, (0.55-rand.random())*magn, (0.45-rand.random())*magn))
    bpy.ops.transform.rotate(value=rand.random()*3.14, axis=(rand.random(), rand.random(), rand.random()), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.material.new()
    mat1 = bpy.data.materials[MatName]
    mat1.diffuse_color = (rand.random(), rand.random(), rand.random())

    bpy.data.objects[TorusName].data.materials.append(mat1)
    
def CreateSphere(SphereName, MatName):
    bpy.ops.mesh.primitive_uv_sphere_add(location=((0.5-rand.random())*magn, (0.5-rand.random())*magn, (0.5-rand.random())*magn))
    bpy.ops.transform.rotate(value=rand.random()*3.14, axis=(rand.random(), rand.random(), rand.random()), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.material.new()
    mat1 = bpy.data.materials[MatName]
    mat1.diffuse_color = (rand.random(), rand.random(), rand.random())

    bpy.data.objects[SphereName].data.materials.append(mat1)
    

ii = 0

while ii < total_scene_number:
    
    ii += 1
    #Clear data from previous scenes
    for material in bpy.data.materials:
        material.user_clear();
        bpy.data.materials.remove(material);
    
    for texture in bpy.data.textures:
        texture.user_clear();
        bpy.data.textures.remove(texture);

    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links
 
    # clear default nodes
    for n in tree.nodes:
        tree.nodes.remove(n)
    
    #setup lighting:
    light = bpy.data.objects['Lamp']
    #light.data.shadow_method = 'RAY_SHADOW'
    light.data.energy = 5.0
    light.select = False

    #setup camera:
    camera = bpy.data.objects['Camera']
    camera.select = True
    camera.rotation_mode = 'XYZ'
    angle1 = 1.3 + (0.5-rand.random())*1.5
    angle2 = (0.5-rand.random())*1.5
    angle3 = 0.75 + (0.5-rand.random())*1.5
    camera.rotation_euler = (angle1, angle2, angle3)
    Cam_x = 10 +(0.5-rand.random())*3
    Cam_y = -3 + (0.5-rand.random())*3
    Cam_z = 3 + (0.5-rand.random())*3
    camera.location = (Cam_x,Cam_y,Cam_z)
    camera.data.stereo.convergence_distance = 10000
    camera.data.lens = 15 #(focal length)
    camera.data.stereo.interocular_distance = 0.3
    dist = ((camera.location[0]-(-3.22))**(2)+(camera.location[1]-(8.0))**(2)+(camera.location[2]-(-5.425))**(2))**(1/2)
    camera.select = False
    
    #Remove objects from previsous scenes
    for item in bpy.data.objects:  
        if item.type == "MESH":  
            bpy.data.objects[item.name].select = True
            bpy.ops.object.delete()
        
    for item in bpy.data.meshes:
      bpy.data.meshes.remove(item)
  
    ##################
    #Create new scene:
    ##################

    scene = bpy.context.scene
    scene.render.use_multiview = True
    scene.render.views_format = 'STEREO_3D'
    rl = tree.nodes.new(type="CompositorNodeRLayers")
    composite = tree.nodes.new(type = "CompositorNodeComposite")
    composite.location = 200,0

    scene = bpy.context.scene

    #setup the depthmap calculation using blender's mist function:
    scene.render.layers['RenderLayer'].use_pass_mist = True
    #the depthmap can be calculated as the distance between objects and camera ('LINEAR'), or square/inverse square of the distance ('QUADRATIC'/'INVERSEQUADRATIC'):
    scene.world.mist_settings.falloff = 'LINEAR'
    #minimum depth:
    scene.world.mist_settings.intensity = 0.0
    #maximum depth (can be changed depending on the scene geometry to normalize the depth map whatever the camera orientation and position is):
    scene.world.mist_settings.depth = dist
    print(dist)

    #magnitude of the random variation of object placements:
    magn = 10;

    #create objects with random location, orientation and color
    
    
    CreateCube('Cube','Material')
    
    CreateCube('Cube.001','Material.001')
    
    CreateCone('Cone','Material.002')
    
    CreateTorus('Torus','Material.003')
    
    CreateSphere('Sphere','Material.004')
    
    #create walls

    bpy.ops.mesh.primitive_plane_add(radius=1, enter_editmode=False, location=(7, 8, -1), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    bpy.ops.transform.resize(value=(30, 30, 30), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    
    bpy.ops.mesh.primitive_plane_add(radius=1, enter_editmode=False, location=(-3, -2, -1), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.transform.rotate(value=3.14, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    bpy.ops.transform.resize(value=(30, 30, 30), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    bpy.ops.mesh.primitive_plane_add(location=(3.5, 0, -5), rotation=(0, 0, 0))
    bpy.ops.transform.resize(value=(30, 30, 30), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)


    bpy.ops.mesh.primitive_plane_add(location=(3.5, 0, 9), rotation=(0, 0, 0))
    bpy.ops.transform.resize(value=(30, 30, 30), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    bpy.ops.material.new()
    mat3 = bpy.data.materials['Material.005']
    bpy.ops.texture.new()
    texture1 = bpy.data.textures["Texture"].type = 'VORONOI'
    bpy.data.textures["Texture"].noise_scale = 0.02
    
    bpy.data.objects['Plane'].data.materials.append(mat3)
    bpy.data.objects['Plane.001'].data.materials.append(mat3)
    bpy.data.objects['Plane.002'].data.materials.append(mat3)
    bpy.data.objects['Plane.003'].data.materials.append(mat3)
    #################
    #Render the scene
    #################

    #ouput the depthmap:
    links.new(rl.outputs['Mist'],composite.inputs['Image'])

    scene.render.use_multiview = False

    scene.render.filepath = 'Depth_map/DepthMap_'+str(ii)+'.png'
    bpy.ops.render.render( write_still=True ) 
    #time.sleep(0.2)
    #output the stereoscopic images:
    links.new(rl.outputs['Image'],composite.inputs['Image'])

    scene.render.use_multiview = True

    scene.render.filepath = 'StereoImages/Stereoscopic_'+str(ii)+'.png'
    bpy.ops.render.render( write_still=True ) 
    #time.sleep(0.2)
