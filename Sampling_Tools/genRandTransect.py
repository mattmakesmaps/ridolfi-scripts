"""
# genRandTransect.py
# Date: 120828
# Contact: matt@ridolfi.com
#
# Description: Create feature classes for randomly selected sampling features.
#
# Requires a grid generated using the, 'Grid Index Features' tool.
#
# For riparian transects, this tool relies upon 'seed lines' a feature class
# containing polyline features perpendicular to the sampaling baseline at pre-
# determined intervals.
# 
# For marsh quadrats, this tool relies on the value of an attribute in the grid,
# 'HabType' that contains habitat values of interest (e.g. 'Marsh').
"""

import arcpy,random

# Setup data sources
# inputs
arcpy.env.workspace = "M:/Projects/330A_Bainbridge/Layers/GDB/Strawberry_Plant_Park.gdb"
transectSeed = u'random_transect_seed'
grid = u'Grid'
quadratHabTypeVal = 'Marsh'
transectHabTypeVal = 'Riparian'
quadratsRequired = 20
# outputs
finalTransectCellFC = 'transect_cells'
finalQuadratCellFC = 'quadrat_cells'

def randomNumber(cellList):
    """Return a random cell from a list"""
    # Check if input is a list
    try:
        assert isinstance(cellList, list)
        randSelect = random.choice(cellList)
        return randSelect
    except:
        print 'ERROR: INPUT DATA ARE NOT A LIST.'

def selectGridLayerGenerate(randCellList, gridLayer, fcOut):
    """Using a grid and random cell list, make a new feature class."""
    print "Creating feature class: %s" % fcOut 
    # Create a new selection for the first value.
    arcpy.SelectLayerByAttribute_management(gridLayer,"NEW_SELECTION", '"PageNumber" = %s' % randCellList[0])
    # Add subsequent values to the existing selection
    for i in randCellList[1:]:
        arcpy.SelectLayerByAttribute_management(gridLayer,"ADD_TO_SELECTION", '"PageNumber" = %s' % i)
    # Export selected features to new feature class
    arcpy.CopyFeatures_management(gridLayer, fcOut)

def randTransectGenerate(transectSeed, grid, HabType):
    """From seed transects and a grid, generate randomly selected cells."""
    print "Generating %s transects." % HabType
    # Convert feature classes to layers
    seedLayer = transectSeed + "_TransectSeed_lyr"
    arcpy.MakeFeatureLayer_management(transectSeed, seedLayer)
    gridLayer = grid + "_Transect_lyr"
    arcpy.MakeFeatureLayer_management(grid, gridLayer)

    # Create search cursor on FC 
    rows = arcpy.SearchCursor(seedLayer,"","","OBJECTID","")
    finalRandCells = []

    # Loop through each transect seed based on OBJECTID.
    for row in rows:
        whereClauseOID = '"OBJECTID" = %s' % row.OBJECTID
        whereClauseHabType = '"HabType" = \'%s\'' % HabType 
        print "Current Value: %s" % whereClauseOID

        # Select individual seeds based on OBJECTID
        arcpy.SelectLayerByAttribute_management(seedLayer,"NEW_SELECTION", whereClauseOID)
        arcpy.SelectLayerByLocation_management(gridLayer,"INTERSECT", seedLayer, "", "NEW_SELECTION")
        arcpy.SelectLayerByAttribute_management(gridLayer,"SUBSET_SELECTION", whereClauseHabType)

        # Create a list of the intersected page numbers
        selectedCells = arcpy.SearchCursor(gridLayer,"","","PageNumber","")
        selectedPageNumbers = []
        for cell in selectedCells:
            selectedPageNumbers.append(cell.PageNumber)
        print "Intersected Cells: %s" % selectedPageNumbers

        # Randomly select an intersected cell, append to final list
        randomSelectCell = randomNumber(selectedPageNumbers)
        finalRandCells.append(randomSelectCell)
        print "Randomly Selected Cell: %s" % randomSelectCell
    print "Final Randomly Selected Cells: %s" % finalRandCells
    selectGridLayerGenerate(finalRandCells, gridLayer, finalTransectCellFC)

def randQuadratGenerate(HabTypeVal, grid, quadratCount):
    """For A Specific Habitat Type, Generate a User-Defined Number of Random Quadrats."""
    print "Generating %d randomly selected %s quadrats" % (quadratCount, HabTypeVal) 
    # Create working layers
    gridLayer = grid + "_Quadrat_lyr"
    arcpy.MakeFeatureLayer_management(grid, gridLayer)

    # Select Based on HabType Value of Interest
    whereClause = '"HabType" = \'%s\'' % HabTypeVal
    arcpy.SelectLayerByAttribute_management(gridLayer,"NEW_SELECTION", whereClause)

    # Create a list of selected cells
    selectedCells = arcpy.SearchCursor(gridLayer,"","","PageNumber","")
    selectedPageNumbers = []
    for cell in selectedCells:
        selectedPageNumbers.append(cell.PageNumber)

    # Random Cell Generate for Desired Range
    finalRandCells = []
    setCount = 0
    while setCount < quadratCount:
        randomSelectCell = randomNumber(selectedPageNumbers)
        finalRandCells.append(randomSelectCell)
        setFinalRandCells = list(set(finalRandCells))
        setCount = len(setFinalRandCells)

    print "Final set of Randomly Selected Cells: %s" % setFinalRandCells
    selectGridLayerGenerate(setFinalRandCells, gridLayer, finalQuadratCellFC)

randTransectGenerate(transectSeed, grid, transectHabTypeVal)
#randQuadratGenerate(quadratHabTypeVal, grid, quadratsRequired)
