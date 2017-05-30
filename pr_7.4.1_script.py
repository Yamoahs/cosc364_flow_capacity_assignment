import subprocess
import itertools

START = 'ABCD'
TRAN = 'XYZ'
DEST = '1234'
demand_variables = set()
link_variables = set()
filename = 'pr_7.4.1.lp'

def demand_vol_dic_creater(demand_volume):

    variables = itertools.product(START, DEST)
    variables = list(map(''.join,list(variables)))
    demands = dict()
    r = [j for i in demand_volume for j in i]
    for key, value in zip(variables, r):
        demands[key] = value

    return demands

def build_cplex(demands, src_links, trn_links, restrictions):
    """"Function builds a Cplex .lp file based on string inputs"""
    lp_string = \
"""Minimize
r
Subject to
{}
{}
{}
{}
  r >= 0
End""".format(demands, src_links, trn_links, restrictions)
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

    # Home machine
    command = "/home/samuel/C_plex/cplex/bin/x86-64_linux/cplex"
    args = [
        "-c",
        "read /home/samuel/cosc364/cosc364_flow_capacity_assignment/" + filename,
        "optimize",
        'display solution variables -'
    ]

    proc = subprocess.Popen([command] + args,stdout=subprocess.PIPE)
    # proc2 = subprocess.Popen(["grep", "x12"], stdin=proc1.stdout, stdout=subprocess.PIPE)
    out,err = proc.communicate()

    result = out.decode("utf-8")
    return result

def demand_constraint(demands):

    demand_flows = []
    for src in START:
        for dst in DEST:
            eqn = []
            for trn in TRAN:
                part = src + trn + dst
                eqn.append(part)
                demand_variables.add("x{}".format(part))
            string = '  x{} + x{} + x{} = {}'.format(eqn[0], eqn[1], eqn[2], demands[str(src + dst)])
            demand_flows.append(string)

    demand_constraint_string = '\n'.join(demand_flows)
    return demand_constraint_string

def source_trans_links():
    """Function Generates the equations for the link demand constraints between
    source and transit nodes.
    The len of the equation will be the number of Destinations"""
    links = []
    for src in START:
        for trn in TRAN:
            eqn = []
            for dst in DEST:
                part = src + trn + dst
                eqn.append(part)
                link_variables.add('y{}'.format(src + trn))
            string = '  x{} + x{} + x{} + x{} - y{} <= 0'.format(eqn[0], eqn[1], \
                                                      eqn[2], eqn[3], src + trn)
            links.append(string)

    links_string = '\n'.join(links)
    return links_string

def trans_dest_links():
    """Function Generates the equations for the link demand constraints between
    transit and destination nodes.
    The len of the equation will be the number of Sources"""
    links = []
    for trn in TRAN:
        for dst in DEST:
            eqn = []
            for src in START:
                part = src + trn + dst
                eqn.append(part)
                link_variables.add('y{}'.format(trn + dst))
            string = '  x{} + x{} + x{} + x{} - y{} <= 0'.format(eqn[0], eqn[1], \
                                                      eqn[2], eqn[3], trn + dst)
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
    all_restrictions = link_capacity_string + '\n' + utilazation_string + \
                                                     '\n' + minimum_bound_string
    return all_restrictions


def main():
    demand_vol = [
    [40,30,20,10],
    [10,60,20,40],
    [20,20,20,20],
    [70,30,50,10]
    ]
    LINK_CAPACITY = 100


    demand = demand_vol_dic_creater(demand_vol)
    part_1 = demand_constraint(demand)
    part_2 = source_trans_links()
    part_3 = trans_dest_links()
    part_4 = restrictions(LINK_CAPACITY)
    build_cplex(part_1, part_2, part_3, part_4)
    print(run_cplex(filename))
    # print("demand variables:\n{}\nlink variables:\n{}".format(sorted(demand_variables),\
    #                                                             sorted(link_variables)))
    # print(sorted(variables))


if __name__ == '__main__':
    main()
