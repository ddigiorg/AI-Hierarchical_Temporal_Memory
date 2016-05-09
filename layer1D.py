import random as rand
import numpy as np
import time

def init_layer_neuron_states(n_time_steps, n_columns, n_neurons):
	# Initialize binary 3D tensors indicating neuron active and predicted state at time steps

	neuron_states_shape   = (n_time_steps, n_columns, n_neurons)
	neuron_states_active  = np.zeros(neuron_states_shape, dtype=np.int8)
#	neuron_states_active  = np.random.randint(2, size=neuron_states_shape)
	neuron_states_predict = np.zeros(neuron_states_shape, dtype=np.int8)
#	neuron_states_predict = np.random.randint(2, size=neuron_states_shape)

	return neuron_states_active, neuron_states_predict

def init_layer_proximal_synapses(n_inputs, n_columns):
	
	connectivity = 0.5
	proximal_synapse_threshold = 20
	proximal_synapse_shape = (n_columns, n_inputs)

	# Initialize proximal synapse values as a 2D array of 0s
	proximal_synapse_values  = np.zeros(proximal_synapse_shape, dtype=np.int8)

	# Initialize proximal synapse connections as a 2D array of binary values
	proximal_synapse_connections = np.random.choice([0, 1], size=proximal_synapse_shape, p=[1-connectivity, connectivity])

	# Initialize proximal synapse permanances as a 2D array of integer values around the threshold value
	temporary_permanances = np.random.random_integers(proximal_synapse_threshold, proximal_synapse_threshold + 1, proximal_synapse_shape)
	proximal_synapse_permanances = temporary_permanances * proximal_synapse_connections

	return proximal_synapse_values, proximal_synapse_permanances

def init_layer_basal_synapses(n_columns, n_neurons, n_basal_dendrites):

	n_basal_synapses = 20
	basal_synapse_threshold = 20

	basal_synapse_shape = (n_columns, n_neurons, n_basal_dendrites, n_basal_synapses)

	basal_synapse_indices = np.zeros(basal_synapse_shape + (2,), dtype=np.int16)
	basal_synapse_values  = np.zeros(basal_synapse_shape, dtype=np.int8)
	basal_synapse_permanances = np.random.random_integers(basal_synapse_threshold, basal_synapse_threshold + 1, basal_synapse_shape)
	basal_synapse_thresholds = np.full(basal_synapse_shape, basal_synapse_threshold, dtype=np.int8)

	neuron_indices = [(c, n) for c in range(n_columns) for n in range(n_neurons)]

	start = time.time()
	neuron_indices = np.random.permutation(neuron_indices[0:20])
	end = time.time()
	print("BS Init Time: {}s".format(end - start))

	for c in range(n_columns):
		for n in range(n_neurons):
			neuron_indices = np.random.permutation(neuron_indices)
			for bd in range(n_basal_dendrites):
				basal_synapse_indices[c][n][bd] = neuron_indices[bd:bd+n_basal_synapses]

	print(basal_synapse_indices[0][0])

	return basal_synapse_values, basal_synapse_indices, basal_synapse_permanances, basal_synapse_thresholds

def spatial_pooling(inputs, n_columns, proximal_synapse_values, proximal_synapse_permanances):
	
	proximal_synapse_threshold = 20

	print(inputs)

	# Calculate if proximal synapse is connected: 2D array of boolean values if permanance value is greater than threshold
	proximal_synapse_is_connected = proximal_synapse_permanances > proximal_synapse_threshold
	print(proximal_synapse_is_connected + 0)
	
	# Calculate proximal synapse values: 2D array of binary values of the input value if the proximal synapse is connected
	proximal_synapse_values = np.logical_and(inputs, proximal_synapse_is_connected) + 0
	print(proximal_synapse_values)

	# Calculate overlap scores: 1D array of integers indicating the sum of each column's proximal synapse values
	overlap_scores = np.einsum('ij->i', proximal_synapse_values) 
	print(overlap_scores)

	'''
	# Inhibition
	active_columns_percent = 0.2
	n_active_columns = np.int16(np.ceil(n_columns * active_columns_percent))
	active_column_indices = np.zeros(n_active_columns, dtype=np.int16)
	column_states = np.zeros(n_columns, dtype=np.int8)	

	# NOTE: MAY HAVE TO SKIP COLUMNS THAT HAVE OVERLAP SCORE < 1 
	for ac in range(n_active_columns):
		greatest_overlap_index =  np.argmax(overlap_scores)
		active_column_indices[ac] = greatest_overlap_index
		column_states[greatest_overlap_index] = 1
		overlap_scores[greatest_overlap_index] = -1	

	# Learning
	proximal_synapse_learn_rate = 1
	proximal_synapse_permanance_lower = 0
	proximal_synapse_permanance_upper = 99
	for ac_index in active_column_indices:
		learn_array = proximal_synapse_learn_rate * (2 * proximal_synapse_values[ac_index] - 1)
		proximal_synapse_permanances[ac_index] = proximal_synapse_permanances[ac_index] + learn_array

	np.clip(proximal_synapse_permanances, proximal_synapse_permanance_lower, proximal_synapse_permanance_upper, out=proximal_synapse_permanances)

	return column_states, active_column_indices
	'''

def temporal_memory(n_neurons, neuron_states_active, neuron_states_predict, column_states, active_column_indices, basal_synapse_values, basal_synapse_indices, basal_synapse_permanances, basal_synapse_thresholds):

	neuron_states_active[0] = neuron_states_active[1]

	# Assign the basal synapse the active state value it points to
	basal_synapse_values = neuron_states_active[0][basal_synapse_indices[:, :, :, :, 0], basal_synapse_indices[:, :, :, :, 1]]	

#	print(basal_synapse_indices[0][0][0])

	# Determine active state of active column neurons
	'''MAKE THIS MORE OPTIMIZED'''
	#nActive = np.einsum('i,ij->ij', cActive, nPredict) 
	for ac_index in active_column_indices:
		flag = 0
		for n in range(n_neurons):
			active = neuron_states_active[0][ac_index][n]
			predict = neuron_states_predict[0][ac_index][n]			
			if predict == 1:
				active == 1
				flag = 1
		if flag == 0:
			for n in range(n_neurons):
				neuron_states_active[1][ac_index][n] = 1

	# Determine predictive state of all neurons
#	for c in range(numColumns):
#	test = np.dot(nActive[1][0], bsValues[0]
	
#	print(nActive)

	return neuron_states_active	


temp = [0]*10
temp[0] = 1
temp[1] = 1
temp[2] = 1
inputs = np.array(temp)
n_inputs = len(inputs)
n_time_steps = 2
n_columns = 10 #2048
n_neurons = 1  #32
n_basal_dendrites = 1

#print("Initializing...")

neuron_states_active, neuron_states_predict = init_layer_neuron_states(n_time_steps, n_columns, n_neurons)

start = time.time()
proximal_synapse_values, proximal_synapse_permanances = init_layer_proximal_synapses(n_inputs, n_columns)
end = time.time()
print("PS Init Time: {}s".format(end - start))

#start = time.time()
#basal_synapse_values, basal_synapse_indices, basal_synapse_permanances, basal_synapse_thresholds = init_layer_basal_synapses(n_columns, n_neurons, n_basal_dendrites)
#end = time.time()
#print("BS Init Time: {}s".format(end - start))

for i in range(1):
	start = time.time()
	column_states, active_column_indices = spatial_pooling(inputs, n_columns, proximal_synapse_values, proximal_synapse_permanances)
	end = time.time()
	print("Spatial Pooling Time: {}s".format(end - start))
	
#	start = time.time()
#	neuron_states_active = temporal_memory(n_neurons, neuron_states_active, neuron_states_predict, column_states, active_column_indices, basal_synapse_values, basal_synapse_indices, basal_synapse_permanances, basal_synapse_thresholds)
#	end = time.time()
#	print("Temporal Memory Time: {}s".format(end - start))
