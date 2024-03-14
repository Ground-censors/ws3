# ws3 - Wood Supply Simulation System

**ws3** (Wood Supply Simulation System) is a Python package for modeling landscape-level wood supply planning problems.

Read the tutorial [here](https://ws3.readthedocs.io/en/dev/).

## Table of Contents

- [Modules](#modules)
- [Examples](#examples)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

---

## Modules 

**ws3** consists of the following main modules:

- **common.py**: Contains definitions for global attributes, functions, and classes that might be used anywhere in the package.
- **core.py**: *(Description needed)*
- **forest.py**: Implements functions for building and running wood supply simulation models.
- **opt.py**: Implements functions for formulating and solving optimization problems. 
- **spatial.py**: Implements the `ForestRaster` class, which can be used to allocate an aspatial disturbance schedule (for example, an optimal solution to a wood supply problem generated by an instance of the `forest.ForestModel` class) to a rasterized representation of the forest inventory.

## Examples 

- **010_ws3_model_example-fromscratch.ipynb**: Example of building a new **ws3** model from scratch.
- **020_ws3_model_example-woodstock.ipynb**: Example of building a **ws3** model from Woodstock-format text input files.
- **030_ws3_libcbm_sequential-fromscratch.ipynb**: This notebook creates the linkages between **ws3** and **libcbm** from scratch (i.e., all code required to create these linkages is developed directly in this notebook).
- **031_ws3_libcbm_sequential-builtin.ipynb**: This notebook replicates what **030_ws3_libcbm_sequential-fromscratch.ipynb** does, but using **ws3** built-in **CBM** linkage functions.
- **040_ws3_libcbm_neilsonhack-fromscratch.ipynb**: This notebook shows how to implement the Neilson hack (i.e., generate carbon yield curves from a CBM for use in a forest estate model) using **ws3** and **libcbm**.

## Installation

Instructions on how to install **ws3** and any prerequisites can be found in "example/000_venv_python_kernel_setup.ipynb".

## Usage

Instructions on how to use the project, including examples and code snippets.

## Contributing

Feel free to contribute to the model if you have suggestions or improvements.

## License

**MIT License**
Copyright (c) 2015-2018 Gregory Paradis

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
- The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

## Acknowledgments

Acknowledgment to individuals or organizations contributing to the project.

## Contact

For questions, feedback, or issues related to the project, please contact:
Gregory Paradis - gregory.paradis@ubc.ca
