from manim import *
import numpy as np


class RightTriangle(Polygon):
    def __init__(self, side_a: float, side_b: float, **kwargs) -> None:
        super().__init__(ORIGIN, side_a * RIGHT, side_b * UP, **kwargs)

    def get_side_centers(self, buffer: float = MED_LARGE_BUFF) -> np.ndarray:
        v1, v2, v3 = self.get_vertices()
        centers = [Line(a, b).get_center() for a, b in zip([v1, v2, v3], [v2, v3, v1])]

        def normalize(v):
            return v / np.linalg.norm(v)

        def unit_normal_helper(a, b):
            v = b - a
            n = np.array([-v[1], v[0], 0])
            return normalize(n)

        normals = [unit_normal_helper(a, b) for a, b in zip([v1, v2, v3], [v2, v3, v1])]
        sign = -1 if (np.cross(v2 - v1, v3 - v1) > 0).any() else 1
        centers = [center + buffer * normal * sign for center, normal in zip(centers, normals)]

        return np.array(centers)

    def get_labels(self, labels: list[str] = ["a", "b", "c"]) -> VGroup:
        centers = self.get_side_centers()
        return VGroup(*[MathTex(label).move_to(pos) for label, pos in zip(labels, centers)])
