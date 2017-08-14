learn_rate = 0.0001
weights = [0.0018, 0.0017, 0.0019, 0.0011, 0.0013, 0.0012, 0.0011]

fr_p = 0.0
fc_p = 0.0
fl_p = 0.0

def prediction_reward(array_x):
    total = 0.0

    for i in range(0, 7):
        total = total + array_x[i] * weights[i]
    pass
    
    return total
pass

def update_weights(actual_reward, predicted_reward, array):
    for i in range(0, 7):
        pDelta = (predicted_reward - actual_reward) * array_x[i]
        weights[i] = weights[i] - (learn_rate * pDelta)
    pass
pass

def receive_reward(right, left, center, isGoingForward):
    reward = 0.0
    if right < 12.0 && left < 12.0 && center < 12.0:
        reward -= 3.0
    else if right < 6.0 || left < 6.0 || center < 6.0:
        reward -= 2.0
    
    if isGoingForward:
        reward += 1
    else
        reward += 0.65
    
    return reward
pass

# setup


# loop

def loop():
    # Scale Distances
    # Use previous distances
    fr_s = fr_p / 10.0
    fc_s = fc_p / 10.0
    fl_s = fl_p / 10.0
    
    # Create Current State Representation
    # using prevoius loops distances
    # Notice indices 3,4 and 5 are left, forward, right.
    # final index is the bias unit.
    array_x = [fr_s, fc_s, fl_s, 1, 0, 0, 1]

    # what is predicted for left?
    left_prediction = prediction_reward(array_x)
    # re-encode state for forward
    array_x[3] = 0
    array_x[4] = 1

    # what is forward reward prediction?
    forward_prediction = prediction_reward(array_x)

    # re-encode state for right
    array_x[4] = 0    
    array_x[5] = 1

    # what is right prediction?
    right_prediction =  prediction_reward(array_x)

    # fr_d = read_distance()
    # fc_d = read_distance()
    # fl_d = read_distance()

    # actual reward
    actual_reward = 0.0 #a_reward
    # predicted reward for action actually taken.
    predicted_reward = 0.0 #y_reward

    if predicted_reward > 1000 || predicted_reward < -1000:
        for i in range(0,7):
            weights[i] = 0.0001 * 1
        pass
    pass

    if forward_prediction > left_prediction && forward_prediction > right_prediction:
        #go forward
        predicted_reward = forward_prediction
        actual_reward = receive_reward(right_distance, left_distance, center_distance, true)
        array_x[3] = 0
        array_x[4] = 1
        array_x[5] = 0
    elif left_prediction > right_prediction:
        #go left
        predicted_reward = left_prediction
        actual_reward = receive_reward(right_distance, left_distance, center_distance, false)
        array_x[3] = 1
        array_x[4] = 0
        array_x[5] = 0
    elif forward_prediction == right_prediction && forward_prediction == left_prediction:
        #go forward
        predicted_reward = forward_prediction
        actual_reward = receive_reward(right_distance, left_distance, center_distance, true)
        array_x[3] = 0
        array_x[4] = 1
        array_x[5] = 0 
    else
        #go right
        predicted_reward = right_prediction
        actual_reward = receive_reward(right_distance, left_distance, center_distance, false)
        array_x[3] = 0
        array_x[4] = 0
        array_x[5] = 1
    pass

    update_weights(actual_reward, predicted_reward, array_x)

    fr_p = fr_d
    fc_p = fm_d
    fl_p = fl_d
pass