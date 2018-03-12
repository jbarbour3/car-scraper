# car-scraper
A Project to gather data on the used car market in Georgia and the surround area.


Monthly
-Get latest list of dealerships from ga sos business license site
    http://verify.sos.ga.gov/Verification/Search.aspx?facility=Y&SubmitComplaint=Y
-Check for additional cities on CL

if needed add dealers/cities to site

Daily
-Query all sites for all cars in the 'cars to search' file for classifieds
-Parse the data from each individual site page
-Store the results in a file with the date

State of Georgia License lookup site
http://verify.sos.ga.gov/Verification/Search.aspx?facility=Y&SubmitComplaint=Y


TODO:
1. Create initial set of search url strings
2. Create a proxy scheme that will allow us to execute all the scraping without being blocked
3. Decide on how daily parsing will be executed(what resource will execute it, where will results be saved, etc.)