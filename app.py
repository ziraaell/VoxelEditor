import OpenGL.GLUT as GLUT
import OpenGL.GL as GL
import glfw
import time
import numpy as np

from camera import Camera
from voxel_editor import VoxelEditor
from utils import look_at, perspective
from opengl_helpers import init_geometry, init_shaders, init_window, load_texture, set_matrices, set_selection_uniforms, update_offsets_buffer, update_materials_buffer, draw_voxels, draw_text_2d
from constants import GRID_SIZE, VOXEL_SIZE, YAW, PITCH, RADIUS, WIDTH, HEIGHT

def cursor_pos_callback(window, x, y):
    """
    Callback obsługujący ruch myszy.
    
    :param window: Okno GLFW.
    :param float x: Pozycja myszy w pikselach (oś X).
    :param float y: Pozycja myszy w pikselach (oś Y).
    """
    app = glfw.get_window_user_pointer(window)
    if app is None:
        return

    app.last_mouse_pos = app.mouse_pos[:]
    app.mouse_pos = [x, y]

    if app.mouse_right:
        dx = app.mouse_pos[0] - app.last_mouse_pos[0]
        dy = app.mouse_pos[1] - app.last_mouse_pos[1]
        app.camera.update_from_mouse(dx, dy)


def mouse_button_callback(window, button, action, mods):
    """
    Callback obsługujący przyciski myszy.

    :param window: Okno GLFW.
    :param int button: Naciśnięty przycisk myszy.
    :param int action: Akcja (naciśnięcie lub zwolnienie).
    """
    
    app = glfw.get_window_user_pointer(window)
    if app is None:
        return

    if button == glfw.MOUSE_BUTTON_LEFT:
        app.mouse_left = (action == glfw.PRESS)
    if button == glfw.MOUSE_BUTTON_RIGHT:
        app.mouse_right = (action == glfw.PRESS)


def scroll_callback(window, xoffset, yoffset):
    """
    Callback obsługujący przewijanie myszy.

    :param window: Okno GLFW.
    :param float xoffset: Przesunięcie przewijania w osi X.
    :param float yoffset: Przesunięcie przewijania w osi Y.
    """
    app = glfw.get_window_user_pointer(window)
    if app is None:
        return
    app.camera.zoom(yoffset)

"""Główna klasa aplikacji."""
class App:
    def __init__(self):
        self.window = init_window()
        self.camera = Camera(YAW, PITCH, RADIUS)
        self.world = VoxelEditor(GRID_SIZE, VOXEL_SIZE)

        self.mouse_pos = [WIDTH / 2.0, HEIGHT / 2.0]
        self.last_mouse_pos = self.mouse_pos.copy()
        self.mouse_left = False
        self.mouse_right = False

        glfw.set_window_user_pointer(self.window, self)
        glfw.set_cursor_pos_callback(self.window, cursor_pos_callback)
        glfw.set_mouse_button_callback(self.window, mouse_button_callback)
        glfw.set_scroll_callback(self.window, scroll_callback)

        self.program, self.loc_view, self.loc_proj, self.loc_selected, self.loc_highlight, self.loc_light, self.loc_viewpos = init_shaders()

        GLUT.glutInit()
        GL.glEnable(GL.GL_DEPTH_TEST)

        self.textures = [
            load_texture("Textures/wood_texture.jpg"),     
            load_texture("Textures/grass.jpg"),    
            load_texture("Textures/stone.jpg"),   
            load_texture("Textures/sand.jpg"), 
            load_texture("Textures/leaves.jpg"),
        ]

        self.current_material_id = 0
        self.vao, self.vbo_cube, self.vbo_offsets, self.vbo_materials, self.num_cube_vertices = init_geometry()
        self.selected_voxel = None
        self.last_action_time = 0.0

    def run(self):
        """Główna pętla aplikacji."""

        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            width, height = glfw.get_framebuffer_size(self.window)
            aspect = width / float(height if height > 0 else 1)

            GL.glViewport(0, 0, width, height)
            GL.glClearColor(0.05, 0.05, 0.08, 1.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            grid_center = self.world.get_center()
            cam_pos = self.camera.get_pos(grid_center)
            view = look_at(cam_pos, grid_center, np.array([0.0, 1.0, 0.0], dtype=np.float32))
            proj = perspective(45.0, aspect, 0.1, 500.0)

            self.selected_voxel = self.world.pick(self.mouse_pos[0], self.mouse_pos[1], width, height, view, proj, cam_pos)

            if glfw.get_key(self.window, glfw.KEY_1) == glfw.PRESS:
                    self.current_material_id = 0 
            elif glfw.get_key(self.window, glfw.KEY_2) == glfw.PRESS:
                    self.current_material_id = 1   
            elif glfw.get_key(self.window, glfw.KEY_3) == glfw.PRESS:
                    self.current_material_id = 2   
            elif glfw.get_key(self.window, glfw.KEY_4) == glfw.PRESS:
                    self.current_material_id = 3  
            elif glfw.get_key(self.window, glfw.KEY_5) == glfw.PRESS:
                    self.current_material_id = 4    
           
            now = time.time()
            if now - self.last_action_time > 0.15 and self.selected_voxel is not None:
                if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
                    self.world.remove(self.selected_voxel)
                    self.last_action_time = now
                elif glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
                    self.world.add_next_to(self.selected_voxel, self.mouse_pos[0], self.mouse_pos[1], width, height, view, proj, cam_pos, self.current_material_id)
                    self.last_action_time = now

            update_offsets_buffer(self.vbo_offsets, self.world.offsets)
            update_materials_buffer(self.vbo_materials, self.world.material_ids)

            GL.glUseProgram(self.program)
            set_matrices(self.loc_view, self.loc_proj, view, proj)
            set_selection_uniforms(self.loc_selected, self.loc_highlight, self.selected_voxel)

            GL.glUniform3f(self.loc_light, GRID_SIZE * 1.25, GRID_SIZE * 2.25, GRID_SIZE * 1.25)
            GL.glUniform3f(self.loc_viewpos, cam_pos[0], cam_pos[1], cam_pos[2])

            for i, tex_id in enumerate(self.textures):
                GL.glActiveTexture(GL.GL_TEXTURE0 + i)
                GL.glBindTexture(GL.GL_TEXTURE_2D, tex_id)

            draw_voxels(self.vao, self.num_cube_vertices, self.world.offsets)

            for i, tex_id in enumerate(self.textures):
                GL.glActiveTexture(GL.GL_TEXTURE0 + i)
                GL.glBindTexture(GL.GL_TEXTURE_2D, tex_id)


            draw_text_2d(10, height - 20,  "A: dodaj blok")
            draw_text_2d(10, height - 40,  "D: usun blok")
            draw_text_2d(10, height - 60,  "Klawisze 1-5: wybór materialu (1-drewno, 2-trawa, 3-kamien, 4-piasek, 5-liście)")
            draw_text_2d(10, height - 80,  "Rolka: zoom")
            draw_text_2d(10, height - 100, "PPM + ruch myszą: obracanie kamery")
            glfw.swap_buffers(self.window)
        
        glfw.terminate()

if __name__ == "__main__":
    app = App()
    app.run()