bl_info = {
    "name": "Combine Selected Objects To A Single Convex Mesh",
    "blender": (3, 3, 1),
    "category": "Object",
}

import bpy

def select_one_object(obj):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

class MakeSelectedMeshesConvex(bpy.types.Operator):

    bl_idname = "object.combinemultipletoconvex"
    bl_label = "Combine Selected Objects To A Single Convex Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
    
        objects = bpy.context.selected_objects;

        if len(objects) <= 1:
            print("Select more than one object to combine")
            return {'CANCELLED'}

        #Add the boolean modifiers to all the objects
        for i in range(1, len(objects)):
            object = objects[i]
            select_one_object(object)
            bmod = object.modifiers.new("_TMP Boolean", 'BOOLEAN')
            bmod.operation = 'UNION'
            bmod.object = objects[i - 1]

        #apply the modifier of the last object
        select_one_object(objects[len(objects) - 1])
        bpy.ops.object.modifier_apply(modifier="_TMP Boolean")

        #remove the modifiers on the other objects
        for object in objects:
            select_one_object(object)
            bpy.ops.object.modifier_remove(modifier="_TMP Boolean")
        return {'FINISHED'}
        
def menu_func(self, context):
    self.layout.operator(MakeSelectedMeshesConvex.bl_idname)

def register():
    bpy.utils.register_class(MakeSelectedMeshesConvex)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(MakeSelectedMeshesConvex)
