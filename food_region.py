# food region 
class FoodRegion:

    def __init__(self, county, state, low_access_pop, excess_food_tons):

        self.county = county
        self.state = state
        self.low_access_pop = float(low_access_pop)
        self.excess_food_tons = float(excess_food_tons)

    def waste_to_need_ratio(self):

        if self.low_access_pop == 0:
            return 0

        return self.excess_food_tons / self.low_access_pop

    def is_high_need(self):

        return self.low_access_pop > 10000

    def summary(self):

        return f"{self.county}, {self.state} | Ratio: {self.waste_to_need_ratio():.2f}"