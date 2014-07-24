import numpy as np

##Reader for Probe Arrays with
#PARRAY_T = LAGRANGE. reads in
#one or more tracer files 
class ParrayReader_Lagrange( object ):

  filename = None
  PARRAY_V = None
  PROBE_N = None
  PROBE_H = None
  TIME = None  

  Var = None

  data = None

  def read( self, filename ):
    self.filename = filename
    f = open( filename, "r" )

    self.PARRAY_V = int(f.readline().split("=")[1])
    self.PROBE_N = int(f.readline().split("=")[1])


    self.PROBE_H = np.array(map(int, f.readline().split("=")[1].split()))
    self.TIME = np.array(map(float, f.readline().split(":")[1].split()))

    self.Var = filename[-7:-4]

    datstr = map(lambda x: x.split(), f.readlines())[:,1:]
    data = []
    for line in datstr:
      data += [map(float, line)]

    self.data = np.array(data)

    f.close()

  def readFields( self, filelist ):
    self.filename = filelist
   
    self.Var = []
    self.PARRAY_V = []
    self.PROBE_N = []
    self.PROBE_H = []
    self.TIME = []
    self.data = []

    for filename in filelist:
      f = open( filename, "r" )

      self.PARRAY_V += [int(f.readline().split("=")[1])]
      self.PROBE_N += [int(f.readline().split("=")[1])]


      self.PROBE_H += [np.array(map(int, f.readline().split("=")[1].split()))]
      self.TIME += [np.array(map(float, f.readline().split(":")[1].split()))]

      self.Var += [filename[-7:-4]]

      datstr = map(lambda x: x.split(), f.readlines())[:,1:]
      data = []
      for line in datstr:
        data += [map(float, line)]

      self.data += [np.array(data)]

      f.close()

##Reader for Probe Arrays with
#PARRAY_T = EULER. reads in
#one or more cell Probe files
class ParrayReader_Euler( object):

  filename = None
  PARRAY_V = None
  PROBE_N = None
  PROBE_H = None
  TIME = None
  CELLVOL = None

  Var = None

  data = None

  def read( self, filename ):
    self.filename = filename
    f = open( filename, "r" )

    self.Var = f.readline().split("=")[1].strip()
    
    self.PARRAY_V = int(f.readline().split("=")[1])
    self.PROBE_N = int(f.readline().split("=")[1])

    
    self.PROBE_H = np.array(map(int, f.readline().split("=")[1].split()))
    self.PROBE_ICOORD = np.array(map(float, f.readline().split("=")[1].split()))
    
    self.CELLVOL = np.array(map(float, f.readline().split("=")[1].split()))

    f.readline()

    datstr = np.array(map(lambda x: x.split(), f.readlines()))
    self.TIME = np.array(map(float, datstr[:,0]))

    datstr = datstr[:,1:]
    data = []
    for line in datstr:
      data += [map(float, line)]

    self.data = np.array(data)
    
    f.close()

  def readFields( self, filelist ):
    self.filename = filelist
    
    self.Var = []
    self.PARRAY_V = []
    self.PROBE_N = []
    self.PROBE_H = []
    self.PROBE_ICOORD = []
    self.CELLVOL = []
    self.TIME = []
    self.data = []

    for filename in filelist:
      f = open( filename, "r" )

      self.Var += [f.readline().split("=")[1].strip()]

      self.PARRAY_V += [int(f.readline().split("=")[1])]
      self.PROBE_N += [int(f.readline().split("=")[1])]


      self.PROBE_H += [np.array(map(int, f.readline().split("=")[1].split()))]
      self.PROBE_ICOORD += [np.array(map(float, f.readline().split("=")[1].split()))]
      
      self.CELLVOL += [np.array(map(float, f.readline().split("=")[1].split()))]

      f.readline()

      datstr = np.array(map(lambda x: x.split(), f.readlines()))
      self.TIME += [datstr[:,0]]

      datstr = datstr[:,1:]
      data = []
      for line in datstr:
        data += [map(float, line)]

      self.data = [np.array(data)]
    
      f.close()

##Main Probe array class
#for reading probe array outputs
#can read several fields to same
#array
class Parray(ParrayReader_Lagrange,ParrayReader_Euler):

  def __init__(self,FILE=None,FILELIST=[],rw,TYPE="EULER",FIELDS=False):
    if FILE != None:
      if (rw == "r" and TYPE == "LAGRANGE" and FIELDS==False):
        self.read_lagrange(FILE)
      elif (rw == "r" and TYPE == "EULER" and FIELDS==False):
        self.read_euler(FILE)
    elif len(FILELIST) > 0:
      if (rw == "r" and TYPE == "LAGRANGE" and FIELDS==False):
        self.read_lagrange_fields(FILELIST)
      elif (rw == "r" and TYPE == "EULER" and FIELDS==False):
        self.read_euler_fields(FILELIST) 

  def read_lagrange(self,filename):
    ParrayReader_Lagrange.read(self,filename)

  def read_lagrange_fields(self,filename):
    ParrayReader_Lagrange.readFields(self,filename)

  def read_euler(self,filename):
    ParrayReader_Euler.read(self,filename)

  def read_euler_fields(self,filename):
    ParrayReader_Euler.readFields(self,filename) 
