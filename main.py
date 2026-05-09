import sys
from analysis import load_food_access, load_excess_food, create_regions, correlation, top_mismatch
from visualization import scatter_plot, histogram, bar_chart

access_file = sys.argv[1]
excess_file = sys.argv[2]

food_access = load_food_access(access_file)
excess_food = load_excess_food(excess_file)
regions = create_regions(food_access, excess_food)

print("Correlation:", correlation(regions))
print("\nTop mismatch counties:\n")

for r in top_mismatch(regions):
    print(r.summary())

scatter_plot(regions)
histogram(regions)
bar_chart(regions)