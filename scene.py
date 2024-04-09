# scene.py
import numpy as np
from pyrr import Matrix44

class Moon:
    def __init__(self, radius=1):
        self.radius = radius
        self.rotation_speed = 0.001  # Adjust this value to control the rotation speed

    def update(self, time):
        """
        Update the Moon's rotation based on the elapsed time.
        """
        self.rotation_matrix = Matrix44.from_y_rotation(time * self.rotation_speed)

    def get_transformation_matrix(self):
        """
        Return the transformation matrix for the Moon.
        """
        return self.rotation_matrix

class AsteroidImpact:
    def __init__(self, impact_data):
        self.time_of_impact = impact_data['time_of_impact']
        self.latitude = impact_data['latitude']
        self.longitude = impact_data['longitude']
        self.crater_diameter = impact_data['diameter']

    def get_impact_position(self, moon):
        """
        Calculate the impact position on the Moon's surface based on the latitude and longitude.
        """
        lat = self.latitude * np.pi / 180
        lon = self.longitude * np.pi / 180

        x = moon.radius * np.cos(lat) * np.cos(lon)
        y = moon.radius * np.sin(lat)
        z = moon.radius * np.cos(lat) * np.sin(lon)

        return np.array([x, y, z])

    def is_active(self, time):
        """
        Check if the asteroid impact should be rendered based on the current time.
        """
        return time >= self.time_of_impact