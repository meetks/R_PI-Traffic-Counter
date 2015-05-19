import numpy as np
import pylab as pl

try:
   fp = open("log", "r")
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    raise
except ValueError:
    print "Could not convert data to an integer."
    raise
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise

data = []
time = []
for i in fp :
    val = i.split(" ")
    valsensor =  int(val[1])
    timeval = float(val[0])
    data.append(valsensor)
    time.append(timeval)



pl.plot(np.array(time), np.array(map(float,data)))
pl.show()

diffdata = np.diff(data)
nptime = np.array(time)

axelcount = 0
count = 0
for i in diffdata :
  
  if i > 0 :
    axelcount = axelcount + 1
  else:
    diffdata[count] = 0
    
  count = count + 1

print axelcount

pl.plot(nptime[:-1], np.array(map(float,diffdata)))
pl.show()
