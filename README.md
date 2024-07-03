# Lab UI
setup environment to build and work with pyhon.
#this command executed fom conda will crete an ENV with all the correct packages required

conda env create --name labui --file=package.yml
conda activate labui


The lab UI can be used for plotting fermentation curves, ABV & DO control charts, generating batch reports, and optimizing OG targets. It has the following functions and requires the following reports:

Fermentation curves:
Standard curves of gravity (deg P) and days since brew to visualize the trend in gravities by brand.
Requires ekos reports: BAX Ferm Log
Python script: Fermentation_Curves

ABV control chart:
Individual and moving range plot of ABV by brand to assess consistency and to determine if our ABVs are in spec.
Requires excel sheets: ABV Tracking
Python script: ABV_control_chart

DO control chart:
Individual and moving range plot of DO by brand to assess consistency and spot outliers.
Requires ekos reports: BAX Conditioning Log
Python script: DO_control_chart

Batch reports:
Compiling data from ferm logs, micro, Anton Paar, DO, CO2, brew sheets into one report by batch number
Requires ekos reports: BAX Ferm Log, BAX Conditioning Log
Requires excel sheets: ABV Tracking, Micro Results Tracking, brewsheets
Python script: Batch_History

OG targets:
Calculates constants (m & b) to fit the equation: RDF * OG = m * ABV + b and uses average RDF and target ABV to calculate target OG by brand.
Requires ekos report: BAX OG by batch
Python script: OG_optimization

Other python scripts:
AP_Hydrometer_R2: correlation between hydrometer gravities and anton paar gravities
Delta_Gravity: calculates the difference between FG, package gravity, and library gravity
DOavg: calculates average brite DO for lagers v ales
Malt_Analysis: haven't used this since 2022 but it was made to track the relation between 2 row lot extract % and BH efficiency
Sensory: calculates sensory participation stats using DraughtLabs reports
