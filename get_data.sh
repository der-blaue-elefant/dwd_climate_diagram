#!/bin/bash
wget ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/monthly/kl/historical/*.zip
for archive in *.zip
do
	sid=$(echo $archive | perl -pe 's|monatswerte_KL_(\d{5})_.*|\1|')
	datafile=${sid}_data.csv
	metafile=${sid}_meta.txt
	unzip -p $archive "produkt_*" > "$datafile"
	unzip -p $archive "Metadaten_Geographie*" > "$metafile"
done
rm *.zip
