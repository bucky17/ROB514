#!/usr/bin/env python3

# This is the code you need to do the Kalman filter for the door localization

import numpy as np

from world_ground_truth import WorldGroundTruth
from robot_sensors import RobotSensors
from robot_ground_truth import RobotGroundTruth


# State estimation using Kalman filter
#   Stores the belief about the robot's location as a Gaussian
#     See the probability_sampling assignment, gaussian, for how to implement store probability as a Gaussian
class KalmanFilter:
    def __init__(self):
        # Kalman (Gaussian) probabilities
        self.mu = 0.5
        self.sigma = 0.4

        self.reset_kalman()

    # Put robot in the middle with a really broad standard deviation
    def reset_kalman(self):
        self.mu = 0.5
        self.sigma = 0.4

    # Sensor reading, distance to wall
    def update_gauss_sensor_reading(self, robot_sensors, dist_reading):
        """ Update state estimation based on sensor reading
        @param robot_sensors - for mu/sigma of wall sensor
        @param dist_reading - distance reading returned by sensor"""

# YOUR CODE HERE
        return self.mu, self.sigma

    # Given a movement, update Gaussian
    def update_continuous_move(self, robot_ground_truth, amount):
        """ Kalman filter update mu/standard deviation with move (the prediction step)
        @param robot_ground_truth : robot state - has the mu/sigma for moving
        @param amount : The control signal (the amount the robot was requested to move
        @return : mu and sigma of new current estimated location """

# YOUR CODE HERE
        return self.mu, self.sigma


# YOUR CODE HERE


def test_kalman_update():
    """ Check against the saved results
    Beware that this requires only calling random.uniform when doing the sensor/move - any additional
     calls will throw the random numbers off"""

    print("Testing Kalman")
    # Generate some move sequences and compare to the correct answer
    import json
    with open("Data/check_kalman_filter.json", "r") as f:
        answers = json.load(f)

    kalman_filter = KalmanFilter()
    robot_ground_truth = RobotGroundTruth()
    robot_sensor = RobotSensors()

    # Set mu/sigmas
    robot_ground_truth.set_move_continuos_probabilities(answers["move_error"]["mu"], answers["move_error"]["sigma"])
    robot_sensor.set_distance_wall_sensor_probabilities(answers["sensor_noise"]["mu"], answers["sensor_noise"]["sigma"])

    # This SHOULD insure that you get the same answer as the solutions, provided you're only calling uniform within
    #  robot_ground_truth.move*
    np.random.seed(3)

    # Try different sequences
    for seq in answers["results"]:
        # Reset to uniform
        kalman_filter.reset_kalman()
        robot_ground_truth.reset()
        for i, s in enumerate(seq["seq"]):
            if s is "Sensor":
                dist = robot_sensor.query_distance_to_wall(robot_ground_truth)
                kalman_filter.update_gauss_sensor_reading(robot_sensor, dist)
                if not np.isclose(dist, seq["sensor_reading"][i]):
                    print(f"Warning, sensor reading should be {seq['sensor_reading'][i]}, got {dist}")
            else:
                actual_move = robot_ground_truth.move_continuous(seq['move_amount'][i])
                kalman_filter.update_continuous_move(robot_ground_truth, seq['move_amount'][i])
                if not np.isclose(actual_move, seq["actual_move"][i]):
                    print(f"Warning, move should be {seq['actual_move'][i]}, got {actual_move}")

        if not np.isclose(seq["mu"], kalman_filter.mu, atol=0.01):
            print(f"Failed sequence {seq['seq']}, got mu {kalman_filter.mu}, expected {seq['mu']}")
        if not np.isclose(seq["sigma"], kalman_filter.sigma, atol=0.01):
            print(f"Failed sequence {seq['seq']}, got sigma {kalman_filter.sigma}, expected {seq['sigma']}")

    print("Passed")
    return True


if __name__ == '__main__':

    test_kalman_update()

    print("Done")