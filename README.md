# Automatic detection for fake profiles in dating platforms

This is a basic analysis and model implemntation of a classifer for online dating platforms to detect scammers

### Data extraction
The scrapper code can be found under data_extraction directory. This is not my code but just used the scraper from https://github.com/gsuareztangil/automatic-romancescam-digger with a few modifications


### Data analysis

* id_assignment.ipynb: To assign ids to each profile
* scam_analysis.ipynb: Analysis for demographic data of dating profiles
* description_translation.ipynb: Preparing the profile descriptions for analysis
* description_analysis.ipynb: Basic analysis over the profiles description
* image_analysis.png: Detecing objects in profiles using ImageAi python package
* regression.ipynb: Basic regression model. 