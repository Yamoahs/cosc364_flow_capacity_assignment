import itertools

def demand_vol_dic_creater(demand_volume):
    start = 'ABCD'
    dest = '1234'
    variables = itertools.product(start, dest)
    variables = list(map(''.join,list(variables)))
    print(variables)
    demands = {(var for var in variables): j for i in demand_volume for j in i}


    total_sources = len(demand_volume)
    if total_sources:
        total_destinations = len(demand_volume[0])
    return demands




def main():
    demand_vol = [
    [40,30,20,10],
    [10,60,20,40],
    [20,20,20,20],
    [70,30,50,10]
    ]

    d_vol = {'A1'}
    print(demand_vol_dic_creater(demand_vol))


if __name__ == '__main__':
    main()
