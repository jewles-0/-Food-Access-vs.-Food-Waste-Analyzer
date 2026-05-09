import matplotlib.pyplot as plt
import numpy as np
import os
 
def scatter_plot(regions):
    """Plot: Food insecurity vs excess food availability."""
    os.makedirs("output", exist_ok=True)
    
    needs = [r.low_access_pop for r in regions]
    excesses = [r.excess_food_tons for r in regions]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(needs, excesses, alpha=0.6, s=80, color='red')
    
    plt.xlabel('People Without Food Access', fontsize=12, fontweight='bold')
    plt.ylabel('Excess Food (Tons per Year)', fontsize=12, fontweight='bold')
    plt.title('Food Insecurity vs Excess Food Availability', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("output/scatter_plot.png", dpi=300)
    plt.close()
    print("✓ Saved output/scatter_plot.png")

 
def histogram(regions):
    """Plot: Distribution of waste-to-need ratios."""
    os.makedirs("output", exist_ok=True)
    
    ratios = [r.waste_to_need_ratio() for r in regions]
    
    plt.figure(figsize=(10, 6))
    plt.hist(ratios, bins=20, color='green', alpha=0.7, edgecolor='black')
    
    plt.axvline(np.mean(ratios), color='red', linestyle='--', linewidth=2, 
                label=f'Average: {np.mean(ratios):.4f}')
    
    plt.xlabel('Excess Food (Tons) per Person in Need', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Counties', fontsize=12, fontweight='bold')
    plt.title('Distribution of Waste-to-Need Ratios', fontsize=13, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig("output/histogram.png", dpi=300)
    plt.close()
    print("✓ Saved output/histogram.png")
    
 
def bar_chart(regions):
    """Plot: Top 10 worst counties (high need, low excess)."""
    os.makedirs("output", exist_ok=True)
    
    from analysis import top_mismatch
    
    mismatches = top_mismatch(regions, n=10)
    
    counties = [f"{r.county}, {r.state}" for r in mismatches]
    ratios = [r.waste_to_need_ratio() for r in mismatches]
    
    plt.figure(figsize=(10, 7))
    plt.barh(range(len(counties)), ratios, color='orange', edgecolor='black')
    
    plt.yticks(range(len(counties)), counties, fontsize=9)
    plt.xlabel('Waste-to-Need Ratio', fontsize=12, fontweight='bold')
    plt.title('Top 10 Worst Mismatches\n(High Need, Low Excess Food)', fontsize=13, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig("output/bar_chart.png", dpi=300)
    plt.close()
    print("✓ Saved output/bar_chart.png")

    # place in the termial this to open the plot 
    #open output/scatter_plot.png
# open output/histogram.png
# open output/bar_chart.png
 # to run program in terminal plug in the following command with your file names
 # python3 main.py Access.csv Excess.csv