import arcpy,random

class RandomGenerator(object):
    """Generate Random Sample Features From a Habitat Type Grid"""
    def __init__(self, workspace):
        arcpy.env.workspace = workspace
        pass
    
    def randomNumber(self, cellList):
        """Return a random cell from a list"""
        # Check if input is a list
        try:
            assert isinstance(cellList, list)
            randSelect = random.choice(cellList)
            return randSelect
        except:
            print 'ERROR: INPUT DATA ARE NOT A LIST.'
    
    def selectGridLayerGenerate(self, randCellList, gridLayer, fcOut):
        """Using a grid and random cell list, make a new feature class."""
        print "Creating feature class: %s" % fcOut 
        # Create a new selection for the first value.
        arcpy.SelectLayerByAttribute_management(gridLayer,"NEW_SELECTION", '"PageNumber" = %s' % randCellList[0])
        # Add subsequent values to the existing selection
        for i in randCellList[1:]:
            arcpy.SelectLayerByAttribute_management(gridLayer,"ADD_TO_SELECTION", '"PageNumber" = %s' % i)
        # Export selected features to new feature class
        arcpy.CopyFeatures_management(gridLayer, fcOut)
        print "Finished creating feature class: %s" % fcOut 
    
    def randTransectGenerate(self, transectSeed, grid, HabType, outputFeatureClass):
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
            randomSelectCell = self.randomNumber(selectedPageNumbers)
            finalRandCells.append(randomSelectCell)
            print "Randomly Selected Cell: %s" % randomSelectCell
        print "Final Randomly Selected Cells: %s" % finalRandCells
        self.selectGridLayerGenerate(finalRandCells, gridLayer, outputFeatureClass)
    
    def randQuadratGenerate(self, HabTypeVal, grid, quadratCount, outputFeatureClass):
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
            randomSelectCell = self.randomNumber(selectedPageNumbers)
            finalRandCells.append(randomSelectCell)
            setFinalRandCells = list(set(finalRandCells))
            setCount = len(setFinalRandCells)
    
        print "Final set of Randomly Selected Cells: %s" % setFinalRandCells
        self.selectGridLayerGenerate(setFinalRandCells, gridLayer, outputFeatureClass)