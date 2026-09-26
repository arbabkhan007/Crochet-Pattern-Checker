"""
Multi-Dimensional Stitch Mapper - Map complex 3D and multi-layer patterns
"""


class MultiDimensionalStitchMapper:
    def __init__(self):
        self.dimensions = {
            "2d": {"layers": 1, "complexity": "basic"},
            "3d": {"layers": "multiple", "complexity": "advanced"},
            "multi_layer": {"layers": "stacked", "complexity": "expert"},
        }

    def map_3d_pattern(self, pattern_layers: list) -> dict:
        """Map multi-layer 3D pattern"""
        layer_analysis = []

        for i, layer in enumerate(pattern_layers):
            layer_info = {
                "layer": i + 1,
                "stitch_count": len(layer.split(",")),
                "complexity": "high" if "inc" in layer or "dec" in layer else "medium",
            }
            layer_analysis.append(layer_info)

        return {
            "total_layers": len(pattern_layers),
            "layer_analysis": layer_analysis,
            "construction_method": self._determine_construction(layer_analysis),
            "assembly_required": len(pattern_layers) > 1,
        }

    def _determine_construction(self, layers: list) -> str:
        if len(layers) == 1:
            return "flat construction"
        elif all(l["complexity"] == "high" for l in layers):
            return "multi-dimensional shaping"
        else:
            return "layered assembly"

    def generate_assembly_guide(self, mapping: dict) -> str:
        """Generate assembly instructions for complex patterns"""
        guide = "🔧 ASSEMBLY GUIDE\n" + "=" * 60 + "\n\n"

        if mapping["assembly_required"]:
            guide += "Construction Method: " + mapping["construction_method"] + "\n\n"
            guide += "Steps:\n"
            for i, layer in enumerate(mapping["layer_analysis"], 1):
                guide += f"{i}. Complete Layer {layer['layer']} ({layer['stitch_count']} stitches)\n"
            guide += f"\n{len(mapping['layer_analysis']) + 1}. Assemble all layers\n"
            guide += f"{len(mapping['layer_analysis']) + 2}. Finish edges and seams\n"
        else:
            guide += "Single layer construction - no assembly needed\n"

        return guide


if __name__ == "__main__":
    print("🎲 Multi-Dimensional Stitch Mapper")
    print("=" * 60)

    mapper = MultiDimensionalStitchMapper()

    # Test with 3D pattern
    pattern_layers = [
        "sc 6, inc 6, sc 12",
        "sc 12, inc 6, sc 18",
        "sc 18, dec 6, sc 12",
    ]

    mapping = mapper.map_3d_pattern(pattern_layers)
    print(f"\nTotal Layers: {mapping['total_layers']}")
    print(f"Construction: {mapping['construction_method']}")
    print(f"Assembly Required: {mapping['assembly_required']}")

    print("\n" + mapper.generate_assembly_guide(mapping))
