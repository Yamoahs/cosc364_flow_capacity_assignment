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

def format_output(demands):

    for src in START:
        for dst in DEST:
            # eqn = ''
            # for trn in TRAN:
                # part = src + trn + dst
                # print(part)
            eqn = src + TRAN[0] + dst
            for trn in TRAN[1:]:
                part = src + trn + dst
                eqn = eqn + ' + ' + part + ' = {}'.format(demands[str(src + dst)])
                # eqn = part + '+' + eqn
        # eqn += part#str(src + trn + dst + '=' )#+ demands[src+dst])

            print(eqn)


def main():
    demand_vol = [
    [40,30,20,10],
    [10,60,20,40],
    [20,20,20,20],
    [70,30,50,10]
    ]


    demand = demand_vol_dic_creater(demand_vol)
    format_output(demand)
    print(demand)


if __name__ == '__main__':
    main()
