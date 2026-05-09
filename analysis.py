import csv
import numpy as np
import time
from food_region import FoodRegion

STATE_MAP = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

def load_food_access(filename):
    """Load USDA food access data."""
    start = time.time()
    
    food_access = {}
    
    with open(filename, "r") as file:
        for _ in range(2):
            file.readline()
        
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                county = row.get("County", "").strip()
                state = row.get("State", "").strip()
                
                if county.endswith(" County"):
                    county = county[:-7]
                
                state = STATE_MAP.get(state, state)
                
                low_access = float(row.get("LAPOP1_10") or row.get("lapop1_10") or 0)
                
                if county and state:
                    key = (county, state)
                    food_access[key] = low_access
            except:
                continue
    
    elapsed = time.time() - start
    print(f"✓ Loaded {len(food_access)} regions in {elapsed:.2f}s")
    return food_access

def load_excess_food(filename):
    """Load EPA excess food data."""
    start = time.time()
    
    excess_food = {}
    
    with open(filename, "r") as file:
        for _ in range(2):
            file.readline()
        
        reader = csv.reader(file)
        
        for row in reader:
            try:
                if len(row) < 12:
                    continue
                
                county = row[5].strip()
                state = row[6].strip()
                
                low = float(row[10]) if row[10] else 0
                high = float(row[11]) if row[11] else 0
                tons = (low + high) / 2
                
                if county and state and tons > 0:
                    key = (county, state)
                    excess_food[key] = excess_food.get(key, 0) + tons
            except:
                continue
    
    elapsed = time.time() - start
    print(f"✓ Loaded excess food data in {elapsed:.2f}s")
    return excess_food

def create_regions(food_access, excess_food):
    """Convert data into FoodRegion objects."""
    start = time.time()
    
    regions = []
    for key in food_access:
        county, state = key
        low_access = food_access[key]
        tons = excess_food.get(key, 0)
        regions.append(FoodRegion(county, state, low_access, tons))
    
    elapsed = time.time() - start
    print(f"✓ Created {len(regions)} regions in {elapsed:.2f}s")
    return regions

def correlation(regions):
    """Calculate correlation using NumPy."""
    start = time.time()
    
    if len(regions) < 2:
        return 0
    
    # Convert to NumPy arrays
    needs = np.array([r.low_access_pop for r in regions])
    excesses = np.array([r.excess_food_tons for r in regions])
    
    # Calculate correlation
    corr = np.corrcoef(needs, excesses)[0][1]
    result = corr if not np.isnan(corr) else 0
    
    elapsed = time.time() - start
    print(f"✓ Calculated correlation in {elapsed:.2f}s")
    return result

def statistics(regions):
    """Calculate statistics using NumPy."""
    start = time.time()
    
    needs = np.array([r.low_access_pop for r in regions])
    excesses = np.array([r.excess_food_tons for r in regions])
    ratios = np.array([r.waste_to_need_ratio() for r in regions])
    
    stats = {
        'mean_need': np.mean(needs),
        'median_need': np.median(needs),
        'std_need': np.std(needs),
        'mean_excess': np.mean(excesses),
        'median_excess': np.median(excesses),
        'std_excess': np.std(excesses),
        'mean_ratio': np.mean(ratios),
        'median_ratio': np.median(ratios),
        'max_ratio': np.max(ratios),
        'min_ratio': np.min(ratios),
    }
    
    elapsed = time.time() - start
    print(f"✓ Calculated statistics in {elapsed:.2f}s")
    return stats

def top_mismatch(regions, n=10):
    """Find top N counties with worst mismatch using NumPy sorting."""
    start = time.time()
    
    # Create arrays for sorting
    ratios = np.array([r.waste_to_need_ratio() for r in regions])
    indices = np.argsort(ratios)  # NumPy sorting
    
    result = [regions[i] for i in indices[:n]]
    
    elapsed = time.time() - start
    print(f"✓ Found top mismatches in {elapsed:.2f}s")
    return result
