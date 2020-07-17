import csv, time
import matplotlib.pyplot as plt


timestr = time.strftime("%Y%m%d_%H%M%S")
def plotError():
    errors = []
    params = []
    with open("data/error_xatol.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for lines in csv_reader:
          param = lines[1].split("[")[1].split("]")[0] 
          errors.append(float(lines[0]))
          params.append(float(param))
    errors = errors[::2]  #every other term
    params = params[::2]
    x = [i+1 for i in range(len(errors))]
    plt.plot(x, errors)
    num = 2*(len(errors)) -  1
    plt.ylabel("Error")
    plt.xlabel("Iteration")
    plt.title("Initial [v0, T]: " + str(params[0]) + " Final [v0,T]: " + str(params[-1])+"\n Iterations: " + str(num))
    for i, txt in enumerate(params):
        plt.annotate(txt, (x[i], errors[i]))
  #  plt.savefig("figures/error_latest_"+timestr+".png")
    plt.show()

plotError()
