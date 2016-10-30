# Galvanize Data Science Immersive Program Final Project

# Trouble Brewing: Predicting the Next Generation of Optimal Coffee-growing Regions Due To Environmental Changes

[![alt text](https://github.com/samuelcheang0419/trouble-brewing/blob/master/Coffea-brassii-screenshot.png)](https://cdn.rawgit.com/samuelcheang0419/trouble-brewing/master/Coffea%20brassii%20(J.-F.Leroy)%20A.P.Davis_current.html)
Recommendation map for Coffea brassii, [Australia's only native coffee species and a subject of discussion among the coffee industry in the past few years](http://www.news.com.au/national/scientists-perked-up-by-aussie-coffee-bean-coffea-brassii-found-at-cape-york/story-e6frfkvr-1226044210772). 

Legend
- Green: current locations growing Coffea brassii
- Red: highly recommended locations to grow Coffea brassii
- Light yellow: recommended locations to grow Coffea brassii

## Motivation behind project:
Coffee quality and production is highly susceptible to various environmental factors, including temperature, rainfall, elevation, and soil condition etc. Demand for coffee is continually growing, with the International Coffee Organization (ICO) estimating an increase by approximately 25% from 2015 to 2020 [1]. This is met with increased unpredictability and decreased quantity of supply by most coffee-producing countries (e.g. Colombia, Brazil etc.) due to shifts in environmental patterns.

For instance, Nicaraguan coffee farmers report that the change in seasonal rainfall over the past 20 years has led to erratic flowering and incomplete maturation of coffee beans [7].

As coffee plantations have a lifespan of about thirty years (some up to fifty years), it is imperative for countries that rely heavily on coffee exports to plan ahead and identify optimal locations for coffee growth. [4]

The methodologies used in this project can be applied to any organism affected by environmental changes.

## Datasource:
http://www.gbif.org/occurrence/search?taxon_key=2895315&HAS_COORDINATE=true&HAS_GEOSPATIAL_ISSUE=false&YEAR.offset=0&offset=20#
Search for:
- Scientific Name = 'Coffea L.'
- Location = 'Georeferenced records only' and 'With NO known coordinate issues'
Returned 7167 results at time of project

## My approach:
- To develop a feasibility study for justifying this project (or to reference sources online)
- To identify key factors that influence coffee growth (e.g. soil condition, CO2 concentration, elevation, temperature, day-night difference, humidity etc.)
- To identify regions suitable for coffee production, depending on coffee species (Coffea arabica and Coffea canephora make up the majority of coffee consumed by the world, but there are many other species that are planted for cross-breeding/biodiversity purposes)
- To develop a recommender system (non-negative matrix factorization) based on coffee species and locations to:
    - predict suitable regions of growth for each species
    - identify optimal environmental conditions for each species (in combination with recent environmental data of locations)
- To develop a predictive model for future environmental factors (factors to be based on identified key factors) based on location
- To develop a similarity matrix between various regions (even regions that have not occurred in my original dataset) based on my environmental prediction model

## Day-to-day tasks:
10/1/2016:

10/2/2016:
As almost all of my rows have different longitude/latitude values, my recommender system would have a lot of different locations. I decided to use Google Map's geocode API to reverse geocode my longitude/latitude points into countries and regions and integrate this new information into my dataframe. Granted, the original dataset has a 'locality' column that describes the general location of where the coffee tree was found, but the descriptions are not very useful for my purposes (e.g. 'Indiera Alta.', 'Bo. Florida Adentro, trail N up limestone hill.  0.5 km along dirt road E. of old quarry at Rt 140, km 50.75.'). I just need a city name.
