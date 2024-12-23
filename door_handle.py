from build123d import *
from ocp_vscode import show_object


# CAD file for a replacement knob for the window roller in a 1981 Dodge Ram Campervan.

# Constants
# Knob Dimensions
KNOB_DIAMETER = 35.0
KNOB_HEIGHT = 20.0

# Screw and Hole Dimensions
SCREW_HOLE_DIAMETER = 3.7  # Approx diameter for a #6 screw
SCREW_HEAD_DIAMETER = 8.0
INSERTION_DEPTH =35.0

# Backing Dimensions
BACKING_FLANGE_DIAMETER = 15.0
BACKING_FLANGE_THICKNESS = 5.0
HEX_NUT_FLAT_TO_FLAT = 10.0  # Approx size for #6 nut
HEX_NUT_DEPTH = 2.5  # Depth of the hex pocket

# Fillet Radius
FILLET_RADIUS = 2.0

with BuildPart() as knob:
    # 1) Create the main knob
    Cylinder(radius=KNOB_DIAMETER / 2, height=KNOB_HEIGHT)
    fillet(knob.edges().filter_by(GeomType.CIRCLE), radius=FILLET_RADIUS)

    # Cut screw head hole
    with Locations((0, 0, KNOB_HEIGHT / 2.0)):
        Cylinder(
            radius=SCREW_HEAD_DIAMETER / 2.0, height=INSERTION_DEPTH, mode=Mode.SUBTRACT
        )
    # Cut screw shaft hole
    with Locations((0, 0, 0)):
        Cylinder(
            radius=SCREW_HOLE_DIAMETER / 2.0, height=KNOB_HEIGHT, mode=Mode.SUBTRACT
        )
# Create the backing
with BuildPart() as backing:
    # Create the flange
    Cylinder(radius=BACKING_FLANGE_DIAMETER / 2.0, height=BACKING_FLANGE_THICKNESS)
    # Apply fillet to the top and bottom edges
    fillet(backing.edges().filter_by(GeomType.CIRCLE), radius=FILLET_RADIUS)
    # Add a through-hole for the screw shaft
    with Locations((0, 0, 0)):
        Cylinder(
            radius=SCREW_HOLE_DIAMETER / 2.0,
            height=BACKING_FLANGE_THICKNESS,
            mode=Mode.SUBTRACT,
        )
    # Add a sketch for the hex pocket
    with BuildSketch() as hex_pocket:
        RegularPolygon(HEX_NUT_FLAT_TO_FLAT / 2.0, 6)  # Hexagon
    # Extrude the sketch to create the pocket
    with Locations((0, 0, -HEX_NUT_DEPTH / 2.0)):
        extrude(amount=HEX_NUT_DEPTH, mode=Mode.SUBTRACT)

# Create a Compound to combine knob and backing
compound = Compound(
    [
        knob.part.located(
            Location(Vector(0, 0, KNOB_HEIGHT / 2.0))
        ),  # Position the knob
        backing.part.located(
            Location(
                Vector(0, 0, -(KNOB_HEIGHT / 2.0 + BACKING_FLANGE_THICKNESS)),
            )
        ),
    ]
)

# Display the Compound
show_object(compound, name="compound_assembly")

export_stl(knob.part, "knob.stl")
export_stl(backing.part, "backing.stl")