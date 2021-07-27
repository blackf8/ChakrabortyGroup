# ChakrabortyGroup
The Chakraborty Group develops mathematical models and simulations for complex materials in various systems. This repository holds all of the different programs created to furthur aid our research group. Main topics include analysis of discontinuous shear thickening(DST) and jamming simulation data.

## DST Network Visualization Project (networkx2.py)
Personal Goal: To better understand the python by working on my first personal project utilizing the language.
Project Goal: The aim of this project is to gain a visual understanding of what occurs during discontinuous shear thickening(DST). The final implementation of the project, networkx2, uses object oriented programming to create snapshots of DST simulations which are then stiched together using video editing software. This version aimed to perform faster than the original implementation largely due to the use of generators when iterating through the DST particle data. After this version was complete I ran some runtime tests to measure the improvement of performance between both versions.

Networkx2 is a reimplementation of the networkx program using object oriented methods.
This program aims to create videos of particle simulations that under-go DST.(Discontinuous Shear Thickening)
By using objects and generators we can greatly improve the runtime and memory usage of the program, thus
allowing the production of faster videos. At the end of this program I included some runtime tests to see how
efficient these changes actually are.
