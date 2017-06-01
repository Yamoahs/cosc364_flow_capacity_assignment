################################################################################
# File: assig2.py
# Author: sy, jl
# Date created: 30/05/17
# Date Modified: 30/05/17
################################################################################
import subprocess
import itertools
################################################################################
# GLOBAL VARIABLES:
demand_variables = set()
link_variables = set()
#/END OF GLOBAL VARIABLES
################################################################################
# LP Variables:
# c = Capacity on a link between source and transit
# d = Capacity on a link between transit and destination
#/END OF LP VARIABLES
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
    for item in sorted(variables):
        demands[item] = '{}'.format(int(item[1]) + int(item[3]))

    return demands

def demand_constraint(start, tran, dest, demand_dict):
    demand_flows = []
    for src in start:
        for dst in dest:
            eqn = []
            for trn in tran:
                part = src + trn + dst
                eqn.append(part)
                demand_variables.add("x{}".format(part))
            string = '  x' + ' + x'.join(eqn) + " = {}".format(demand_dict[str(src + dst)])
            # string = '  x{} + x{} + x{} = {}'.format(eqn[0], eqn[1], eqn[2], demand_dict[str(src + dst)])
            demand_flows.append(string)

    demand_constraint_string = '\n'.join(demand_flows)
    return demand_constraint_string

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
            string = '  x' + ' + x'.join(eqn) + " - y{} = 0".format(src + trn)
            links.append(string)

    links_string = '\n'.join(links)
    return links_string

def trans_dest_links(start, tran, dest):
    """Function Generates the equations for the link demand constraints between
    transit and destination nodes.
    The len of the equation will be the number of Sources"""
    links = []
    for trn in tran:
        for dst in dest:
            eqn = []
            for src in start:
                part = src + trn + dst
                eqn.append(part)
                link_variables.add('y{}'.format(trn + dst))
            string = '  x' + ' + x'.join(eqn) + " - y{} = 0".format(trn+ dst)
            links.append(string)

    links_string = '\n'.join(links)
    return links_string

def restrictions(capacity):
    """Fuction generates the variable restrictions for the .lp file"""
    restrictions = []
    utilazation_restrictions = []
    minimum_bound = []
    # demand_restrictions = []
    #Link Capacity
    for variable in sorted(link_variables):
        eqn = '  {} <= {}'.format(variable, capacity)
        restrictions.append(eqn)
        # eqn = '  {}/{} <= r'.format(variable, capacity)
        # utilazation_restrictions.append(eqn)
        eqn = '  {} >= 0'.format(variable)
        minimum_bound.append(eqn)

    #demand restrictions
    for variable in sorted(demand_variables):
        eqn = '  {} >= 0'.format(variable)
        minimum_bound.append(eqn)

    #r values
    all_variables = sorted(link_variables.union(demand_variables))
    # print(all_variables)
    yyy = []
    for trn in TRAN:
        xxx = []
        for var in all_variables:
            if trn in var:
                xxx.append(var)
            eqn = '  ' + ' + '.join(xxx) + " - {}r <= 0".format(capacity)
        # print(eqn)
        utilazation_restrictions.append(eqn)



    link_capacity_string = '\n'.join(restrictions)
    utilazation_string = '\n'.join(utilazation_restrictions)
    minimum_bound_string = '\n'.join(minimum_bound)
    all_restrictions = link_capacity_string + '\n' + utilazation_string
    return all_restrictions, minimum_bound_string

def main():
    start, tran, dest = set_nodes()
    demand_dict = demand_vol_dic_creater(start, dest)
    part_1 = demand_constraint(start, tran, dest, demand_dict)
    part_2 = source_trans_links(start, tran, dest)
    part_3 = trans_dest_links(start, tran, dest)
    print(part_1)
    print(part_2)
    print(part_3)
    # print(demand_dict)
    # print(sorted(link_variables))
    # print(start, dest)
    # for i in start:
    #     print(int(i[1]))


if __name__ == '__main__':
    main()
