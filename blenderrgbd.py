import os
import bpy
import numpy as np

# Set the path to save the generated dataset
output_path = "C:\\Users\\Raashid\\Thesis\\Data\\data"
os.makedirs(output_path, exist_ok=True)

# Set the number of samples you want to generate
num_samples = 10

# Set Blender scene settings
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Set camera settings
bpy.ops.object.camera_add(location=(0, -2, 1), rotation=(np.radians(56), 0, np.radians(0)))  # Adjust rotation as needed
camera = bpy.data.objects['Camera']
bpy.context.scene.camera = camera

# Set cube settings
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, 0, 0))
cube = bpy.data.objects['Cube']

# Set plane settings
bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, -0.05))  # Adjust size and location as needed
plane = bpy.data.objects['Plane']

track_to_constraint = camera.constraints.new(type='TRACK_TO')
track_to_constraint.target = cube
track_to_constraint.track_axis = 'TRACK_NEGATIVE_Z'
track_to_constraint.up_axis = 'UP_Y'


# Set light settings
bpy.ops.object.light_add(type='POINT', location=(1, 0, 0))
light = bpy.data.objects['Point']
light.data.energy = 2.0  # Adjust light intensity as needed

# Set Blender rendering settings
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'
bpy.context.scene.render.resolution_x = 160
bpy.context.scene.render.resolution_y = 120
bpy.context.scene.render.resolution_percentage = 100
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
output_node_depth.format.file_format = 'PNG'
output_node_depth.base_path = output_path
output_node_depth.file_slots.new("Depth")

# Link nodes for Depth output
tree.links.new(render_layers_node_depth.outputs["Depth"], output_node_depth.inputs["Image"])

# Create a loop to generate synthetic data
for i in range(num_samples):
    # Change light location for different lighting conditions
    light.location = (np.random.uniform(-5, 5), np.random.uniform(-5, 5), np.random.uniform(2, 5))
    camera.location = ((np.random.uniform(-5, 5), np.random.uniform(-5, 5), np.random.uniform(1, 5)))
    # Render the scene
    bpy.ops.render.render(write_still=True)

    # Save RGB image
    output_node_rgb.file_slots[0].path = f"rgb_{i}.png"
    bpy.ops.render.render(write_still=True)

    # Save Depth image
    output_node_depth.file_slots[0].path = f"depth_{i}.png"
    bpy.ops.render.render(write_still=True)

    with open(os.path.join(output_path, f"location_{i}.txt"), 'w') as f:
        f.write(f"Camera {bpy.context.scene.camera.location.x} {bpy.context.scene.camera.location.y} {bpy.context.scene.camera.location.z}\n")
        f.write(f"Light {light.location.x} {light.location.y} {light.location.z}")

print("Dataset generation complete.")
