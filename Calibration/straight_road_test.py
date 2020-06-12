"""
@author: Sadman Ahmed Shanto
status: in development
===================================================================================================================================
Update Plan: 
    1) have multiple sim launching script ready  
        a) launch a sim with default values
        b) launch a sim with chosen values
    2) have script that creates data params 
        a) script must also have abilities to create random numbers
        b) script can generate n number of entries
    3) have script that plots microsim data and macro info
    4) have script that uses the parameter data relationship established by 1)a) and 1)b) and some 
            calibration model to take data from from unknown params to determine the params
            then check for how close those params are
    5) create mother script to automate 
    (optional)
    6) for a default param set generate FD and using that same set sim a closed road traffic flow
        then generate FD from the data 
    7) generate sim with velocity and other driver behaviour params from distribution (probabilities, randomness and statistics)
        a) inflow resembling some realistic distribution

Expected TimeLine:
    Jun 12: have data generation script and multiple sim launching script ready (date_generate.py, straight_road_test.py and ~calib_sim.sh)
    Weekend: read calibration paper 
    Monday: data_analysis.py and calibrate.py
    Tuesday: have prelim results ready, tweak process 
    Wednesday: have results and explanations ready

Control Flow of Program:
    date_generate.py -> data.csv -> calib_sim.sh -> straight_road_test.py -> microsim_data.csv 
    microsim_data.csv -> data_analysis.py -> (figures, macro data, params) -> Allinfo.csv 
    Allinfo.csv & referenceDataParams -> calibrate.py -> guesses the params from macro info and generates stats on accuracy (prelim results)

Presently Working On:
    determining inflow params
===================================================================================================================================
"""

from flow.controllers import IDMController,OV_FTL_Controller,LinearOVM,BandoFTL_Controller
from flow.core.params import SumoParams, EnvParams, NetParams, InitialConfig, SumoLaneChangeParams
from flow.core.params import VehicleParams, InFlows
from flow.envs.ring.lane_change_accel import ADDITIONAL_ENV_PARAMS
from flow.networks.highway import HighwayNetwork, ADDITIONAL_NET_PARAMS
from flow.envs import LaneChangeAccelEnv
from flow.core.experiment import Experiment
import numpy as np
import pandas as pd
import os, sys

"""
accel_data = (BandoFTL_Controller,{'alpha':.5,'beta':20.0,'h_st':12.0,'h_go':50.0,'v_max':30.0,'noise':1.0})
traffic_speed = 18.1
traffic_flow = 2056
"""
#read data
a = round(float(sys.argv[1]),2)
b = round(float(sys.argv[2]),2)
noise =round(float(sys.argv[3]),2)
v0 = round(float(sys.argv[4]),3)
T = round(float(sys.argv[5]),2)
delta = round(float(sys.argv[6]),2)
s0 = round(float(sys.argv[7]),2)

accel_data = (IDMController, {'a':a,'b':b,'noise':noise, 'v0':v0, 'T':T, 'delta':delta, 's0':s0})
traffic_speed = 25.8
traffic_flow = 1720

vehicles = VehicleParams()
vehicles.add(
    veh_id="human",
    acceleration_controller=accel_data,
    lane_change_params=SumoLaneChangeParams(
        model="SL2015",
        lc_sublane=2.0,
    ),
)

env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)

inflow = InFlows()
inflow.add(
    veh_type="human",
    edge="highway_0",
    vehs_per_hour=traffic_flow,
    departLane="free",
    departSpeed=traffic_speed)

# inflow.add(
#     veh_type="human2",
#     edge="highway_0",
#     probability=0.25,
#     departLane="free",
#     departSpeed=20)


additional_net_params = ADDITIONAL_NET_PARAMS.copy()
additional_net_params['lanes'] =1
additional_net_params['length'] = 10000

flow_params = dict(
    # name of the experiment
    exp_tag='highway',
    # name of the flow environment the experiment is running on
    env_name=LaneChangeAccelEnv,
    # name of the network class the experiment is running on
    network=HighwayNetwork,
    # simulator that is used by the experiment
    simulator='traci',
    # sumo-related parameters (see flow.core.params.SumoParams)
    sim=SumoParams(
        render=False,
        lateral_resolution=1.0,
        emission_path='data',
        restart_instance=True,
    ),
    # environment related parameters (see flow.core.params.EnvParams)
    env=EnvParams(
        horizon=1000,
        additional_params=ADDITIONAL_ENV_PARAMS.copy(),
    ),
    # network-related parameters (see flow.core.params.NetParams and the
    # network's documentation or ADDITIONAL_NET_PARAMS component)
    net=NetParams(
        inflows=inflow,
        additional_params=additional_net_params,
    ),
    # vehicles to be placed in the network at the start of a rollout (see
    # flow.core.params.VehicleParams)
    veh=vehicles,
    # parameters specifying the positioning of vehicles upon initialization/
    # reset (see flow.core.params.InitialConfig)
    initial=InitialConfig(
        spacing="uniform",
        shuffle=True,
    ),
)


#create experiment obj using flow params
exp = Experiment(flow_params)

# run the sumo simulation
_ = exp.run(1, convert_to_csv=True)

# to get data file as csv
emission_location = os.path.join(exp.env.sim_params.emission_path, exp.env.network.name)
print(emission_location + '-emission.xml')
pd.read_csv(emission_location + '-emission.csv')
