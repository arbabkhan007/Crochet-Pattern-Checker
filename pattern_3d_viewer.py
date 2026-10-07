"""Text positions are not a measured size."""

class Pattern3DViewer:
    def __init__(self):
        self.render_modes = ["wireframe", "solid", "textured"]

    def generate_3d_coordinates(self, pattern_text: str) -> list:
        return []

    def create_rotation_animation(self) -> str:
        return "No animation was made. Coordinates are not millimetres."

if __name__ == "__main__":
    print(Pattern3DViewer().create_rotation_animation())
