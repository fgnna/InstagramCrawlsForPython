import time 
print time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime(1472832229))

from distutils.core import setup  
import py2exe  
  
setup(console=["HelloPy2exe.py"])  
