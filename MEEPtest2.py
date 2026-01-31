import meep as mp

cell = mp.Vector3(16,16,0)

geometry = [mp.Block(mp.Vector3(12,1,mp.inf),
                     center=mp.Vector3(-2.5,-3.5),
                     material=mp.Medium(epsilon=12)),
            mp.Block(mp.Vector3(1,12,mp.inf),
                     center=l,
                     material=mp.Medium(epsilon=12))]

pml_layers = [mp.PML(1.0)]

resolution = 20

sources = [mp.Source(mp.ContinuousSource(wavelength=2*(11**0.5), width=20),
                     component=mp.Ez,
                     center=mp.Vector3(-7,0),
                     size=mp.Vector3(0,13))]
# sources = [mp.Source(mp.GaussianSource(wavelength=2*(11**0.5)),
#                      component=mp.Ez,
#                      center=mp.Vector3(-7,-6.5),
#                      size=mp.Vector3(0,13))]

# def mod1(ax):
        # ax.set_xlabel('Testing')
        # return ax
  
animate = mp.Animate2D(fields=mp.Ez,
                       normalize=True,
                #        plot_modifiers = [mod1],
                       field_parameters={'alpha':0.8, 'cmap':'RdBu', 'interpolation':'none'},
                       boundary_parameters={'hatch':'o', 'linewidth':1.5, 'facecolor':'y', 'edgecolor':'b', 'alpha':0.3})


sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution,
                    Courant=.5)

# sim.to_(fields=mp.Ez,
        #    field_parameters={'alpha':0.8, 'cmap':'RdBu', 'interpolation':'none'},
        #    boundary_parameters={'hatch':'o', 'linewidth':1.5, 'facecolor':'y', 'edgecolor':'b', 'alpha':0.3})


sim.run(mp.at_beginning(mp.output_epsilon),
        mp.at_every(0.25,animate),
        mp.to_appended("ez", mp.at_every(0.6, mp.output_efield_z)),
        until=400)

animate.to_mp4(fps=60,filename='meepvideo.mp4')

print("CP1")

import numpy as np
import matplotlib.pyplot as plt

eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
# plt.figure()
# plt.imshow(eps_data, interpolation='spline36', cmap='binary')
# plt.axis('off')
# plt.show()

print("CP2")


ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
# plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
# plt.axis('off')
# plt.show()

print("CP3")


# plt.show()
# plt.savefig('sim_domain.png')

print("CP4")
