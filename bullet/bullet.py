import clr

clr.AddReference("Interop.SolidEdge")
clr.AddReference("System.Runtime.InteropServices")

import SolidEdgeFramework as SEFramework
import SolidEdgePart as SEPart
import SolidEdgeConstants as SEConstants
import System.Runtime.InteropServices as SRI
# import SolidEdgeDraft as SEDraft

from settings2 import drillsize, stdthread
import sys


class Hole(object):
    """Access the propeties and methodes of holes in Solidedge."""

    def __init__(self, hole):
        self.hole = hole
        self.family = 'Simple'

    def extract_data(self):
        params = {"Standard": self.hole.Standard,
            "Sub Type": self.hole.SubType,
            "Size": self.hole.Size,
            "Fit": self.hole.Fit,
            "Hole Diameter": self.hole.HoleDiameter,
        }
        print(params)

    def inject(self, db):
        if db:
            self.hole.Standard = db.get("Standard",'')
            self.hole.SubType = db.get("Sub Type",'')
            self.hole.Size = db.get("Size", '')
            self.hole.Fit = db.get("Fit", '')
            self.hole.HoleDiameter = db.get("Hole Diameter",'')
            # self.hole.ThreadMinorDiameter = db.get("Internal Minor",None) #unique to threads
        else:
            print('[-] hole unchanged')

    def inspection(self):
        '''Display holes details.'''
        print('-------------------------------------')
        print('Name         : %s' %self.hole.Name)
        print('Family       : %s' %self.family)
        # print('Display      : %s' %self.hole.DisplayName) #same as Name
        # print('SystemName   : %s' %self.hole.SystemName) #same as Name
        print('=====================================')
        print('Standard     : %s' %self.hole.Standard)
        print('SubType      : %s' %self.hole.SubType)
        print('Size         : %s' %self.hole.Size)
        print('Fit          : %s' %self.hole.Fit)
        print('H.Diam       : %s' %self.hole.HoleDiameter)
        print('-------------------------------------')

    @staticmethod
    def convertor(distance):
        return distance*25.4/100 #inch -> meter

    def equivalence(self):
        if not self.hole.SubType:
            raise Exception('[-] SubType unknown')
        else:
            if self.hole.Standard == 'ANSI Metric - PT':
                print('[-] %s is already metric' %self.hole.Name)
            else:
                if self.hole.SubType == 'Drill Size':
                    sz = self.hole.Size #check for size
                    hole_data = drillsize.get('%s' %sz)#with this size check for the equivalence in metrical
                    return hole_data
                elif self.hole.SubType == 'Standard Thread':
                    sz = self.hole.Size #check for size
                    hole_data = stdthread.get('%s' %sz)#with this size check for the equivalence in metrical
                    return hole_data



class Threaded(Hole):

    def __init__(self, hole):
        super(Threaded, self).__init__(hole)
        self.family = 'Threaded'

    def inspection(self):
        super(Threaded, self).inspection()
        print('Th.Min.Diam  : %s' %self.hole.ThreadMinorDiameter)   #unique to threads
        print('Th.Nominal.Diam  : %s' %self.hole.ThreadNominalDiameter)   #unique to threads
        # if self.hole.ThreadDepth:
        #     print('Pitch  : %s' %self.hole.ThreadDepth)
        print('-------------------------------------')

    def inject(self, db):
        if db:
            self.hole.Standard = db.get("Standard",'')
            self.hole.SubType = db.get("Sub Type",'')
            self.hole.Size = db.get("Size", '')
            self.hole.Fit = db.get("Fit", '')
            self.hole.ThreadNominalDiameter = db.get("Nominal Diameter",'')
            self.hole.ThreadMinorDiameter = db.get("Internal Minor",None) #unique to threads
            # if self.hole.ThreadDepth:
            #     self.hole.ThreadDepth = db.get("Pitch", None)

        else:
            print('[-] Unchanged')




if __name__ == "__main__":
    # Connect to a running instance of Solid Edge
    objApplication = SRI.Marshal.GetActiveObject("SolidEdge.Application")
    # Get a reference to the active document
    objPart = objApplication.ActiveDocument
    print(objPart.Name) #partnumber
    # Get a reference to the variables collection
    holes = objPart.HoleDataCollection
    for hole in holes:
        o = Threaded(hole)
        # o = Hole(hole) #for simple hole
        o.inspection()
        # print(o.extract_data()) #return a dictionnary of holes data #debugging
        print('...')
        db = Threaded.equivalence(o)
        o.inject(db)
        o.inspection()
            print('Inch -> mm\n')
        # raw_input("\n(Press any key to exit ;)")