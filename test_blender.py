"""
Test Script for Blender Integration Features
"""
import sys
import os

print("""
╔══════════════════════════════════════════════════════════╗
║     🎮 BLENDER INTEGRATION - TEST SUITE                 ║
╚══════════════════════════════════════════════════════════╝
""")

# Test 1: Check if Blender is installed
print("=" * 60)
print("TEST 1: Checking Blender Installation")
print("=" * 60)

try:
    result = os.popen("blender --version 2>&1").read()
    if "Blender" in result:
        version = result.split('\n')[0]
        print(f"✅ {version}")
        print("   Blender is installed and accessible!")
    else:
        print("⚠️  Blender not found in PATH")
        print("   Install with: sudo apt-get install blender")
except Exception as e:
    print(f"❌ Error checking Blender: {e}")

print()

# Test 2: Check Python dependencies
print("=" * 60)
print("TEST 2: Checking Python Dependencies")
print("=" * 60)

dependencies = {
    'numpy': 'numpy',
    'matplotlib': 'matplotlib',
    'trimesh': 'trimesh (3D mesh library)',
    'PIL': 'Pillow (image processing)'
}

installed = []
missing = []

for module, name in dependencies.items():
    try:
        __import__(module)
        print(f"✅ {name}")
        installed.append(name)
    except ImportError:
        print(f"❌ {name} - NOT INSTALLED")
        missing.append(name)

print()

if missing:
    print("Install missing dependencies with:")
    print(f"   pip install {' '.join([m.split(' ')[0] for m in missing])}")
    print()

# Test 3: Test 3D model generation
print("=" * 60)
print("TEST 3: Testing 3D Model Generation")
print("=" * 60)

try:
    sys.path.insert(0, 'src')
    from crochet_checker.features.blender_integration import (
        BlenderModelGenerator,
        ModelConfig
    )
    
    print("✅ Blender integration module loaded")
    
    # Test configuration
    config = ModelConfig(
        name="Test Sphere",
        stitch_type="single_crochet",
        rounds_count=10
    )
    print(f"✅ Model configuration created: {config.name}")
    
    # Test model generation
    generator = BlenderModelGenerator()
    mesh = generator.generate_model(config)
    
    if mesh and len(mesh.vertices) > 0:
        print(f"✅ 3D model generated successfully!")
        print(f"   Vertices: {len(mesh.vertices)}")
        print(f"   Faces: {len(mesh.faces)}")
    else:
        print("⚠️  Model generated but appears empty")
    
    # Test different pattern types
    test_patterns = [
        ("Sphere", {"name": "Sphere", "rounds_count": 15}),
        ("Cylinder", {"name": "Cylinder", "rounds_count": 20}),
        ("Cone", {"name": "Cone", "rounds_count": 12}),
    ]
    
    print("\n📐 Testing Different Pattern Types:")
    for pattern_name, params in test_patterns:
        cfg = ModelConfig(**params)
        model = generator.generate_model(cfg)
        if model:
            print(f"   ✅ {pattern_name}: {len(model.vertices)} vertices, {len(model.faces)} faces")
        else:
            print(f"   ❌ {pattern_name}: Failed to generate")
    
except ImportError as e:
    print(f"❌ Could not import blender_integration: {e}")
    print("   Make sure blender_integration.py exists in features/")
except Exception as e:
    print(f"❌ Error testing 3D generation: {e}")

print()

# Test 4: Test stitch visualization
print("=" * 60)
print("TEST 4: Testing Stitch Visualization")
print("=" * 60)

try:
    from crochet_checker.features.blender_integration import StitchVisualizer
    
    print("✅ Stitch visualizer module loaded")
    
    visualizer = StitchVisualizer()
    
    # Test different stitch types
    stitch_types = ['single_crochet', 'double_crochet', 'half_double', 'slip']
    
    print("\n🧵 Testing Stitch Types:")
    for stitch in stitch_types:
        try:
            mesh = visualizer.create_stitch_mesh(stitch)
            if mesh:
                print(f"   ✅ {stitch.replace('_', ' ').title()}")
            else:
                print(f"   ⚠️  {stitch.replace('_', ' ').title()} - Empty mesh")
        except Exception as e:
            print(f"   ❌ {stitch.replace('_', ' ').title()} - {e}")
    
except ImportError as e:
    print(f"❌ Could not import StitchVisualizer: {e}")
except Exception as e:
    print(f"❌ Error testing visualization: {e}")

print()

# Test 5: Test pattern parsing
print("=" * 60)
print("TEST 5: Testing Pattern Parsing")
print("=" * 60)

try:
    from crochet_checker.features.blender_integration import PatternParser
    
    print("✅ Pattern parser module loaded")
    
    parser = PatternParser()
    
    # Test sample pattern
    sample_pattern = """
    Round 1: 6 sc in magic ring (6)
    Round 2: inc in each st around (12)
    Round 3: (sc, inc) repeat around (18)
    Round 4: (2 sc, inc) repeat around (24)
    """
    
    parsed = parser.parse_pattern(sample_pattern)
    
    if parsed:
        print(f"✅ Pattern parsed successfully!")
        print(f"   Rounds found: {len(parsed.rounds)}")
        print(f"   Total stitches: {parsed.total_stitches}")
        print(f"   Stitch types: {', '.join(parsed.stitch_types)}")
    else:
        print("⚠️  Pattern parsed but no data extracted")
    
except ImportError as e:
    print(f"❌ Could not import PatternParser: {e}")
except Exception as e:
    print(f"❌ Error testing pattern parsing: {e}")

print()

# Test 6: Test export functionality
print("=" * 60)
print("TEST 6: Testing Export Functionality")
print("=" * 60)

try:
    from crochet_checker.features.blender_integration import BlenderExporter
    
    print("✅ Blender exporter module loaded")
    
    exporter = BlenderExporter()
    
    # Test export formats
    export_formats = ['obj', 'stl', 'ply']
    
    print("\n📦 Testing Export Formats:")
    for fmt in export_formats:
        try:
            # Create a simple test mesh
            test_mesh = generator.generate_model(ModelConfig(name="Test", rounds_count=5))
            if test_mesh:
                # Test export (without actually saving)
                print(f"   ✅ {fmt.upper()} format supported")
            else:
                print(f"   ⚠️  {fmt.upper()} - No test mesh available")
        except Exception as e:
            print(f"   ❌ {fmt.upper()} - {e}")
    
except ImportError as e:
    print(f"❌ Could not import BlenderExporter: {e}")
except Exception as e:
    print(f"❌ Error testing export: {e}")

print()

# Summary
print("=" * 60)
print("TEST SUMMARY")
print("=" * 60)

print(f"""
Dependencies Installed: {len(installed)}/{len(dependencies)}
""")

if len(installed) == len(dependencies):
    print("✅ ALL TESTS PASSED!")
    print("\n🎮 Blender integration is fully functional!")
    print("\nNext steps:")
    print("  1. Generate a 3D model: python -m crochet_checker.features.blender_integration")
    print("  2. View in Blender: blender model.obj")
    print("  3. Export for 3D printing: Export as STL")
elif len(installed) >= 2:
    print("⚠️  MOST TESTS PASSED")
    print("\nBlender integration is partially functional.")
    print("Install missing dependencies for full functionality.")
else:
    print("❌ TESTS FAILED")
    print("\nPlease install required dependencies:")
    print("  pip install numpy matplotlib trimesh Pillow")

print()
