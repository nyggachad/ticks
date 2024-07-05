class TickPopulationSimulator:
    def __init__(self):
        self.current_month = 1
        self.total_months = 0
        self.enviroment_settings = {
            'simulation_extent': 10000,  # square meters
            'number_of_cells': 100,
            'patch_size': 16,  # square meters
            'lawn_desiccation_parameter': 0.01,
        }
        self.host_settings = {
            "initial_hosts": 50,
            'movement_rate': 1,
            'host_mortality_rate': 0.002,
            'max_adults_per_host': 10,
            'max_nymphs_per_host': 25,
            'max_larvae_per_host': 100,
        }
        self.tick_settings = {
            'initial_ticks': 10000,
            'nymph_percent': 90,
            'adult_percent': 10,
            'prob_successful_attachment': 0.003,
            'eggs_laid_per_female': 250,
            'egg_to_hatching': 60//30, # 60 days
            'larvae_to_nymph': 270//30,
            'nymph_to_adult': 360//30,
            'maximum_questing_time': 42,
            'length_of_bloodmeal': 3,
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

    def get_mortality_rate(self):
        return self.monthly_mortality_rates[self.current_month]

    def get_next_month(self):
        self.current_month = 1 if self.current_month == 12 else self.current_month + 1

    def simulate_month_passage(self):
        # Increment the time tracker
        self.total_months += 1

        # Mortality applies to all life stages
        self.apply_mortality()

        # Check for any hatchings
        if self.total_months in self.birth_queue:
            self.larvae_population += self.birth_queue.pop(self.total_months)

        # Lifecycle transitions as ticks develop
        self.migrate_ticks()

        # Egg-laying by adult ticks
        if self.total_months % self.tick_settings['length_of_bloodmeal'] == 0:
            eggs_laid = self.adult_population * self.tick_settings['eggs_laid_per_female']
            hatching_month = self.total_months + self.tick_settings['egg_to_hatching']
            if hatching_month not in self.birth_queue:
                self.birth_queue[hatching_month] = 0
            self.birth_queue[hatching_month] += eggs_laid

        # Output current state
        self.output_current_state()

    def apply_mortality(self):
        mortality_rate = self.get_mortality_rate()
        self.adult_population -= int(self.adult_population * mortality_rate)
        self.nymph_population -= int(self.nymph_population * mortality_rate)
        self.larvae_population -= int(self.larvae_population * mortality_rate)

    def migrate_ticks(self):
        # Migration from larvae to nymphs
        if self.total_months % self.tick_settings['larvae_to_nymph'] == 0:
            self.nymph_population += self.larvae_population
            self.larvae_population = 0

        # Migration from nymphs to adults
        if self.total_months % self.tick_settings['nymph_to_adult'] == 0:
            self.adult_population += self.nymph_population
            self.nymph_population = 0

    def output_current_state(self):
        print(f"Month: {self.current_month}, Total Months: {self.total_months}")
        print(f"Adults: {self.adult_population}, Nymphs: {self.nymph_population}, Larvae: {self.larvae_population}")

# Simulation Execution
simulator = TickPopulationSimulator()
print("Initial State:")
simulator.output_current_state()
print("Starting simulation...")
for _ in range(24):  # Simulating over a span of 100 months
    simulator.simulate_month_passage()
    simulator.get_next_month()
