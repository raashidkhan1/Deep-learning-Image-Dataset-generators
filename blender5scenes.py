import os
import bpy
import numpy as np

# Set the path to save the generated dataset
output_path = "C:\\Users\\Raashid\\Thesis\\SyntheticData"
os.makedirs(output_path, exist_ok=True)

# Set the number of samples you want to generate for each scene
num_samples_per_scene = 10

# List of 3D objects (cube, cylinder, cone, sphere, pyramid)
objects = ["Cube"]

# Set Blender scene settings
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Set Blender rendering settings
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'
bpy.context.scene.render.resolution_x = 160
bpy.context.scene.render.resolution_y = 120
bpy.context.scene.render.resolution_percentage = 100  # Adjust as needed
bpy.context.scene.use_nodes = True
bpy.context.scene.view_layers["ViewLayer"].use_pass_normal = True
bpy.context.scene.view_layers["ViewLayer"].use_pass_z = True
tree = bpy.context.scene.node_tree

# Clear default nodes
for node in tree.nodes:
    tree.nodes.remove(node)

# Create nodes for RGB output
render_layers_node_rgb = tree.nodes.new(type='CompositorNodeRLayers')
output_node_rgb = tree.nodes.new(type='CompositorNodeOutputFile')
output_node_rgb.format.file_format = 'PNG'
output_node_rgb.base_path = output_path
output_node_rgb.file_slots.new("Image")

# Link nodes for RGB output
tree.links.new(render_layers_node_rgb.outputs["Image"], output_node_rgb.inputs["Image"])

# Create nodes for Depth output
render_layers_node_depth = tree.nodes.new(type='CompositorNodeRLayers')
output_node_depth = tree.nodes.new(type='CompositorNodeOutputFile')
output_node_depth.format.file_format = 'OPEN_EXR'
output_node_depth.base_path = output_path
output_node_depth.file_slots.new("Depth")

# Link nodes for Depth output
tree.links.new(render_layers_node_depth.outputs["Depth"], output_node_depth.inputs["Image"])

# Create a loop to generate synthetic data for each scene
for obj_name in objects:
    # Set light settings
    bpy.ops.object.light_add(type='POINT', location=(2, 2, 3))
    light = bpy.data.objects['Point']
    light.data.energy = 2.0  # Adjust light intensity as needed

    # Set the object in the center of the scene
    if obj_name == "Cube":
        bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, 0, 0))
    elif obj_name == "Cylinder":
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.1, location=(0, 0, 0))
    elif obj_name == "Cone":
        bpy.ops.mesh.primitive_cone_add(radius1=0.05, depth=0.1, location=(0, 0, 0))
    elif obj_name == "Sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(0, 0, 0))
    elif obj_name == "Pyramid":
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.05, depth=0.1, location=(0, 0, 0))


    for i in range(num_samples_per_scene):
        # Set camera settings with random position
        bpy.ops.object.camera_add(location=(np.random.uniform(-5, 5), np.random.uniform(-5, 5), np.random.uniform(1, 5)),
                                  rotation=(np.radians(60), 0, np.radians(45)))
        camera = bpy.data.objects['Camera']
        bpy.context.scene.camera = camera
        # Add a Track To constraint to make the camera always point towards the object
        track_to_constraint = bpy.data.objects['Camera'].constraints.new(type='TRACK_TO')
        track_to_constraint.target = bpy.data.objects[obj_name]
        track_to_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_to_constraint.up_axis = 'UP_Y'

        # Change light location for different lighting conditions
        light.location = (np.random.uniform(-5, 5), np.random.uniform(-5, 5), np.random.uniform(2, 5))

        # Render the scene
        bpy.ops.render.render(write_still=True)

        # Save RGB image
        output_node_rgb.file_slots[0].path = f"{obj_name.lower()}_rgb_{i}.png"
        bpy.ops.render.render(write_still=True)

        # Save Depth image in OpenEXR format
        output_node_depth.file_slots[0].path = f"{obj_name.lower()}_depth_{i}.exr"
        bpy.ops.render.render(write_still=True)

        # Remove the camera after rendering
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.data.objects['Camera']
        bpy.data.objects['Camera'].select_set(True)
        bpy.ops.object.delete()

print("Synthetic dataset generation complete.")
