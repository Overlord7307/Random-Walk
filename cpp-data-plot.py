import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df1 = pd.read_csv("second-moment-data_cpp.csv")
df2 = pd.read_csv("second-moment-data_python.csv")


plt.figure(figsize=(16, 9))
plt.plot(df1["Time"], df1["SecondMoment"], marker='o', linestyle='-', color='#000080', label='C++ Data')
plt.plot(df1["Time"], df1["SecondMoment"], linestyle='-', color='#FF7F0E', label='Python Data')

plt.xlabel(r"Total Number of Steps ($t$)", fontsize=12)
plt.ylabel(r"Second Moment of Final Position $\langle x^2 \rangle$", fontsize=12)
plt.title("Second Moment vs. Time", fontsize=14)

plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)
plt.savefig('plots\\second-moment-vs-t_cpp-vs-python.png', dpi=300, bbox_inches='tight')
plt.show()