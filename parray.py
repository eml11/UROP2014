import numpy as np

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
    #self.TIME = map(float, f.readline().split(":")[1].split())
    self.CELLVOL = np.array(map(float, f.readline().split("=")[1].split()))

    f.readline()

    datstr = np.array(map(lambda x: x.split(), f.readlines()))
    self.TIME = datstr[:,0]

    datstr = datstr[:,1:]
    data = []
    for line in datstr:
      data += [map(float, line)]

    self.data = np.array(data)
    
    f.close()

class Parray(ParrayReader_Lagrange,ParrayReader_Euler):
  
  def __init__(self,filename,rw,TYPE="EULER"):
    if (rw == "r" and TYPE == "LAGRANGE"):
      self.read_lagrange(filename)
    elif (rw == "r" and TYPE == "EULER"):
      self.read_euler(filename)

  def read_lagrange(self,filename):
    ParrayReader_Lagrange.read(self,filename)

  def read_euler(self,filename):
    ParrayReader_Euler.read(self,filename)
 
