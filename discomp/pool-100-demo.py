import os

from multiprocessing  import Pool

os.environ['DISCO_LOGIN_USER'] = ''
os.environ['DISCO_LOGIN_PASSWORD'] = ''

def tenCube(x):
    theCube = (x*10)**3
    print (theCube)
    return theCube

if __name__ == "__main__":
    # execute only if run as a script   
    p = Pool()
    results = p.map(tenCube, range(100))
    print(results)
