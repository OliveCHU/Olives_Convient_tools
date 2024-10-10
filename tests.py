#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 10:29:24 2024

@author: mengyuanchu
"""
raw = []

# 1. corrolation test 
from scipy import stats

res = stats.pearsonr(raw[x_column], raw[y_column])
# print(res)
plt.annotate("Pearson R = %.2f\n p= %.4f" %(res[0], res[1]) , 
            fontsize=8, 
            xycoords ='axes fraction',
            # fontweight='bold',
            family='Arial'
            ,xy = (0.2,0.75))


#  2. Kruskal-Wallis test
from scipy import stats
import scikit_posthocs as sp
groups = tt.groupby(para)[pol + '_average'].apply(lambda x: list(x.dropna())).to_dict()
kruskal_result = stats.kruskal(*groups.values())
# print("Kruskal-Wallis Test Result:")
print(f"Statistic: {kruskal_result.statistic}")
print(f"P-value: {kruskal_result.pvalue}")
groups_list = list(groups.values())
print(groups.keys())
# https://scikit-posthocs.readthedocs.io/en/latest/generated/scikit_posthocs.posthoc_dunn.html
# print(sp.posthoc_dunn([groups['EU4'],groups['EU5'],groups['EU6']], p_adjust = 'fdr_bh'))
print(sp.posthoc_dunn(groups_list, p_adjust =  'hommel' ))                      # 'holm-sidak' ))
                      # 'fdr_bh'))

# 3. mannwhitneyu test with the 
# https://rowannicholls.github.io/python/graphs/ax_based/boxplots_significance.html#test-for-statistical-significance
from scipy import stats
species = raw['veh'].unique()
combinations = itertools.combinations(species, 2)
for combination in combinations:
    print(combination)
# Check from the outside pairs of boxes inwards
ls = list(range(1, len(species ) + 1))
combinations = [(ls[x], ls[x + y]) for y in reversed(ls) for x in range((len(ls) - y))]
# for combination in combinations:
#     print(combination)

# Initialise a list of combinations of groups that are significantly different
significant_combinations = []
# Check from the outside pairs of boxes inwards
# ls = list(range(1, len(raw) + 1))
combinations = [(ls[x], ls[x + y]) for y in reversed(ls) for x in range((len(ls) - y))]
for combination in combinations:
    data1 = raw['Q'][raw['veh']== species[combination[0]-1] ]
    data2 = raw['Q'][raw['veh']== species[combination[1]-1] ]
    # Significance
    U, p = stats.mannwhitneyu(data1, data2, alternative='two-sided')
    if p < 0.05:
        significant_combinations.append([combination, p])

print(significant_combinations)

# Get the y-axis limits
bottom, top = ax.get_ylim()
y_range = (top - bottom)*0.6


# Significance bars
for i, significant_combination in enumerate(significant_combinations):
    # Columns corresponding to the datasets of interest
    x1 = significant_combination[0][0]-1
    x2 = significant_combination[0][1]-1
    # What level is this bar among the bars above the plot?
    level = len(significant_combinations) - i
    # Plot the bar
    bar_height = (y_range * 0.07 * level) + top -2000
    bar_tips = bar_height - (y_range * 0.02)
    plt.plot(
        [x1, x1, x2, x2],
        [bar_tips, bar_height, bar_height, bar_tips], lw=1, c='k'
    )
    # Significance level
    p = significant_combination[1]
    if p < 0.001:
        sig_symbol = '***'
    elif p < 0.01:
        sig_symbol = '**'
    elif p < 0.05:
        sig_symbol = '*'
    text_height = bar_height - (y_range * 0.05) 
    plt.text((x1 + x2) * 0.5, text_height, sig_symbol, ha='center', va='bottom', c='k')




