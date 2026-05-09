import sys
import time
from analysis import load_food_access, load_excess_food, create_regions, correlation, statistics, top_mismatch
from visualization import scatter_plot, histogram, bar_chart

def main():
    """Main program with timing."""
    
    if len(sys.argv) != 3:
        print("Usage: python main.py Access.csv Excess.csv")
        sys.exit(1)
    
    total_start = time.time()
    
    access_file = sys.argv[1]
    excess_file = sys.argv[2]
    
    print("="*60)
    print("Food Waste Inequality Analyzer")
    print("="*60 + "\n")
    
    # Load data
    food_access = load_food_access(access_file)
    excess_food = load_excess_food(excess_file)
    
    # Create regions
    regions = create_regions(food_access, excess_food)
    
    # Analysis
    print("\nAnalysis:")
    corr = correlation(regions)
    stats = statistics(regions)
    
    print(f"\n{'='*60}")
    print(f"CORRELATION: {corr:.4f}")
    print(f"Mean low-access population: {stats['mean_need']:,.0f}")
    print(f"Mean excess food (tons): {stats['mean_excess']:,.1f}")
    print(f"{'='*60}\n")
    
    # Top mismatches
    print("Top 10 worst mismatches:")
    for i, r in enumerate(top_mismatch(regions), 1):
        print(f"{i:2d}. {r.summary()}")
    
    # Visualizations
    print("\nGenerating visualizations...")
    scatter_plot(regions)
    histogram(regions)
    bar_chart(regions)
    
    total_elapsed = time.time() - total_start
    print(f"\n✓ Total analysis time: {total_elapsed:.2f}s")

if __name__ == "__main__":
    main()
