"""I-210 subnetwork example."""
import os

import numpy as np

from flow.controllers.car_following_models import IDMController
from flow.controllers.lane_change_controllers import StaticLaneChanger
from flow.controllers.routing_controllers import I210Router
from flow.core.params import SumoParams
from flow.core.params import EnvParams
from flow.core.params import NetParams
from flow.core.params import SumoLaneChangeParams
from flow.core.params import VehicleParams
from flow.core.params import InitialConfig
from flow.core.params import InFlows

from flow.core.params import SumoCarFollowingParams

import flow.config as config
from flow.envs import TestEnv

# Instantiate which conditions we want to be true about the network

WANT_GHOST_CELL = True
WANT_DOWNSTREAM_BOUNDARY = True
ON_RAMP = False

horizon = 1500 #number of simulation steps
sim_step = .5 #Simulation step size

inflow_rate = 2050 #Per lane flow rate in veh/hr
inflow_speed = 25.5 #Speed corresponding to this inflow rate


downstream_speed = 3.5 #What the downstream congestion speed should be

on_ramp_inflow = 100 #on ramp inflow rate


accel_data = (IDMController,{'a':1.3,'b':2.0,'noise':0.3,'fail_safe': ['obey_speed_limit', 'safe_velocity', 'feasible_accel', 'instantaneous']})

#accel_data = (IDMController,{'a':1.3,'b':2.0,'noise':0.3})

highway_start_edge = ''

if(WANT_GHOST_CELL):
    from flow.networks.i210_subnetwork_ghost_cell import I210SubNetwork, EDGES_DISTRIBUTION
    highway_start_edge = 'ghost0'
else:
    from flow.networks.i210_subnetwork import I210SubNetwork, EDGES_DISTRIBUTION
    highway_start_edge = "119257914"


vehicles = VehicleParams()

inflow = InFlows()


# car_following_params=SumoCarFollowingParams(speed_mode = 'aggressive'),


if ON_RAMP:   
    vehicles.add(
        "human",
        num_vehicles=0,
        lane_change_params=SumoLaneChangeParams(
            lane_change_mode="strategic",
        ),
        acceleration_controller=accel_data,
        car_following_params=SumoCarFollowingParams(speed_mode = 'aggressive'),
        routing_controller=(I210Router, {})
    )

    lane_list = ['0','1','2','3','4']

    for lane in lane_list:
        inflow.add(
            veh_type="human",
            edge=highway_start_edge,
            vehs_per_hour=inflow_rate,
            departLane=lane,
            departSpeed=inflow_speed)

    inflow.add(
        veh_type="human",
        edge="27414345",
        vehs_per_hour=on_ramp_inflow,
        departLane="random",
        departSpeed=10)
    inflow.add(
        veh_type="human",
        edge="27414342#0",
        vehs_per_hour=on_ramp_inflow,
        departLane="random",
        departSpeed=10)

else:

    vehicles.add(
        'human',
        num_vehicles=0,
        lane_change_params=SumoLaneChangeParams(
            lane_change_mode='strategic',
        ),
        acceleration_controller=accel_data,
    )

    lane_list = ['0','1','2','3','4']

    for lane in lane_list:
        inflow.add(
            veh_type="human",
            edge=highway_start_edge,
            vehs_per_hour=inflow_rate,
            departLane=lane,
            departSpeed=inflow_speed)


#This is the default file used:
sumo_templates_path = "examples/exp_configs/templates/sumo/"

sumo_templates_path = os.path.join(config.PROJECT_PATH,sumo_templates_path)


def Set_i210_congestion(sumo_templates_path=None,speed=5.0):
    '''
    This function creates a new xml file that has the new specificed downstream speed.
    It creates a new xml file called i210_downstream_set.xml each time from the original
    that is then used as the net file.

    '''
    speed = str(speed)

    #Original xml file:
    fileName = 'i210_with_ghost_cell_with_downstream_test_2.net.xml'
    fileName = os.path.join(sumo_templates_path,fileName)

    file_lines = []
    lines_to_change = [2415,2418,2421,2424,2427,2430]

    with open(fileName) as f:
        file_lines = f.readlines()


    for line_num in lines_to_change:
        new_line = file_lines[line_num][:183]+speed+file_lines[line_num][186:]
        file_lines[line_num] = new_line

    #New xml file that will be used in the sim:
    new_fileName = os.path.join(sumo_templates_path,'i210_downstream_set.xml')

    with open(new_fileName, 'w') as filehandle:
        filehandle.writelines(file_lines)


    return new_fileName

NET_TEMPLATE = Set_i210_congestion(sumo_templates_path=sumo_templates_path,speed=downstream_speed)


flow_params = dict(
    # name of the experiment
    exp_tag='I-210_subnetwork',

    # name of the flow environment the experiment is running on
    env_name=TestEnv,

    # name of the network class the experiment is running on
    network=I210SubNetwork,

    # simulator that is used by the experiment
    simulator='traci',

    # simulation-related parameters
    sim=SumoParams(
        sim_step=sim_step,
        render=False,
        color_by_speed=True,
        use_ballistic=True
    ),

    # environment related parameters (see flow.core.params.EnvParams)
    env=EnvParams(
        horizon=horizon,
    ),

    # network-related parameters (see flow.core.params.NetParams and the
    # network's documentation or ADDITIONAL_NET_PARAMS component)
    net=NetParams(
        inflows=inflow,
        template=NET_TEMPLATE,
        additional_params={"use_on_ramp": ON_RAMP}
    ),

    # vehicles to be placed in the network at the start of a rollout (see
    # flow.core.params.VehicleParams)
    veh=vehicles,

    # parameters specifying the positioning of vehicles upon initialization/
    # reset (see flow.core.params.InitialConfig)
    initial=InitialConfig(
        edges_distribution=EDGES_DISTRIBUTION,
    ),
)

edge_id = "119257908#1-AddedOnRampEdge"
custom_callables = {
    "avg_merge_speed": lambda env: np.nan_to_num(np.mean(
        env.k.vehicle.get_speed(env.k.vehicle.get_ids_by_edge(edge_id)))),
    "avg_outflow": lambda env: np.nan_to_num(
        env.k.vehicle.get_outflow_rate(120)),
    # we multiply by 5 to account for the vehicle length and by 1000 to convert
    # into veh/km
    "avg_density": lambda env: 5 * 1000 * len(env.k.vehicle.get_ids_by_edge(
        edge_id)) / (env.k.network.edge_length(edge_id)
                     * env.k.network.num_lanes(edge_id)),
}
