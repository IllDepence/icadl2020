### Analysis of cross-lingual citations in English papers

##### Main components

* 0\_data/
    * collected data and intermediate results (copy/extract files into analysis folder for use)
* 1\_data\_collection/
    * `search.py` script for initial collection of reference section entries
    * `clean_bibitems.ipynb.py` script for initial filtering of reference section entries
    * `generate_control_sample.ipynb` Jupyter notebook for generating the *random set*
* 2\_analysis/
    * scrips and Jupyer notebooks used for analysis
    * details and full results of evaluations in notebooks
* 3\_manual\_evaluation/
    * details and full results of manually performed evaluations

##### Run analyses

* `$ virtualenv venv`
* `$ source venv/bin/activate`
* `$ pip install -r requirements.txt`
* copy/extract files from `0_data/` to `2_analysis/` as needed
* `$ jupyter notebook`

##### Recreate from scratch (not necessary to run analyses/Jupyer notebooks)

* Required
    * [unarXive](https://doi.org/10.5281/zenodo.3385851) data set
    * [MAG](https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/) data set
    * [Project Academic Knowledge API key](https://msr-apis.portal.azure-api.net/products/project-academic-knowledge)
