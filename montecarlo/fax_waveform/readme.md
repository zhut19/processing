## Description

Using paxer simulation (fax) to generate data from fake input.

## To Run

python fax_production_main.py

## Motivation

Fax is designed to mimic detector responses to photons and electrons at given location. It is already implemented in full chain simulation.

However, full chain simulation is not cost effective timewise when the goal is not being most truthful to physics, instead just wanting to study certain feature of the detector, for example electron diffusion, photon propagation.

The scripts here make up to an isolated module to run fax.

## Thanks to 

Qing and Joey for that most classes in fax_production_process.py are modified from their code
Chris and Sander for that Batch and Submit class in fax_production_control.py are modified from their code
