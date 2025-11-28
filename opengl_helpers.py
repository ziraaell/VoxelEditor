import OpenGL.GLUT as GLUT
import OpenGL.GL as GL
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import ctypes
import numpy as np
from PIL import Image

from utils import create_cube_geometry
from constants import WIDTH, HEIGHT, VOXEL_SIZE

def init_window():
    """Inicjalizuje okno GLFW i kontekst OpenGL."""

    if not glfw.init():
        raise RuntimeError("Nie udało się zainicjalizować GLFW")

    window = glfw.create_window(WIDTH, HEIGHT, "Voxel Editor 3D", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Nie udało się stworzyć okna")

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    return window


def init_shaders():
    """
    Inicjalizuje i kompiluje shadery, zwraca program i lokalizacje uniformów.
    
    :return: tuple (program, loc_view, loc_proj, loc_selected, loc_highlight, loc_light, loc_viewpos)
    """

    vertex_src = load_shader_source("shaders/voxel.vert")
    fragment_src = load_shader_source("shaders/voxel.frag")

    program = compileProgram(compileShader(vertex_src, GL.GL_VERTEX_SHADER), compileShader(fragment_src, GL.GL_FRAGMENT_SHADER))
    GL.glUseProgram(program)

    loc_view = GL.glGetUniformLocation(program, "u_view")
    loc_proj = GL.glGetUniformLocation(program, "u_proj")
    loc_selected = GL.glGetUniformLocation(program, "u_selected")
    loc_highlight = GL.glGetUniformLocation(program, "u_highlight_selected")
    loc_light = GL.glGetUniformLocation(program, "u_light_pos")
    loc_viewpos = GL.glGetUniformLocation(program, "u_view_pos")
    loc_textures = GL.glGetUniformLocation(program, "u_textures")
    GL.glUniform1iv(loc_textures, 5, (GL.GLint * 5)(0, 1, 2, 3, 4))

    return program, loc_view, loc_proj, loc_selected, loc_highlight, loc_light, loc_viewpos


def init_geometry():
    """
    Inicjalizuje geometrię sześcianu i zwraca VAO, VBO oraz liczbę wierzchołków.
    
    :return: tuple (vao, vbo_cube, vbo_offsets, vbo_materials, num_cube_vertices)
    """

    cube_vertices = create_cube_geometry(VOXEL_SIZE)
    num_cube_vertices = len(cube_vertices) // 8
    stride = 8 * 4

    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)

    vbo_cube = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_cube)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, cube_vertices.nbytes, cube_vertices, GL.GL_STATIC_DRAW)

    GL.glEnableVertexAttribArray(0)
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(0))

    GL.glEnableVertexAttribArray(2)
    GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(12))

    GL.glEnableVertexAttribArray(3)
    GL.glVertexAttribPointer(3, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(20))

    vbo_offsets = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_offsets)
    GL.glEnableVertexAttribArray(1)
    GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
    GL.glVertexAttribDivisor(1, 1)

    vbo_materials = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_materials)
    GL.glEnableVertexAttribArray(4)
    GL.glVertexAttribPointer(4, 1, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
    GL.glVertexAttribDivisor(4, 1)

    GL.glBindVertexArray(0)

    return vao, vbo_cube, vbo_offsets, vbo_materials, num_cube_vertices


def update_instance_buffers(vbo_offsets, vbo_materials, world):
    """
    Aktualizuje bufory instancji dla przesunięć i materiałów na podstawie stanu świata.
    
    :param int vbo_offsets: ID bufora przesunięć.
    :param int vbo_materials: ID bufora identyfikatorów materiałów.
    :param World world: Obiekt świata voxelowego.
    """

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_offsets)
    if len(world.offsets) > 0:
        GL.glBufferData(GL.GL_ARRAY_BUFFER, world.offsets.nbytes, world.offsets, GL.GL_DYNAMIC_DRAW)
    else:
        GL.glBufferData(GL.GL_ARRAY_BUFFER, 0, None, GL.GL_DYNAMIC_DRAW)

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_materials)
    if len(world.instance_material_ids) > 0:
        GL.glBufferData(GL.GL_ARRAY_BUFFER, world.instance_material_ids.nbytes, world.instance_material_ids, GL.GL_DYNAMIC_DRAW)
    else:
        GL.glBufferData(GL.GL_ARRAY_BUFFER, 0, None, GL.GL_DYNAMIC_DRAW)


def load_texture(path):
    """
    Ładuje teksturę z pliku i zwraca jej ID.

    :param str path: Ścieżka do pliku tekstury.
    :return: ID tekstury OpenGL.
    """

    img = Image.open(path).convert("RGBA")
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.frombuffer(img.tobytes(), dtype=np.uint8)

    width, height = img.size

    tex_id = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, tex_id)

    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, img_data)
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
    return tex_id

def load_shader_source(path: str):
    """
    Ładuje kod źródłowy shadera z pliku.
    :param str path: Ścieżka do pliku shadera.
    :return: Kod źródłowy shadera jako string.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def update_offsets_buffer(vbo_offsets, offsets):
    """
    Aktualizuje bufor przesunięć instancji.

    :param int vbo_offsets: ID bufora przesunięć.
    :param np.array offsets: Tablica przesunięć.
    """

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_offsets)
    if len(offsets) > 0:
        GL.glBufferData(GL.GL_ARRAY_BUFFER, offsets.nbytes, offsets, GL.GL_DYNAMIC_DRAW)
    else:
        GL.glBufferData(GL.GL_ARRAY_BUFFER, 0, None, GL.GL_DYNAMIC_DRAW)

def update_materials_buffer(vbo_materials, material_ids):
    """
    Aktualizuje bufor identyfikatorów materiałów instancji.

    :param int vbo_materials: ID bufora identyfikatorów materiałów.
    :param list material_ids: Lista identyfikatorów materiałów.
    """

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_materials)

    if material_ids is not None and len(material_ids) > 0:
        arr = np.array(material_ids, dtype=np.float32)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, arr.nbytes, arr, GL.GL_DYNAMIC_DRAW)
    else:
        GL.glBufferData(GL.GL_ARRAY_BUFFER, 0, None, GL.GL_DYNAMIC_DRAW)


def set_matrices(loc_view, loc_proj, view, proj):
    """
    Ustawia macierze widoku i projekcji w shaderach.

    :param int loc_view: Lokalizacja uniformu macierzy widoku.
    :param int loc_proj: Lokalizacja uniformu macierzy projekcji.
    :param np.array view: Macierz widoku (4x4).
    :param np.array proj: Macierz projekcji (4x4).
    """

    GL.glUniformMatrix4fv(loc_view, 1, GL.GL_FALSE, view.T)
    GL.glUniformMatrix4fv(loc_proj, 1, GL.GL_FALSE, proj.T)


def set_selection_uniforms(loc_selected, loc_highlight, selected_voxel):
    """
    Ustawia uniformy zaznaczenia voxela w shaderach.

    :param int loc_selected: Lokalizacja uniformu zaznaczonego voxela.
    :param int loc_highlight: Lokalizacja uniformu podświetlenia zaznaczenia.
    :param selected_voxel: 3-elementowy wektor współrzędnych zaznaczonego voxela lub None.
    """

    if selected_voxel is not None:
        GL.glUniform1i(loc_highlight, GL.GL_TRUE)
        GL.glUniform3i(loc_selected, selected_voxel[0], selected_voxel[1], selected_voxel[2])
    else:
        GL.glUniform1i(loc_highlight, GL.GL_FALSE)
        GL.glUniform3i(loc_selected, -1, -1, -1)


def draw_voxels(vao, num_cube_vertices, offsets):
    """
    Rysuje voxele za pomocą instancjonowania.

    :param int vao: ID VAO sześcianu.
    :param int num_cube_vertices: Liczba wierzchołków sześcianu.
    :param np.array offsets: Tablica przesunięć instancji.
    """

    GL.glBindVertexArray(vao)
    if len(offsets) > 0:
        GL.glDrawArraysInstanced(GL.GL_TRIANGLES, 0, num_cube_vertices, len(offsets))
    GL.glBindVertexArray(0)

def draw_text_2d(x, y, text, font=GLUT.GLUT_BITMAP_9_BY_15):
    """
    Rysuje tekst 2D na ekranie w pozycji (x, y).

    :param float x: Pozycja tekstu w pikselach (oś X).
    :param float y: Pozycja tekstu w pikselach (oś Y).
    :param str text: Tekst do wyświetlenia.
    :param font: Czcionka GLUT do użycia.
    """

    GL.glUseProgram(0)
    GL.glColor3f(1.0, 1.0, 1.0)
    GL.glWindowPos2f(x, y)
    for ch in text:
        GLUT.glutBitmapCharacter(font, ord(ch))