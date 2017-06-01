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
source_link_variables = set()
transit_link_variables = set()
filename = 'assig.lp'
#/END OF GLOBAL VARIABLES
################################################################################
# LP Variables:
# c = Capacity on a link between source and transit
# d = Capacity on a link between transit and destination
# u = Binary Auxilary variables
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
                source_link_variables.add('y{}'.format(src + trn))
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
                transit_link_variables.add('y{}'.format(trn + dst))
            string = '  x' + ' + x'.join(eqn) + " - y{} = 0".format(trn+ dst)
            links.append(string)

    links_string = '\n'.join(links)
    return links_string

def restrictions(tran):
    """Fuction generates the variable restrictions for the .lp file"""
    restrictions = []
    utilazation_restrictions = []
    minimum_bound = []
    # demand_restrictions = []
    #source_link_variables
    for variable in sorted(source_link_variables):
        # eqn = '  {} <= c{}'.format(variable, variable[1:])
        eqn = '  {} - c{} = 0'.format(variable, variable[1:])
        restrictions.append(eqn)
        eqn = '  {} >= 0'.format(variable)
        minimum_bound.append(eqn)

    #transit_link_variables
    for variable in sorted(transit_link_variables):
        # eqn = '  {} <= d{}'.format(variable, variable[1:])
        eqn = '  {} - d{} = 0'.format(variable, variable[1:])
        restrictions.append(eqn)
        eqn = '  {} >= 0'.format(variable)
        minimum_bound.append(eqn)

    #demand restrictions variables
    for variable in sorted(demand_variables):
        eqn = '  {} >= 0'.format(variable)
        minimum_bound.append(eqn)

    # #r values
    all_variables = sorted(source_link_variables.union(transit_link_variables.union(demand_variables)))
    yyy = []
    for trn in tran:
        xxx = []
        for var in all_variables:
            if trn in var:
                xxx.append(var)
            eqn = '  ' + ' + '.join(xxx) + " - r <= 0"
        # print(eqn)
        utilazation_restrictions.append(eqn)

    link_capacity_string = '\n'.join(restrictions)
    utilazation_string = '\n'.join(utilazation_restrictions)
    minimum_bound_string = '\n'.join(minimum_bound)
    all_restrictions = link_capacity_string + '\n' + utilazation_string
    return all_restrictions, minimum_bound_string

def binaries(start, tran, dest, demand_dict):
    #binary path equation formulation that will sum to total paths used (3)
    binary_variables = []
    binaries_path = []
    for src in start:
        for dst in dest:
            eqn = []
            for trn in tran:
                part = src + trn + dst
                eqn.append(part)
                binary_variables.append('  u' + part)
            string = '  u' + ' + u'.join(eqn) + " = 3" #3 set by assignmet spec
            binaries_path.append(string)
    #formualation whether a path is used to transport demand Volume
    binary_true = []

    for var in sorted(demand_variables):
        key = var[1:3] + var[5:7]
        string = '  3 {} - {} u{} = 0'.format(var, demand_dict[key], var[1:])
        binary_true.append(string)

    binaries_path_string = '\n'.join(binaries_path)
    binary_true_string = '\n'.join(binary_true)
    binary_variables_string = '\n'.join(binary_variables)
    return binaries_path_string, binary_true_string, binary_variables_string

def build_cplex(demands, src_links, trn_links, restrictions, binaries):
    """"Function builds a Cplex .lp file based on string inputs"""
    lp_string = \
"""Minimize
r
Subject to
{}
{}
{}
{}
{}
{}
Bounds
{}
  r >= 0
Binary
{}
End""".format(demands, src_links, trn_links, restrictions[0], binaries[0], binaries[1], restrictions[1], binaries[2])
    f = open(filename, 'w')
    f.write(lp_string)
    f.close()

def run_cplex(filename):
    """"Script for building and running Cplex based on .lp file input"""
    # Lab machines (comment out either these set or the other)
    command = "/home/cosc/student/sya57/internet_tech_cosc364/labs/cplex/cplex/bin/x86-64_linux/cplex"
    args = [
        "-c",
        "read /home/cosc/student/sya57/internet_tech_cosc364/assig_2/" + filename,
        "optimize",
        'display solution variables -'
    ]

    # # Home machine
    # command = "/home/samuel/C_plex/cplex/bin/x86-64_linux/cplex"
    # args = [
    #     "-c",
    #     "read /home/samuel/cosc364/cosc364_flow_capacity_assignment/" + filename,
    #     "optimize",
    #     'display solution variables -'
    # ]

    proc = subprocess.Popen([command] + args,stdout=subprocess.PIPE)
    # proc2 = subprocess.Popen(["grep", "x12"], stdin=proc1.stdout, stdout=subprocess.PIPE)
    out,err = proc.communicate()

    result = out.decode("utf-8")
    return result

def main():
    start, tran, dest = set_nodes()
    demand_dict = demand_vol_dic_creater(start, dest)
    part_1 = demand_constraint(start, tran, dest, demand_dict)
    part_2 = source_trans_links(start, tran, dest)
    part_3 = trans_dest_links(start, tran, dest)
    part_4 = restrictions(tran)
    part_5 = binaries(start, tran, dest, demand_dict)
    build_cplex(part_1, part_2, part_3, part_4, part_5)
    print(run_cplex(filename))
    # print(part_1)
    # print(part_2)
    # print(part_3)
    # print(part_4[0])
    # print(part_4[1])
    # print(part_5[0])
    # print(part_5[1])
    # print(part_5[2])
    # print(sorted(source_link_variables))
    # print(sorted(transit_link_variables))
    # print(sorted(demand_variables))
    # print(demand_dict.items())
    # print(sorted(link_variables))


if __name__ == '__main__':
    main()
