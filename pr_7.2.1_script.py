import subprocess
import matplotlib.pyplot as plt

def run_cplex(filename):
    """"Script for running Cplex based on .lp file input"""

    command = "/home/cosc/student/sya57/internet_tech_cosc364/labs/cplex/cplex/bin/x86-64_linux/cplex"
    args = [
        "-c",
        "read /home/cosc/student/sya57/internet_tech_cosc364/labs/" + filename,
        "optimize",
        'display solution variables -'
    ]

    proc1 = subprocess.Popen([command] + args,stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(["grep", "x12"], stdin=proc1.stdout, stdout=subprocess.PIPE)
    proc1.stdout.close()
    out,err = proc2.communicate()

    result = out.decode("utf-8").split()
    #No value for wanted variable
    if not result:
        return 0
    else:
        result = float(result[1])
        return result


def plot_results(x,y):
    """Function plots the result fromn the two lists using gnuplot"""
    plt.plot(x,y)
    plt.ylabel("h values")
    plt.xlabel("x12 optimal sol.")
    plt.show()


def main():
    """Main Function"""

    h_vals = []
    x12_vals = []
    current_h = 1.0
    filename = 'pr_7.2.1.lp'

    while current_h <= 19.1:
        f = open(filename, 'w')
        lp_string = \
"""Minimize
10 x12 + 5 x132
Subject to
  demand flow: x12 + x132 = {}
  capp1: x12 <= 10
  capp2: x132 <= 10
Bounds
0 <= x12
0 <= x132
End""".format(round(current_h, 1))

        f.write(lp_string)
        f.close()

        h_vals.append(round(current_h, 1))
        x12_vals.append(run_cplex(filename))
        current_h += 0.1

    print("h_vals:\n{}".format(h_vals))
    print("x12:\n{}".format(x12_vals))
    plot_results(h_vals, x12_vals)


if __name__ == '__main__':
    main()
