import itertools

START = 'ABCD'
TRAN = 'XYZ'
DEST = '1234'
demand_variables = set()
link_variables = set()

def demand_vol_dic_creater(demand_volume):

    variables = itertools.product(START, DEST)
    variables = list(map(''.join,list(variables)))
    demands = dict()
    r = [j for i in demand_volume for j in i]
    for key, value in zip(variables, r):
        demands[key] = value

    return demands

def run_cplex(demands, src_links, trn_links, restrictions):
    """"Script for building and running Cplex based on .lp file input"""

def demand_constraint(demands):

    demand_flows = []
    for src in START:
        for dst in DEST:
            eqn = []
            for trn in TRAN:
                part = src + trn + dst
                eqn.append(part)
                demand_variables.add("x{}".format(part))
            string = 'x{} + x{} + x{} = {}'.format(eqn[0], eqn[1], eqn[2], demands[str(src + dst)])
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
            string = 'x{} + x{} + x{} + x{} = y{}'.format(eqn[0], eqn[1], \
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
            string = 'x{} + x{} + x{} + x{} = y{}'.format(eqn[0], eqn[1], \
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
        eqn = '{} <= {}'.format(variable, capacity)
        restrictions.append(eqn)
        eqn = '{} <= {}r'.format(variable, capacity)
        utilazation_restrictions.append(eqn)
        eqn = '{} >= 0'.format(variable)
        minimum_bound.append(eqn)

    #demand restrictions
    for variable in sorted(demand_variables):
        eqn = '{} >= 0'.format(variable)
        minimum_bound.append(eqn)


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
    run_cplex(part_1, part_2, part_3, part_4)
    # print("demand variables:\n{}\nlink variables:\n{}".format(sorted(demand_variables),\
                                                                # sorted(link_variables)))
    # print(sorted(variables))


if __name__ == '__main__':
    main()
