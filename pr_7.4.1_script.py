import itertools

START = 'ABCD'
TRAN = 'XYZ'
DEST = '1234'

def demand_vol_dic_creater(demand_volume):

    variables = itertools.product(START, DEST)
    variables = list(map(''.join,list(variables)))
    demands = dict()
    r = [j for i in demand_volume for j in i]
    for key, value in zip(variables, r):
        demands[key] = value

    return demands

def run_cplex():
    pass


def demand_constraint(demands):

    demand_flows = []
    for src in START:
        for dst in DEST:
            eqn = []
            for trn in TRAN:
                part = src + trn + dst
                eqn.append(part)
            string = 'x{} + x{} + x{} = {}'.format(eqn[0], eqn[1], eqn[2], demands[str(src + dst)])
            demand_flows.append(string)

    demand_constraint_string = '\n'.join(demand_flows)
    return demand_constraint_string


def main():
    demand_vol = [
    [40,30,20,10],
    [10,60,20,40],
    [20,20,20,20],
    [70,30,50,10]
    ]


    demand = demand_vol_dic_creater(demand_vol)
    print(demand_constraint(demand))
    # print(demand)


if __name__ == '__main__':
    main()
