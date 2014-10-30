import numpy as np

class Initialization:

    def __init__(self,Step=0):
        self.Step = Step

class Termination:

    def __init__(self,MaxIter=1,Tols=[]):
        self.Tols = [MaxIter]
        self.Tols.append(Tols)

    def CheckTols(self,PermRequests,TempRequests):
        for tol in self.Tols[1]:
            if (not (tol[0] in PermRequests)) and (not (tol[0] in TempRequests)):
                self.Tols.remove(tol)
                print(`tol[0].func_name`+' cannot be used as a terminal condition because it is not tracked during the descent.')
        return self.Tols
    
    def IsTerminal(self,Record):
        if (Record.thisPermIndex>=self.Tols[0]):
            return True
        for tol in self.Tols[1]:
            if tol[0] in Record.TempStorage:
                if (Record.TempStorage[tol[0]][-1]<=tol[1]): return True
            else:
                if (Record.PermStorage[tol[0]][Record.thisPermIndex]<=tol[1]): return True
            
class Reporting:

    def __init__(self,Requests=[]):
        self.PermRequests = Requests

    def CheckRequests(Method,Domain):
        for req in self.PermRequests:
            inTempStorage = (req in Method.TempStorage)
            inDomainFunctions = False;
            req_str = req[0]
            if hasattr(req,'__self__'):
                inDomainFunctions = (req.self == Domain)
                req_str = req[0].func_name
            if not (inTempStorage or inDomainFunctions):
                self.PermRequests.remove(req)
                print(`req_str`+' cannot be used as a terminal condition because it is not tracked during the descent.')

class Miscellaneous:

    def __init__(self,Min=None):
        self.Min = Min

class DescentOptions:

    def __init__(self,Init=Initialization(),Term=Termination(),Repo=Reporting(),Misc=Miscellaneous()):
        self.Init = Init
        self.Term = Term
        self.Repo = Repo
        self.Misc = Misc

    def CheckOptions(self,Method,Domain):
        if not self.Misc.Min == None: Domain.Min = self.Misc.Min
        # check if requests are either tracked in tempstorage or are available as domain functions
        self.Term.Tols = self.Term.CheckTols(self.Repo.PermRequests,Method.TempStorage.keys())



