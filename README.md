# Fall 2022 CS170 Project Skeleton
This repository contains utility functions which might be helpful for solving the project.

## Requirements
`python >= 3.6` is needed for the python files.

C++ is needed if you want to recompile the code. If you have C++ already installed, then add [this package](https://json.nlohmann.me/integration/package_managers/#conda) using your preferred package manager.

If you don’t have c++ installed, then follow [these instructions](https://www.msys2.org/) and then run:

    pacman -S mingw-w64-x86 64-toolchain
    pacman -S mingw-w64-x86 64-nlohmann-json

## Instructions
To compile run: 

    g++ -fopenmp -o main main.cpp rpg.cpp graph utils.cpp

To run the algorithm:

    ./main 

**Note: the algorithm takes a long time to run as it was run overnight usually.**

It outputs all the .out files for each graph to the rpg_outputs folder and to generate the tar you can just use:

    py rpg.py 

**Note: you might be told you are missing packages. If you are then simply use pip to install them (requests, Seleneum, etc).**

If you would like to run the python version of the code, uncomment the second to last line of rpg.py and use:

    py rpg.py

**Note: the python version has slightly less optimized parameters but is the same algorithm.**

## Licence
Copyright 2022, The Regents of the University of California and UC Berkeley CS170 Staff  
All rights reserved.  
This content is protected and may not be shared, uploaded, or distributed without prior permission. 


