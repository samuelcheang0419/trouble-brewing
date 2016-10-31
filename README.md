# Galvanize Data Science Immersive Program Final Project

# Trouble Brewing: Predicting the Next Generation of Optimal Coffee-growing Regions Due To Environmental Changes

[![alt text](https://github.com/samuelcheang0419/trouble-brewing/blob/master/Coffea-brassii-screenshot.png)](https://cdn.rawgit.com/samuelcheang0419/trouble-brewing/master/Coffea%20brassii%20(J.-F.Leroy)%20A.P.Davis_current.html)
***(click the map to see an interactive version of it)***

An example of a recommendation map for Coffea brassii, Australia's only native coffee species and [a subject of discussion among the coffee industry in the past few years](http://www.news.com.au/national/scientists-perked-up-by-aussie-coffee-bean-coffea-brassii-found-at-cape-york/story-e6frfkvr-1226044210772).

Legend
- Green: current locations growing Coffea brassii
- Red: highly recommended locations to grow Coffea brassii
- Light yellow: recommended locations to grow Coffea brassii

To check out a presentation I gave on this project:
- [Presentation slides](https://github.com/samuelcheang0419/trouble-brewing/blob/master/16-Sam.pdf)
- [Talk](https://github.com/samuelcheang0419/trouble-brewing/blob/master/presentation.m4v)
- [Response to questions](https://github.com/samuelcheang0419/trouble-brewing/blob/master/presentation-questions.rtf)

## Motivation
Demand for coffee is continually growing [1]. This is met with increased unpredictability and decreased quantity of supply by most coffee-producing countries (e.g. Colombia, Brazil etc.) due to shifts in environmental patterns [7].

As coffee plantations have a lifespan of about thirty years (some up to fifty years), it is imperative for countries that rely heavily on coffee exports to plan ahead and identify optimal locations for coffee growth. [4]

The methodologies used in this project can be applied to any organism affected by environmental changes.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine (or more likely an AWS EC2 instance)

### Prerequisites
The coffee biodiversity data can be found [here](http://www.gbif.org/occurrence/search?taxon_key=2895315&HAS_COORDINATE=true&HAS_GEOSPATIAL_ISSUE=false&YEAR.offset=0&offset=20#). Search for:
- Scientific Name = 'Coffea L.'
- Location = 'Georeferenced records only' and 'With NO known coordinate issues'

Returned 7167 results at time of project. Save the resulting file as 'georeferenced.csv'

The baseline and projected climate data can be found [here](http://ccafs-climate.org/data_spatial_downscaling/). Depending on the downscaling method and time periods etc., you can use different climate data. At the time of the project, I searched for:
- File Set (Empirical/Statistical Downscaling) = Delta Method IPCC AR5
- Scenario = RCP 2.6, 4.5, 6.0 and 8.5
- Model = ipsl_cm5a_lr, miroc_esm_chem, gfdl_esm2m
- Extent = Global
- Format = ASCII Grid Format
- Period = 2030s and 2050s
- Variable = Bioclimatics
- Resolution = 10 minutes

Save the resulting uncompressed asc files into a folder 'climate-data.' It may be a good idea to move everything to an AWS EC2 instance.

### Preprocessing
Fork this repository.

Run 'preprocesing.py.' It takes as input the coffee biodiversity data and saves a graphlab recommender model and cleaned coffee biodiversity data. The recommender model recommends suitable regions for various coffee species based on their similarites to other species currently grown in other locations.

Run 'climate-data-baseline.py' and 'climate-data.py.' They take as input the climate data and process the data into the same format (in the 'processed-data' folder)

Run 'combine-baseline.py' and 'combine.py.' They take as input the processed climate data from above and combine them into a format for analysis (in the 'combined-data' folder).

### Analysis
Run 'similarity.py.' It takes as input the combined climate data (baseline and projected future) from above and saves a similarity matrix of different latitude/longitude coordinates based on their bioclimatic data (in the combined-data folder as similarity_array.csv).

Run 'final_final.py.' It takes as input the similarity matrix from above and, for each coffee species, creates a csv file of recommendations (in the 'prediction-data' folder).

### Visualization
Run 'climate-plot.py' and 'recommender-plot.py.' IT takes as input the recommendation files from above and, for each coffee species, produces an interactive map of current coffee growing locations and other recommended locations (in the 'recommendations' folder).

## Acknowledgements
- CCAFS for climate data
- GBIF for coffee biodiversity data
- [Python Folium package for maps](https://github.com/python-visualization/folium)
