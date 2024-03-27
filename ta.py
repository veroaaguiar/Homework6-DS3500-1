import pandas as pd
import numpy as np
import pytest

tas_df = pd.read_csv('tas.csv')
sections_df = pd.read_csv('sections.csv')

# Process TA Data
# Assume columns 0 to 16 in tas_df correspond to availability and preference
ta_data = tas_df.iloc[:, 3:].replace({'U': 0, 'W': 1, 'P': 2}).values

# we still need max_assigned information for each TA:
def max_assigned(tas_df):
    return tas_df['max_assigned'].values
max_assigned = max_assigned(tas_df)
# what we will have to do with max_assigned: # loop through and see when a TA id is assigned too many times, correspond it to max_assigned index

# Process Section Data
# Extract the 'min_ta' and 'max_ta' columns from sections_df
min_ta = sections_df['min_ta'].values
max_ta = sections_df['max_ta'].values
# make sure it's not going over the max number. have baby arrays in big array [min, max]
section_data = np.column_stack((min_ta, max_ta))

def times(sections_df):
    return sections_df['daytime'].values
times = times(sections_df)

# Combine Data
num_tas = len(ta_data)
num_sections = len(section_data)

# initialize our solution data structure by having each array (row) represent a ta and each column (or index in that array) represent a lab practicum
# just initialize it by randomly filling the array's with 0 or 1 (they are assigned or not assigned) and then we will make them better

data_arrays = [np.random.randint(2, size=num_sections) for _ in range(num_tas)]

# Combine the individual arrays into a single data structure
data = np.array(data_arrays)

# before we do objectives/agents, function should assign ta's to section.
# loop through different lists within the list, assign a random number from the TA options
# start by randomly assigning them to a practicum with no consideration for their preferences



# Add objectives below


def overallocation(data, max_assigned):
    """ If a TA requests at most 2 labs and you assign to them 5 labs, that’s an overallocation penalty of 3. 
    Compute the objective by summing the overallocation penalty over all TAs. There is no minimum allocation"""

    return sum([num_assigned - max_assigned[i] for i, num_assigned in enumerate(map(sum, data)) if num_assigned > max_assigned[i]])



def time_conflict(data, times):
    penalty = 0
    for i in range(len(data)):
        ta_array = data[i]
        indices = np.where(ta_array==1)[0]
        #print('this is indeces: ', indices)
        selected_times = times[indices]
        # Check if there's a conflict 
        has_conflict = len(selected_times) != len(np.unique(selected_times))
        #print("Is there a time conflict?", has_conflict)
        if has_conflict:
            penalty += 1
    return penalty



total_time_conflict_penalty = time_conflict(data,times)
print(total_time_conflict_penalty)
