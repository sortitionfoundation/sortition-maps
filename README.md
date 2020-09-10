# sortition-maps
Code to generate maps of sortition activities, for the Sortition Foundation website and general visualisation.

## Contents
* sortition-around-the-globe: Folder of code related to maps for the SF website.
	* sortition-around-the-globe.js: init_map() function to be copied to the website. Be sure to add the API key when doing so.
	* text-test.js: javascript with snippets copied from the above to test the generating and formatting of text content for the map. API key for test purposes will be read from a file called api-key.js. For security, this file is not stored in the repo.
	* api-key.js.example: Rename this api-key.js and insert your own API key to use text-test.js.
	* test.html: An html file used to run text-test.js
	* add_latlng_to_OECD.py: Python script used to augment the OECD database with latitude and longitude data.
	* OECD.csv: A copy of the OECD's database of deliberative democracy activities.
