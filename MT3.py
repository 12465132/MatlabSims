from meep.chunk_balancer import ChunkBalancer
from meep.timing_measurements import MeepTimingMeasurements
from meep.materials import cSi
import meep as mp
import numpy as np
import math
import pickle
import os.path


LBaseSide = 8

LDomainHight = 250

LPHeight = 2

LBaseH = -(LDomainHight-2)/2
LDSide = LBaseSide/2

cell = mp.Vector3(8,8,LDomainHight)

prismVertcies = [mp.Vector3(-LDSide,-LDSide,LBaseH), 
                 mp.Vector3( LDSide,-LDSide,LBaseH), 
                 mp.Vector3( LDSide, LDSide,LBaseH), 
                 mp.Vector3(-LDSide, LDSide,LBaseH)]

geometry = [mp.Prism(prismVertcies,
                     height=2.83,
                     axis=mp.Vector3(0.0,0.0,1.0),
                     sidewall_angle=3.14/4.0,
                     material=mp.Medium(epsilon=3.43))]
# geometry = []

pml_layers = [mp.PML(1.0,direction=mp.Z)]

resolution = 10

sources = [mp.Source(mp.ContinuousSource(wavelength=2.94,is_integrated=True),
                     component=mp.Ex,
                     center=mp.Vector3(0,0,LBaseH),
                     size=mp.Vector3(LBaseSide,LBaseSide,0))]
# sources = [mp.Source(mp.GaussianSource(wavelength=2*(11**0.5)),
#                      component=mp.Ez,
#                      center=mp.Vector3(-7,-6.5),
#                      size=mp.Vector3(0,13))]

# def mod1(ax):
        # ax.set_xlabel('Testing')
        # return ax
  
animate1 = mp.Animate2D(fields= mp.By,
                       normalize=True,
                #        plot_modifiers = [mod1],
                       field_parameters={'alpha':0.8, 'cmap':'RdBu', 'interpolation':'none'},
                       boundary_parameters={'hatch':'o', 'linewidth':1.5, 'facecolor':'y', 'edgecolor':'b', 'alpha':0.3})
animate2 = mp.Animate2D(fields= mp.Ex,
                       normalize=True,
                #        plot_modifiers = [mod1],
                       field_parameters={'alpha':0.8, 'cmap':'RdBu', 'interpolation':'none'},
                       boundary_parameters={'hatch':'o', 'linewidth':1.5, 'facecolor':'y', 'edgecolor':'b', 'alpha':0.3})

# Fetch chunk layout from a previous run if it exists
if os.path.exists("chunk_layout.pkl"):
  initial_chunk_layout = pickle.load(open("chunk_layout.pkl", "rb"))
else:
  initial_chunk_layout = None
  
initial_chunk_layout = None
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    # geometry=geometry,
                    epsilon_input_file = 'MT3-out/MT3-eps-000000.00.h5',
                    sources=sources,
                    resolution=resolution,
                    Courant=.5,
                    k_point=mp.Vector3(0,0,1),
                    # chunk_layout=initial_chunk_layout,
                    split_chunks_evenly = False)
sim.use_output_directory()
sim.init_sim()

# sim.plot3D(save_to_image = True,image_name = 'sim.png')

sim.run(mp.synchronized_magnetic(
        mp.at_beginning(mp.output_epsilon),
        # mp.at_every(0.25,mp.in_volume(mp.Volume(mp.Vector3(0,0,0), size=mp.Vector3(LBaseSide,0,LDomainHight)),animate1)),
        # mp.at_every(0.25,mp.in_volume(mp.Volume(mp.Vector3(0,0,0), size=mp.Vector3(LBaseSide,0,LDomainHight)),animate2)),
        mp.to_appended("ex", mp.at_every(50, mp.output_tot_pwr)),
        # mp.in_volume(mp.Volume(mp.Vector3(0,0,0), size=mp.Vector3(LBaseSide,0,LBaseSide)), mp.to_appended("PT-slice", mp.output_tot_pwr)),
        ),until=400)

# animate1.to_mp4(fps=60,filename='MT3By.mp4')
# animate2.to_mp4(fps=60,filename='MT3Ex.mp4')


# Compute and save chunk layout for next run
timings = MeepTimingMeasurements.new_from_simulation(sim)
chunk_layout = sim.chunk_layout
chunk_volumes = sim.structure.get_chunk_volumes()
chunk_owners = sim.structure.get_chunk_owners()
next_chunk_layout = ChunkBalancer().compute_new_chunk_layout(
    timings,
    chunk_layout,
    chunk_volumes,
    chunk_owners,
    sensitivity=0.4)

# Save chunk layout for next run
with open("chunk_layout.pkl", "wb") as f:
    pickle.dump(next_chunk_layout, f)
    
print("CP1")
