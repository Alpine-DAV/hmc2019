import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dfs = {}
dfs['construct_bvh_timing'] = pd.read_csv('./data/construct_bvh_timing.csv', index_col=0)
dfs['locate_stats'] = pd.read_csv('./data/locate_stats.csv', index_col=1, skiprows=lambda x: x != 0 and x%100 !=2)
dfs['locate_timing'] = pd.read_csv('./data/locate_timing.csv', index_col=0)

cuda_fixed_labels = ["cuda_fixed_000", "cuda_fixed_001", "cuda_fixed_004",
                    "cuda_fixed_009", "cuda_fixed_014", "cuda_fixed_024",
                    "cuda_fixed_049", "cuda_fixed_074", "cuda_fixed_099",
                    "cuda_fixed_124", "cuda_fixed_149", "cuda_fixed_499", 
                    "cuda_fixed_999"]
fixed_labels = ["fixed_000", "fixed_001", "fixed_004",
                    "fixed_009", "fixed_014", "fixed_024",
                    "fixed_049", "fixed_074", "fixed_099",
                    "fixed_124", "fixed_149", "fixed_499", 
                    "fixed_999"]

cuda_wang_labels = ["cuda_wang_100.0", "cuda_wang_0.1277", "cuda_wang_0.05116",
                    "cuda_wang_0.02949", "cuda_wang_0.023741", "cuda_wang_0.01572",
                    "cuda_wang_0.00957", "cuda_wang_0.007325", "cuda_wang_0.00639",
                    "cuda_wang_0.005592", "cuda_wang_0.004764", "cuda_wang_0.0020131",
                    "cuda_wang_0.001391"]
wang_labels = ["wang_100.0", "wang_0.1277", "wang_0.05116",
                    "wang_0.02949", "wang_0.023741", "wang_0.01572",
                    "wang_0.00957", "wang_0.007325", "wang_0.00639",
                    "wang_0.005592", "wang_0.004764", "wang_0.0020131",
                    "wang_0.001391"]

cuda_rec_sub_labels = ["cuda_rec_sub_100.0", "cuda_rec_sub_0.0559", "cuda_rec_sub_0.020685",
                        "cuda_rec_sub_0.01221", "cuda_rec_sub_0.00921", "cuda_rec_sub_0.005983",
                        "cuda_rec_sub_0.00365842", "cuda_rec_sub_0.00282126", "cuda_rec_sub_0.00235283",
                        "cuda_rec_sub_0.0019996", "cuda_rec_sub_0.00172711", "cuda_rec_sub_0.00076726",
                        "cuda_rec_sub_0.000484781"]
rec_sub_labels = ["rec_sub_100.0", "rec_sub_0.0559", "rec_sub_0.020685",
                        "rec_sub_0.01221", "rec_sub_0.00921", "rec_sub_0.005983",
                        "rec_sub_0.00365842", "rec_sub_0.00282126", "rec_sub_0.00235283",
                        "rec_sub_0.0019996", "rec_sub_0.00172711", "rec_sub_0.00076726",
                        "rec_sub_0.000484781"]

aabb_labels = ["3276 (no splits)", "~6552", "~16380", "~32760", "~49140", "~81900", "~163800", "~245700",
                "~327600", "~409500", "~491400", "~1638000", "~3276000"]

df_name = "locate_timing"
average_col = "AVERAGE of time"
stdev_col = "STDEV of time"

ylabel = "time (s)"
xlabel = "number of AABBs"
title = "AABB Times"


x = np.arange(len(aabb_labels))  # the label locations
width = 0.2  # the width of the bars
aabb_times_fixed = dfs[df_name].loc[cuda_fixed_labels, average_col]
aabb_times_wang = dfs[df_name].loc[cuda_wang_labels, average_col]
aabb_times_rec_sub = dfs[df_name].loc[cuda_rec_sub_labels, average_col]

aabb_times_fixed_std = dfs[df_name].loc[cuda_fixed_labels, stdev_col]
aabb_times_wang_std = dfs[df_name].loc[cuda_wang_labels, stdev_col]
aabb_times_rec_sub_std = dfs[df_name].loc[cuda_rec_sub_labels, stdev_col]

error_kwdict = {'lw':0.75, 'color':'gray'}

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, aabb_times_fixed, width, yerr=aabb_times_fixed_std, label='Fixed', color='#FF1053', error_kw=error_kwdict)
rects2 = ax.bar(x, aabb_times_wang, width, yerr=aabb_times_wang_std, label='Wangs Formula', color='#6C6EA0', error_kw=error_kwdict)
rects3 = ax.bar(x + width, aabb_times_rec_sub, width, yerr=aabb_times_rec_sub_std, label='Recrsive Subdivision', color='#66C7F4', error_kw=error_kwdict)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel(ylabel)
ax.set_xlabel(xlabel)
ax.set_title(title)
ax.set_xticks(x)
ax.set_xticklabels(aabb_labels, fontdict={'rotation':'vertical'})
ax.legend()

fig.tight_layout()

plt.show()
