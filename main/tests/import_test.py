import unittest

class CanImportTests(unittest.TestCase):
  
  def testImportGdata(self):
    try:
      import gdata
      print "Can import gdata"
    except ImportError:
      print "Can't import gdata"
      self.failIf(True)

def main():
  unittest.main()

if __name__ == '__main__':
  main()
