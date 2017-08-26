# dwd_climate_diagram
## Purpose
This project provides a python and gnuplot script to generate climate diagrams.
## Data
### Original Data Source
The data are retreived from the Climate Data Centre CDC by the German National Weather Forecast Agency Deutscher Wetterdienst (DWD). You can download all data sets on the CDC FTP server ( ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/monthly/more_precip/historical/ ). Please adhere to their  terms of use ( ftp://ftp-cdc.dwd.de/pub/CDC/Terms_of_use.txt ) (german: ftp://ftp-cdc.dwd.de/pub/CDC/Nutzungsbedingungen_German.txt ).
### Processed Data for Climate Diagrams
The [python script](generate_gnuplot_and_datafile.py) computes the average temperature and precipitation for each station and each month over 30 years. If any single of the 30·2·2=720 required data points is missing, the computation is aborted. Note that some of the old and most of the newer stations (DWD index >≈ 06000) do not match these criteria. That is why CSV data sets for some stations are missing and some only contain data ranging from the years 1905 – 1935 for instance as there was no recent continuous 30 year frame.
## Generation of SVG files
The python script takes the [Gnuplot template file](template.gpl) and replaces the placeholders within with station specific data files and meta information such as latitude, longitude or the time interval shown.
## results
All SVG files are provided on [Wikimedia Comons](https://commons.wikimedia.org/wiki/Special:ListFiles?limit=500&user=Der-blaue-elefant&ilshowall=0) uploaded by user der-blaue-elefant in the category "Climate diagrams of Germany".
