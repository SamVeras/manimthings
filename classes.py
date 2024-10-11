from manim import *
import numpy as np


class RightTriangle(Polygon):
    def __init__(self, side_a: float, side_b: float, **kwargs) -> None:
        super().__init__(ORIGIN, side_a * RIGHT, side_b * UP, **kwargs)

    def get_side_centers(self, buffer: float = MED_LARGE_BUFF) -> np.ndarray:
        # As vértices do triângulo, começando do inferior esquerdo, em sentido anti-horário
        v1, v2, v3 = self.get_vertices()

        # O centro de cada aresta do triângulop
        centers = [Line(a, b).get_center() for a, b in zip([v1, v2, v3], [v2, v3, v1])]

        # Função auxiliar pra normalizar um vetor (deixar magnitude = 1)
        def normalize(v):
            return v / np.linalg.norm(v)

        # Função auxiliar para calcular a normal unitária de um vetor definido por dois pontos a e b
        # Normal = vetor "perpendicular" ao vetor que vai de a -> b
        def unit_normal_helper(a, b):
            v = b - a
            n = np.array([-v[1], v[0], 0])
            return normalize(n)

        normals = [unit_normal_helper(a, b) for a, b in zip([v1, v2, v3], [v2, v3, v1])]
        # Esse produto cruzado é necessário pra determinar se o normal é somado ou subtraído
        # É necessário caso tenhamos um triângulo flipado, por ex.
        # Não dá pra entender só aceite
        sign = -1 if (np.cross(v2 - v1, v3 - v1) > 0).any() else 1

        # Ajustar os centros com o buffer
        centers = [center + buffer * normal * sign for center, normal in zip(centers, normals)]

        return np.array(centers)

    def get_labels(self, labels: list[str] = ["a", "b", "c"]) -> VGroup:
        centers = self.get_side_centers()
        return VGroup(*[MathTex(label).move_to(pos) for label, pos in zip(labels, centers)])

    def get_angles(self, right_angle_length=0.4, angle_radius=0.7, color=WHITE) -> VGroup:
        v1, v2, v3 = self.get_vertices()
        # Não vou comentar essas paradas acho q dá pra entender
        right_angle = RightAngle(Line(v1, v2), Line(v1, v3), length=right_angle_length)
        angle1 = Angle.from_three_points(v1, v2, v3, radius=angle_radius, other_angle=True)
        angle2 = Angle.from_three_points(v2, v3, v1, radius=angle_radius, other_angle=True)
        for a in [right_angle, angle1, angle2]:
            a.set_color(color)
        return VGroup(*[right_angle, angle1, angle2])
