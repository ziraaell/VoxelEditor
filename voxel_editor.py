import numpy as np
from utils import compute_ray_from_mouse, ray_box_intersection
# jeśli używasz pakietu "Projekt", możesz też dać:
# from Projekt.utils import compute_ray_from_mouse, ray_box_intersection

"""
Klasa reprezentująca edytor voxelowy i operacje na voxelach.
"""
class VoxelEditor:
    def __init__(self, grid_size, voxel_size):
        self.grid_size = grid_size
        self.voxel_size = voxel_size
        self.voxels = np.zeros((grid_size, grid_size, grid_size), dtype=np.uint8)
        self.material_ids_3d = np.zeros((grid_size, grid_size, grid_size), dtype=np.uint8)

        center = grid_size // 2
        self.voxels[center-1:center+2, center-1:center+2, center-1:center+2] = 1
        self.material_ids_3d[center-1:center+2, center-1:center+2, center-1:center+2] = 1  
        self.offsets = None                #
        self.material_ids = None           

        self.build_instance_data()

    def get_center(self):
        """
        Środek świata w jednostkach świata (do ustawienia kamery).
        
        :return: 3-elementowy wektor pozycji środka świata.
        """
        return np.array([
            self.grid_size * self.voxel_size / 2.0,
            self.grid_size * self.voxel_size / 2.0,
            self.grid_size * self.voxel_size / 2.0,
        ], dtype=np.float32)

    def build_instance_data(self):
        """
        Buduje tablice offsetów i identyfikatorów materiałów dla istniejących voxeli.

        :return: None
        """
        xs, ys, zs = np.where(self.voxels == 1)

        if len(xs) == 0:
            self.offsets = np.zeros((0, 3), dtype=np.float32)
            self.material_ids = np.zeros((0,), dtype=np.float32)
            return

        self.offsets = np.stack([xs, ys, zs], axis=1).astype(np.float32) * self.voxel_size
        self.material_ids = self.material_ids_3d[xs, ys, zs].astype(np.float32)

    def pick(self, mouse_x, mouse_y, width, height, view_mat, proj_mat, cam_pos):
        """
        Wybiera voxel na podstawie pozycji myszy.

        :param float mouse_x: Pozycja myszy w pikselach (oś X).
        :param float mouse_y: Pozycja myszy w pikselach (oś Y).
        :param int width: Szerokość okna w pikselach.
        :param int height: Wysokość okna w pikselach.
        :param np.array view_mat: Macierz widoku (4x4).
        :param np.array proj_mat: Macierz projekcji (4x4).
        :param np.array cam_pos: Pozycja kamery (3-elementowy wektor).
        :return: 3-elementowy wektor współrzędnych voxelowych wybranego voxela lub None.
        """
        ray_origin, ray_dir = compute_ray_from_mouse(mouse_x, mouse_y, width, height, view_mat, proj_mat, cam_pos)

        closest_t = float('inf')
        selected = None

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    if self.voxels[x, y, z] == 0:
                        continue

                    box_min = np.array([x, y, z], dtype=np.float32) * self.voxel_size
                    box_max = box_min + self.voxel_size

                    t_near, _ = ray_box_intersection(ray_origin, ray_dir, box_min, box_max)
                    if t_near is not None and t_near < closest_t and t_near >= 0.0:
                        closest_t = t_near
                        selected = (x, y, z)

        return selected

    def add_next_to(self, selected_voxel, mouse_x, mouse_y, width, height, view_mat, proj_mat, cam_pos,current_material_id):
        """
        Dodaje voxel obok wybranego voxela na podstawie pozycji myszy.

        :param selected_voxel: 3-elementowy wektor współrzędnych voxelowych wybranego voxela.
        :param float mouse_x: Pozycja myszy w pikselach (oś X).
        :param float mouse_y: Pozycja myszy w pikselach (oś Y).
        :param int width: Szerokość okna w pikselach.
        :param int height: Wysokość okna w pikselach.
        :param np.array view_mat: Macierz widoku (4x4).
        :param np.array proj_mat: Macierz projekcji (4x4).
        :param np.array cam_pos: Pozycja kamery (3-elementowy wektor).
        :param int current_material_id: Identyfikator materiału dla nowego voxela.
        :return: None
        """
        if selected_voxel is None:
            return

        ray_origin, ray_dir = compute_ray_from_mouse(mouse_x, mouse_y, width, height, view_mat, proj_mat, cam_pos)

        x, y, z = selected_voxel
        box_min = np.array([x, y, z], dtype=np.float32) * self.voxel_size
        box_max = box_min + self.voxel_size

        t_near, _ = ray_box_intersection(ray_origin, ray_dir, box_min, box_max)
        if t_near is None:
            return

        hit_point = ray_origin + t_near * ray_dir

        eps = 1e-3
        normal = np.array([0, 0, 0], dtype=int)

        if abs(hit_point[0] - box_min[0]) < eps:
            normal = np.array([-1, 0, 0], dtype=int)
        elif abs(hit_point[0] - box_max[0]) < eps:
            normal = np.array([1, 0, 0], dtype=int)
        elif abs(hit_point[1] - box_min[1]) < eps:
            normal = np.array([0, -1, 0], dtype=int)
        elif abs(hit_point[1] - box_max[1]) < eps:
            normal = np.array([0, 1, 0], dtype=int)
        elif abs(hit_point[2] - box_min[2]) < eps:
            normal = np.array([0, 0, -1], dtype=int)
        elif abs(hit_point[2] - box_max[2]) < eps:
            normal = np.array([0, 0, 1], dtype=int)

        new_voxel = np.array([x, y, z], dtype=int) + normal
        nx, ny, nz = new_voxel

        if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and 0 <= nz < self.grid_size:
            self.voxels[nx, ny, nz] = 1
            self.material_ids_3d[nx, ny, nz] = current_material_id
            self.build_instance_data()

    def remove(self, selected_voxel):
        """
        Usuwa wybrany voxel.
        
        :param selected_voxel: 3-elementowy wektor współrzędnych voxelowych wybranego voxela.
        :return: None
        """
        if selected_voxel is None:
            return
        x, y, z = selected_voxel
        self.voxels[x, y, z] = 0
        self.material_ids_3d[x, y, z] = 0
        self.build_instance_data()

