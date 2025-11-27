import numpy as np
import math

def perspective(fov_y_deg, aspect, near, far):
    """
    Generuje macierz projekcji perspektywicznej.
    
    :param float fov_y_deg: Kąt pola widzenia w pionie w stopniach.
    :param float aspect: Stosunek szerokości do wysokości widoku.
    :param float near: Odległość od płaszczyzny bliskiej.
    :param float far: Odległość od płaszczyzny dalekiej.
    :return: Macierz projekcji 
    """

    f = 1.0 / math.tan(math.radians(fov_y_deg) / 2.0)
    M = np.zeros((4, 4), dtype=np.float32)
    M[0, 0] = f / aspect
    M[1, 1] = f
    M[2, 2] = (far + near) / (near - far)
    M[2, 3] = (2.0 * far * near) / (near - far)
    M[3, 2] = -1.0
    return M

def look_at(eye, target, up):
    """
    Generuje macierz widoku (view matrix) na podstawie pozycji kamery, punktu docelowego i wektora "up".
    
    :param np.array eye: Pozycja kamery (3-elementowy wektor).
    :param np.array target: Punkt, na który patrzy kamera (3-elementowy wektor).
    :param np.array up: Wektor "up" definiujący orientację kamery (3-elementowy wektor).
    :return: Macierz widoku (4x4).
    """
    f = target - eye
    f = f / np.linalg.norm(f)
    u = up / np.linalg.norm(up)
    s = np.cross(f, u)
    s = s / np.linalg.norm(s)
    u = np.cross(s, f)

    M = np.identity(4, dtype=np.float32)
    M[0, 0:3] = s
    M[1, 0:3] = u
    M[2, 0:3] = -f

    T = np.identity(4, dtype=np.float32)
    T[0, 3] = -eye[0]
    T[1, 3] = -eye[1]
    T[2, 3] = -eye[2]
    return M @ T

def ray_box_intersection(ray_origin, ray_dir, box_min, box_max):
    """
    Oblicza przecięcie promienia z osiągniętym pudełkiem (AABB).

    :param np.array ray_origin: Początek promienia (3-elementowy wektor).
    :param np.array ray_dir: Kierunek promienia (3-elementowy wektor, powinien być znormalizowany).
    :param np.array box_min: Minimalne współrzędne pudełka (3-elementowy wektor).
    :param np.array box_max: Maksymalne współrzędne pudełka (3-elementowy wektor).
    :return: (t_near, t_far) lub (None, None) jeśli brak przecięcia.
    """

    tmin = (box_min - ray_origin) / ray_dir
    tmax = (box_max - ray_origin) / ray_dir

    t1 = np.minimum(tmin, tmax)
    t2 = np.maximum(tmin, tmax)

    t_near = np.max(t1)
    t_far = np.min(t2)

    if t_near > t_far or t_far < 0:
        return None, None
    return t_near, t_far

def compute_ray_from_mouse(mouse_x, mouse_y, width, height, view_mat, proj_mat, cam_pos):
    """
    Oblicza promień w przestrzeni świata na podstawie pozycji myszy.

    :param float mouse_x: Pozycja myszy w pikselach (oś X).
    :param float mouse_y: Pozycja myszy w pikselach (oś Y).
    :param int width: Szerokość okna w pikselach.
    :param int height: Wysokość okna w pikselach.
    :param np.array view_mat: Macierz widoku (4x4).
    :param np.array proj_mat: Macierz projekcji (4x4).
    :param np.array cam_pos: Pozycja kamery (3-elementowy wektor).
    :return: (ray_origin, ray_dir)
    """
    x = (2.0 * mouse_x) / width - 1.0
    y = 1.0 - (2.0 * mouse_y) / height
    z = 1.0
    ray_nds = np.array([x, y, z, 1.0], dtype=np.float32)

    inv_proj = np.linalg.inv(proj_mat)
    inv_view = np.linalg.inv(view_mat)

    ray_eye = inv_proj @ ray_nds
    ray_eye = np.array([ray_eye[0], ray_eye[1], -1.0, 0.0], dtype=np.float32)

    ray_world = inv_view @ ray_eye
    ray_dir = ray_world[0:3]
    ray_dir = ray_dir / np.linalg.norm(ray_dir)

    return cam_pos, ray_dir

def create_cube_geometry(s=1.0):
    """
    Tworzy tablicę ze współrzędnymi, normalnymi i współrzędnymi tekstury dla sześcianu o rozmiarze s.
    
    :param float s: Rozmiar sześcianu.
    :return: Numpy array z danymi wierzchołków.
    """
    vertices = [
        # z+
        0, 0, s,   0, 0,   0, 0, 1,
        s, 0, s,   1, 0,   0, 0, 1,
        s, s, s,   1, 1,   0, 0, 1,
        0, 0, s,   0, 0,   0, 0, 1,
        s, s, s,   1, 1,   0, 0, 1,
        0, s, s,   0, 1,   0, 0, 1,

        # z-
        s, 0, 0,   0, 0,   0, 0,-1,
        0, 0, 0,   1, 0,   0, 0,-1,
        0, s, 0,   1, 1,   0, 0,-1,
        s, 0, 0,   0, 0,   0, 0,-1,
        0, s, 0,   1, 1,   0, 0,-1,
        s, s, 0,   0, 1,   0, 0,-1,

        # x-
        0, 0, 0,   0, 0,  -1, 0, 0,
        0, 0, s,   1, 0,  -1, 0, 0,
        0, s, s,   1, 1,  -1, 0, 0,
        0, 0, 0,   0, 0,  -1, 0, 0,
        0, s, s,   1, 1,  -1, 0, 0,
        0, s, 0,   0, 1,  -1, 0, 0,

        # x+
        s, 0, s,   0, 0,   1, 0, 0,
        s, 0, 0,   1, 0,   1, 0, 0,
        s, s, 0,   1, 1,   1, 0, 0,
        s, 0, s,   0, 0,   1, 0, 0,
        s, s, 0,   1, 1,   1, 0, 0,
        s, s, s,   0, 1,   1, 0, 0,

        # y-
        0, 0, 0,   0, 0,   0,-1, 0,
        s, 0, 0,   1, 0,   0,-1, 0,
        s, 0, s,   1, 1,   0,-1, 0,
        0, 0, 0,   0, 0,   0,-1, 0,
        s, 0, s,   1, 1,   0,-1, 0,
        0, 0, s,   0, 1,   0,-1, 0,

        # y+
        0, s, s,   0, 0,   0, 1, 0,
        s, s, s,   1, 0,   0, 1, 0,
        s, s, 0,   1, 1,   0, 1, 0,
        0, s, s,   0, 0,   0, 1, 0,
        s, s, 0,   1, 1,   0, 1, 0,
        0, s, 0,   0, 1,   0, 1, 0,
    ]

    return np.array(vertices, dtype=np.float32)