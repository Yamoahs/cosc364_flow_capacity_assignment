################################################################################
# File: assig2.py
# Author: sy, jl
# Date created: 30/05/17
# Date Modified: 30/05/17
################################################################################
import subprocess
import itertools
################################################################################
GLOBAL VARIABLES:
demand_variables = set()
link_variables = set()
#/END OF GLOBAL VARIABLES
################################################################################

def set_nodes():
    """Take the user input of the number of Sources, Transits and Destinations
    """
    no_sources = int(input("Number of Sources: "))
    no_transits = int(input("Number of Transits: "))
    no_destinations = int(input("Number of Destinations: "))

    #create source variables
    start = []
    for var in range(1, no_sources + 1):
        start.append('S{}'.format(var))

    #create transit variables
    transit = []
    for var in range(1, no_transits + 1):
        transit.append('T{}'.format(var))

    #create destination variables
    destination = []
    for var in range(1,no_destinations + 1):
        destination.append('D{}'.format(var))

    return start, transit, destination

def demand_vol_dic_creater(start, dest):

    variables = itertools.product(start, dest)
    variables = list(map(''.join,list(variables)))
    demands = dict()
    #A variable will represent the demand Volume
    for item in variables:
        demands[item] = 'a{}'.format(item)

    return demands

def source_trans_links(start, tran, dest):
    """Function Generates the equations for the link demand constraints between
    source and transit nodes.
    The len of the equation will be the number of Destinations"""
    links = []
    for src in start:
        for trn in tran:
            eqn = []
            for dst in dest:
                part = src + trn + dst
                eqn.append(part)
                link_variables.add('y{}'.format(src + trn))
            string = '  x{} + x{} + x{} + x{} - y{} = 0'.format(eqn[0], eqn[1], \
                                                      eqn[2], eqn[3], src + trn)
            links.append(string)

    links_string = '\n'.join(links)
    return links_string




def main():
    start, tran, dest = set_nodes()
    demands = demand_vol_dic_creater(start, dest)
    print(demands)


if __name__ == '__main__':
    main()
