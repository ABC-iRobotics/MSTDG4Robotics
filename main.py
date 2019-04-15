import sys
import VrepMeshDrawer as vdrawer

elementsCount = 30

def main():
    drawer = vdrawer.VrepMeshDrawer()
    for i in range(elementsCount):
        drawer.DrawMesh()
    success, objectIds = drawer.GetObjects('Shape', elementsCount)
    if success is not -1:
        drawer.GetObjectProperties('Shape', objectIds)
    else:
        print('Error while get inserted object shapes from simulation.')
    return 0

if __name__ == "__main__":
    main()