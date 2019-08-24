import os

from multiprocessing  import Pool

# Set DISCO_LOGIN_USER and DISCO_LOGIN_PASSWORD environment variables before run

def tenCube(x):
    theCube = (x*10)**3
    print (theCube)
    return theCube
    
if __name__ == "__main__":
    # execute only if run as a script
    p = Pool()
    print("Send heavy calculation to cloud")
    results = p.map(tenCube, range(10))

    print ("Get results as a list of real python objects and continue working")

    [print('result for {0} is {1}'.format(n, result)) for n, result in enumerate(results)]

