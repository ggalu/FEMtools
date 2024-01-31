# GCG 31 Jan 2024
#
# This program reads a mesh file produced by Gid and saves it into LS-Dyna .k format.

import sys

def read_gid(filename):

    print("... reading from file %s" % (filename))
    with open(filename, "r") as f:
        linecount = 0
        nodes = []
        elements = []
        section_nodes = section_elements = False
        for line in f.readlines():
            if linecount == 0:
                assert line.startswith("MESH dimension 3 ElemType Hexahedra Nnode 8"),\
                "expected in first line: MESH dimension 3 ElemType Hexahedra Nnode 8"

            if line.startswith("Coordinates"):
                section_nodes = True
            elif line.startswith("End Coordinates"):
                section_nodes = False
            elif line.startswith("Elements"):
                section_elements = True
            elif line.startswith("End Elements"):
                section_elements = False
            elif section_nodes == True:
                id, x, y, z = line.split()
                #print("NODE", id, x, y, z)
                nodes.append({"id": int(id), "x": float(x), "y": float(y), "z": float(z)})
            elif section_elements == True:
                id, n1, n2, n3, n4, n5, n6, n7, n8 = line.split()
                #print("ELEM ", id, n1, n2, n3, n4, n5, n6, n7, n8)
                elements.append({"id": int(id), "n1": int(n1), "n2": int(n2), "n3": int(n3),
                                 "n4": int(n4), "n5": int(n5), "n6": int(n6), "n7": int(n7), "n8": int(n8)})

            linecount += 1
        print("read %d lines from file %s" % (linecount, filename))            
        print("there are %d nodes and %d elements" % (len(nodes), len(elements)))
        print("---")

    return nodes, elements

def write_lsdyna(filename, nodes, elements, partID=1):

    print("... writing to file %s" % (filename))
    with open(filename, "w") as f:
        f.write("*KEYWORD\n")

        f.write("*NODE\n")
        count = 0
        for n in nodes:
            f.write("%d,%f,%f,%f,0,0\n" % (n["id"], n["x"], n["y"], n["z"]))
            count += 1
        print("... wrote %d nodes to LS-Dyna mesh file" % (count))

        
        f.write("*ELEMENT_SOLID\n")
        count = 0
        for e in elements:
            f.write("%d,%d," % (e["id"], partID))
            f.write("%d,%d,%d,%d,%d,%d,%d,%d\n" % (e["n1"], e["n2"], e["n3"], e["n4"], e["n5"], e["n6"], e["n7"], e["n8"]))
            count += 1
        print("... wrote %d elements to LS-Dyna mesh file" % (count))

        f.write("*END\n")


nodes, elements = read_gid(sys.argv[1])
write_lsdyna(sys.argv[2], nodes, elements)
