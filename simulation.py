month_mortality = {
    1: 0.1,  # January
    2: 0.1,  # February
    3: 0.1,  # March
    4: 0.01,  # April
    5: 0.01,  # May
    6: 0.01,  # June
    7: 0.01,  # July
    8: 0.01,  # August
    9: 0.1,  # September
    10: 0.1,  # October
    11: 0.1,  # November
    12: 0.1,  # December
}

def get_total_months(days):
    return days // 30

current_month = 1

def get_next_month(current_month):
    if current_month == 12:
        return 1
    return current_month + 1

def get_mortality_rate():
    return month_mortality[current_month]


# ENVIROMENT SETTINGS
enviroment_settings = {
    'simulation_extent': 10000, # 10,000 square meters
    'number_of_cells': 100, # 625 patches (25x25) grid
    'patch_size': 16, # 16 square meters
    'monthly_mortality_rate': get_mortality_rate,
    'lawn_desiccation_parameter': 0.01, # means 1% of the lawn will be desiccated (desiccation is the state of extreme dryness)
}

# HOSTS SETTINGS
host_settings = {
    "initial_hosts": 50,
    'movement_rate': 1, # patch per timestamp
    'host_mortality_rate': 0.002, # per 24 hours
    'max_adults_per_host': 10, # 10 ticks
    'max_nymphs_per_host': 25, # 25 ticks
    'max_larvae_per_host': 100, # 100 ticks
}


# TICK SETTINGS

tick_settings = {
    'initial_ticks': 10000,
    'nymph_percent': 90,
    'adult_percent': 10,
    'prob_successful_attachment': 0.003,
    'eggs_laid_per_female': 250, # 250 eggs
    'egg_to_hatching': 60, # 60 days
    'larvae_to_nymph': 270, # 270 days
    'nymph_to_adult': 360, # 360 days
    'maximum_questing_time': 42, # 42 days
    'length_of_bloodmeal': 3, # 3 days
}

tick_settings.update({
    'nymph_population': tick_settings.get('initial_ticks') * tick_settings.get('nymph_percent') // 100, 
    'adult_population': tick_settings.get('initial_ticks') * tick_settings.get('adult_percent') // 100,
})

total_months = 0
total_adults = tick_settings.get('adult_population')
total_nymphs = tick_settings.get('nymph_population')
total_larvae = tick_settings.get('initial_ticks') - total_adults - total_nymphs

total_ticks = total_adults + total_nymphs + total_larvae
print("STARTING SIMULATION")
print("total ticks:")
print(total_ticks)
print(f"total adults: {total_adults} total nymphs: {total_nymphs} total larvae: {total_larvae}")

birth_queue = {} # {month_time: number_of_births} # on laying eggs we will tick_settings[egg_to_hatching]: number_of_eggs to this queue, and then after egg_to_hatching days we will add them to the total_larvae

# Start simulation
def start_simulation_year():
    current_month = 1
    for i in range(12):
        total_months += 1
        current_month = get_next_month(current_month)
        print(current_month)
        print(enviroment_settings['monthly_mortality_rate']())


# start_simulation_year()