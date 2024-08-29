# Overview
This repository contains the code for parsing the raw measurement data
from [our ISP measurement campaign](https://doi.org/10.5281/zenodo.13388093)
and recreating the plots in the paper "Measuring Network Latency from
a Wireless ISP: Variations Within and Across Subnets", accepted for
IMC '24.

TODO: Add link to paper once it's published.

Most of the code is contained within Jupyter notebooks. To actually
run these notebooks, you will need to download the data files from
[Zenodo](https://doi.org/10.5281/zenodo.13388093) and place them in
unpack it (the code assumes it will exist in a folder called *data* at
the root of this repository).

## Manifest

- **paper\_figures.ipynb:** This is the main notebook for recreating
  all the results from Section 4 and 5 in the paper (mostly
  figures). It already includes the output from running it, so it is
  possible to inspect the generated figures without having to run the
  code.
- **overhead\_estimation.ipynb:** This notebook contains the code for
  recreating the results regarding overhead, presented in Section 3.3.
- **data\_preprocessing.ipynb:** This notebook contains code for
  processing the raw measurement data and merging into the different
  more compact format used by the *paper\_figures.ipynb* notebook. As
  the dataset on Zenodo already includes the output from running this
  notebook, there is no need to run this.
- **remove\_internal\_subnet\_structure.ipynb:** This notebook contains
  the code that was used to merge all LAN subnets from the raw data
  before publishing the dataset, in order to avoid leaking any details
  about the structure of the ISP's internal network. As the published
  data has already been run through this there is no point in running
  this code, and it has only been included for transparency.
- **histogram\_functions.py**, **plotting\_functions.py** and
  **util.py:** These files contain various python functions which the
  notebook include.
