from sample_tools import RandomGenerator

# Setup data sources
# inputs
workspace = "M:/Projects/330A_Bainbridge/Layers/GDB/PythonTest.gdb"

testQuadrat = RandomGenerator(workspace)
testQuadrat.randQuadratGenerate(None, 'Grid', 26)