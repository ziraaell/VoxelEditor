import numpy as np
import math

"""Klasa reprezentująca kamerę w scenie 3D."""
class Camera:
    def __init__(self, yaw, pitch, radius):
        self.yaw = yaw
        self.pitch = pitch
        self.radius = radius

    def update_from_mouse(self, dx, dy):
        """
        Aktualizuje orientację kamery na podstawie ruchu myszy.
        
        :param float dx: Różnica pozycji myszy w osi X.
        :param float dy: Różnica pozycji myszy w osi Y.
        """

        self.yaw   += dx * 0.2
        self.pitch += dy * 0.2
        self.pitch = max(-89.0, min(89.0, self.pitch))

    def zoom(self, scroll_delta):
        """
        Zmienia odległość kamery od punktu centralnego na podstawie przewijania myszy.

        :param float scroll_delta: Wartość przewijania myszy.
        """

        self.radius *= (1.0 - scroll_delta * 0.1)
        self.radius = max(5.0, min(100.0, self.radius))

    def get_pos(self, grid_center):
        """
        Oblicza pozycję kamery w przestrzeni świata na podstawie jej orientacji i odległości od centrum.

        :param np.array grid_center: 3-elementowy wektor pozycji środka świata.
        :return: 3-elementowy wektor pozycji kamery.
        """
        
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        cam_x = grid_center[0] + self.radius * math.cos(pitch_rad) * math.cos(yaw_rad)
        cam_y = grid_center[1] + self.radius * math.sin(pitch_rad)
        cam_z = grid_center[2] + self.radius * math.cos(pitch_rad) * math.sin(yaw_rad)
        return np.array([cam_x, cam_y, cam_z], dtype=np.float32)