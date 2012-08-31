from sample_tools import RandomGenerator

# Setup data sources
# inputs
workspace = "M:/Projects/330A_Bainbridge/Layers/GDB/Strawberry_Plant_Park.gdb"

testQuadrat = RandomGenerator(workspace)

testQuadrat.randQuadratGenerate('Marsh', 'Grid', 30, 'PythonMethod_FC')