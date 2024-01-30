import os, math
import bpy
import numpy as np
import mathutils
import numpy as np
import random

def spherical_to_cartesian(r, theta, phi):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

output_path = "C:\\Users\\Raashid\\Thesis\\Data\\Blender GenData\\withSphereandSun"

bpy.context.preferences.edit.use_global_undo = False

# Set up rendering
context = bpy.context
scene = bpy.context.scene
render = bpy.context.scene.render

# render.engine = "BLENDER_EEVEE"
render.engine = "CYCLES"
scene.cycles.device = 'GPU'
scene.cycles.samples = 64  # Or lower if acceptable
scene.cycles.preview_samples = 32 # or lower

render.image_settings.color_mode = "RGBA"  # ('RGB', 'RGBA', ...)
render.image_settings.color_depth = "8"
render.image_settings.file_format = "PNG"
render.resolution_x = 160
render.resolution_y = 120
render.resolution_percentage = 100
render.film_transparent = True

scene.use_nodes = True
scene.view_layers["ViewLayer"].use_pass_normal = True
scene.view_layers["ViewLayer"].use_pass_z = True
scene.eevee.taa_render_samples = 1  # Disable TAA for sharper images
scene.eevee.use_gtao = True  # Enable global ambient occlusion (GTAO)


nodes = bpy.context.scene.node_tree.nodes
links = bpy.context.scene.node_tree.links

# Clear default nodes
for n in nodes:
    nodes.remove(n)

# Create input render layer node
render_layers = nodes.new("CompositorNodeRLayers")

# Create depth output nodes
depth_file_output = nodes.new(type="CompositorNodeOutputFile")
depth_file_output.label = "Depth Output"
depth_file_output.base_path = ""
depth_file_output.file_slots[0].use_node_format = True
depth_file_output.format.file_format = "OPEN_EXR"
depth_file_output.format.color_depth = "16"
links.new(render_layers.outputs["Depth"], depth_file_output.inputs[0])


# # Create normal output nodes
# scale_node = nodes.new(type="CompositorNodeMixRGB")
# scale_node.blend_type = "MULTIPLY"
# # scale_node.use_alpha = True
# scale_node.inputs[2].default_value = (0.5, 0.5, 0.5, 1)
# links.new(render_layers.outputs["Normal"], scale_node.inputs[1])

# bias_node = nodes.new(type="CompositorNodeMixRGB")
# bias_node.blend_type = "ADD"
# # bias_node.use_alpha = True
# bias_node.inputs[2].default_value = (0.5, 0.5, 0.5, 0)
# links.new(scale_node.outputs[0], bias_node.inputs[1])

# normal_file_output = nodes.new(type="CompositorNodeOutputFile")
# normal_file_output.label = "Normal Output"
# normal_file_output.base_path = ""
# normal_file_output.file_slots[0].use_node_format = True
# normal_file_output.format.file_format = "PNG"
# links.new(bias_node.outputs[0], normal_file_output.inputs[0])

# Create albedo output nodes
# alpha_albedo = nodes.new(type="CompositorNodeSetAlpha")
# links.new(render_layers.outputs["DiffCol"], alpha_albedo.inputs["Image"])
# links.new(render_layers.outputs["Alpha"], alpha_albedo.inputs["Alpha"])

# albedo_file_output = nodes.new(type="CompositorNodeOutputFile")
# albedo_file_output.label = "Albedo Output"
# albedo_file_output.base_path = ""
# albedo_file_output.file_slots[0].use_node_format = True
# albedo_file_output.format.file_format = "PNG"
# albedo_file_output.format.color_mode = "RGB"
# albedo_file_output.format.color_depth = "8"
# links.new(alpha_albedo.outputs["Image"], albedo_file_output.inputs[0])


# Delete default cube
# context.active_object.select_set(True)
bpy.ops.object.delete()


bpy.ops.object.select_all(action="DESELECT")

################ START SCENE LOGIC #################
# Add cube to scene
bpy.ops.mesh.primitive_cube_add(size=0.1)
cube = bpy.context.selected_objects[0]
cube.location = (0.0, 0.0, 0.0)
# Set materials for the cube
cube.data.materials.clear()  # Clear default material
mat_cube = bpy.data.materials.new(name="MaterialCube")
cube.data.materials.append(mat_cube)
mat_cube.use_nodes = True  # Switch to Shader Editor for more advanced materials


# Set plane settings
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -0.05))  # Adjust size and location as needed
plane = bpy.data.objects['Plane']
# Set materials for the plane
plane.data.materials.clear()  # Clear default material
mat_plane = bpy.data.materials.new(name="MaterialPlane")
plane.data.materials.append(mat_plane)
mat_plane.use_nodes = True  # Switch to Shader Editor for more advanced materials

################ END SCENE LOGIC ###################

obj = bpy.context.selected_objects[0]
context.view_layer.objects.active = obj

# Possibly disable specular shading
# for slot in obj.material_slots:
#     node = slot.material.node_tree.nodes["Principled BSDF"]
#     node.inputs["Specular"].default_value = 0.05

# Make light just directional, disable shadows.
# light = bpy.data.lights["Light"]
# light.type = "POINT"
# # light.use_shadow = False
# # Possibly disable specular shading:
# # light.specular_factor = 1.0
# light.energy = 1.0

bpy.ops.object.light_add(type='POINT', location=(1, 0, 0))
light = bpy.data.objects['Point']
light.data.energy = 10.0
light.data.use_shadow = True


# Adding a sun light
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))  # Adjust location as needed
sun_light = bpy.data.objects['Sun']
sun_light.data.energy = 1.0  # Adjust energy as needed
sun_light.data.use_shadow = True

# Add another light source so stuff facing away from light is not completely dark
# bpy.ops.object.light_add(type="SUN")
# light2 = bpy.data.lights["Sun"]
# light2.use_shadow = False
# light2.specular_factor = 1.0
# light2.energy = 0.015
# bpy.data.objects["Sun"].rotation_euler = bpy.data.objects["Light"].rotation_euler
# bpy.data.objects["Sun"].rotation_euler[0] += 180

# Place camera
camera = scene.objects["Camera"]
# camera.location = (0, 10, 5)
camera.location = (0, -1, 0.5)
camera.rotation_euler = (np.radians(90), 0, np.radians(45))
camera.data.lens = 35
camera.data.sensor_width = 32

cam_constraint = camera.constraints.new(type="TRACK_TO")
cam_constraint.track_axis = "TRACK_NEGATIVE_Z"
cam_constraint.up_axis = "UP_Y"

cam_empty = bpy.data.objects.new("Empty", None)
cam_empty.location = (0, 0, 0)
camera.parent = cam_empty

scene.collection.objects.link(cam_empty)
context.view_layer.objects.active = cam_empty
cam_constraint.target = cam_empty

view_count = 5501
# stepsize = 360.0 / view_count
# rotation_mode = "XYZ"
# Set the fixed rotation for a top-front view
fixed_rotation = (np.radians(90), 0, np.radians(45))

model_identifier = "cube"
fp = os.path.join(os.path.abspath(output_path), model_identifier, model_identifier)
min_radius=0.5 #in meters
max_radius=1.0 #in meters

for i in range(5342, view_count):
    # print("Rotation {}, {}".format((stepsize * i), math.radians(stepsize * i)))

    # Set point light in Blender
    light.location = (np.random.uniform(-1, 1), np.random.uniform(-1, 1), np.random.uniform(2, 1))
    light.data.energy = np.random.uniform(0.5, 20)
    light.data.color = (np.random.uniform(0.5, 1.0), 
                    np.random.uniform(0.5, 1.0), 
                    np.random.uniform(0.5, 1.0))


    # Set sun light in Blender
    sun_light.data.energy = np.random.uniform(1, 20)
    sun_light.data.color = (np.random.uniform(0.5, 1.0), 
                    np.random.uniform(0.5, 1.0), 
                    np.random.uniform(0.5, 1.0))
    
    sun_light.rotation_euler[0] = np.random.uniform(-np.pi/2, np.pi/2) #theta
    sun_light.rotation_euler[2] = np.random.uniform(0, 2*np.pi) #phi

    # Randomize camera distance from cube
    camera_distance = np.random.uniform(min_radius, max_radius)

    # Randomize azimuth angle (0 to 360 degrees)
    camera_azimuth = np.radians(np.random.uniform(0, 360))

    # Randomize elevation angle (-45 to 45 degrees)
    # elevation = np.radians(np.random.uniform(-45, 45))

    # More controlled randomization of elevation angle
    elevation_segment = np.random.choice([0, 90])  # Choose among key segments
    elevation_variation = np.random.uniform(-10, 10)  # Add small random variation
    # elevation = np.radians(elevation_segment + elevation_variation)
    camera_elevation = np.radians(np.random.uniform(0,90))

    # Calculate camera position using spherical coordinates
    camera.location.x = cube.location.x + camera_distance * np.sin(camera_elevation) * np.cos(camera_azimuth)
    camera.location.y = cube.location.y + camera_distance * np.sin(camera_elevation) * np.sin(camera_azimuth)
    camera.location.z = cube.location.z + camera_distance * np.cos(camera_elevation)

    # Point the camera towards the cube
    direction = cube.location - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()

    # light.location = (np.random.uniform(-1, 1), np.random.uniform(-1, 1), np.random.uniform(2, 1))
    # camera.location = (np.random.uniform(-0.3, 0.3), -1, np.random.uniform(0.2, 0.7))
    # camera.rotation_euler = (np.radians(90), 0, np.radians(45))

    # render_file_path = fp + "_r_{0:03d}".format(int(i * stepsize))

    # scene.render.filepath = render_file_path
    # depth_file_output.file_slots[0].path = render_file_path + "_depth"
    # normal_file_output.file_slots[0].path = render_file_path + "_normal"
    # albedo_file_output.file_slots[0].path = render_file_path + "_albedo"

    # bpy.ops.render.render(write_still=True)  # render still

    # Render the scene
    # bpy.ops.render.render(write_still=True)

    render_file_path = fp + f"_rgb_{i}"

    scene.render.filepath = render_file_path
    depth_file_output.file_slots[0].path = render_file_path + f"_depth_{i}"
    # normal_file_output.file_slots[0].path = render_file_path + f"_rgb_{i}"

    # Save normal image
    # normal_file_output.file_slots[0].path = f"rgb_{i}.png"
    # # bpy.ops.render.render(write_still=True)

    # # Save Depth image
    # depth_file_output.file_slots[0].path = f"depth_{i}.png"
    bpy.ops.render.render(write_still=True)

    light_x,light_y,light_z = spherical_to_cartesian(1, sun_light.rotation_euler[0], sun_light.rotation_euler[2])
    camera_x, camera_y, camera_z = spherical_to_cartesian(camera_distance, camera_elevation, camera_azimuth)

    with open(os.path.join(output_path, f"location_{i}.txt"), 'w') as f:
            f.write(f"Camera {camera_x} {camera_y} {camera_z}\n")
            f.write(f"Light {light_x} {light_y} {light_z}\n")
            f.write(f"Intensity {sun_light.data.energy}")
    
    bpy.ops.outliner.orphans_purge()
    
    # cam_empty.rotation_euler[2] += math.radians(stepsize)
    # Update camera position and rotation based on the fixed_rotation and stepsize
    # camera.location = (0, -1, 0.5)
    # camera.rotation_euler = fixed_rotation
    # camera.rotation_euler[2] += math.radians(stepsize * (i + 1))

bpy.context.preferences.edit.use_global_undo = True