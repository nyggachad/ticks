class TickPopulationSimulator:
    def __init__(self):
        self.current_month = 1
        self.total_months = 0
        self.tick_settings = {
            'initial_ticks': 10000,
            'nymph_percent': 90,
            'adult_percent': 10,
            'eggs_laid_per_female': 250,
            'egg_to_hatching': 20,        # Reduced for demonstration
            'larvae_to_nymph': 6,  
            'nymph_to_adult': 12,  
        }

        self.monthly_mortality_rates = {
            1: 0.1, 2: 0.1, 3: 0.1, 4: 0.01, 5: 0.01, 6: 0.01,
            7: 0.01, 8: 0.01, 9: 0.1, 10: 0.1, 11: 0.1, 12: 0.1
        }
        # Initialize populations
        self.adult_population = self.tick_settings['initial_ticks'] * self.tick_settings['adult_percent'] // 100
        self.nymph_population = self.tick_settings['initial_ticks'] * self.tick_settings['nymph_percent'] // 100
        self.larvae_population = self.tick_settings['initial_ticks'] - self.adult_population - self.nymph_population
        self.birth_queue = {}

        print("Initializing simulation...")
        self.output_current_state()

    def get_mortality_rate(self):
        return self.monthly_mortality_rates[self.current_month]

    def get_next_month(self):
        self.current_month = 1 if self.current_month == 12 else self.current_month + 1

    def simulate_month_passage(self):
        self.total_months += 1
        self.apply_mortality()
        self.process_birth_queue()
        self.migrate_ticks()
        self.process_births()
        self.output_current_state()
    
    def apply_mortality(self):
        mortality_rate = self.get_mortality_rate()
        self.adult_population = int(self.adult_population * (1 - mortality_rate))
        self.nymph_population = int(self.nymph_population * (1 - mortality_rate))
        self.larvae_population = int(self.larvae_population * (1 - mortality_rate))

    def process_birth_queue(self):
        due_births = self.birth_queue.pop(self.total_months, 0)
        self.larvae_population += due_births

    def migrate_ticks(self):
        if self.total_months % self.tick_settings['larvae_to_nymph'] == 0:
            self.nymph_population += self.larvae_population
            self.larvae_population = 0
        if self.total_months % self.tick_settings['nymph_to_adult'] == 0:
            self.adult_population += self.nymph_population
            self.nymph_population = 0

    def process_births(self):
        if self.total_months % self.tick_settings['egg_to_hatching'] == 0:
            eggs_laid = self.adult_population * self.tick_settings['eggs_laid_per_female']
            hatching_time = self.total_months + self.tick_settings['egg_to_hatching']
            self.birth_queue[hatching_time] = self.birth_queue.get(hatching_time, 0) + eggs_laid

    def output_current_state(self):
        print(f"Month: {self.current_month}, Total Months: {self.total_months}")
        print(f"Adults: {self.adult_population}, Nymphs: {self.nymph_population}, Larvae: {self.larvae_population}")

# Simulation Execution
simulator = TickPopulationSimulator()
print("Starting simulation...")
for _ in range(12):  # simulate for an additional 100 months
    simulator.get_next_month()
    simulator.simulate_month_passage()
