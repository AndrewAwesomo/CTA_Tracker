# CTA_Tracker
simple CTA tracker app for RPI

<b>API key setup:</b>

* After cloning or downloading, rename api_keys_generic.txt to api_keys.txt

* Then replace the 'xxxxxxxxx' with your own CTA API keys.  Be sure to keep the single quotes as this will be
read in as a dictionary.

* If you need api keys go to the following URLs to request one for the Train Tracker and one for the Bus Tracker

1. Train tracker: http://www.transitchicago.com/developers/traintrackerapply.aspx

2. Bus tracker: You will need to create a developer account here: http://www.ctabustracker.com/bustime/login.jsp
Then go to http://www.ctabustracker.com/bustime/updateDeveloper.jsp or click the "My API" button next to "Sign Out"
in the upper right hand corner of your account page.  You can then register for an API key.


<b>Trains and Bus setup:</b>

* You can set up one route and station and the app will return train ETAs for both route directions.

1. Find your stop by opening stops.txt in Excel.  Do this by opening an instance of Excel then go to
Data -> Get Data -> From File -> From Text/CSV.

2. Then navigate to stops.txt and click 'Import'.  When the new window
opens, click 'Load'.

2. Use the 'Find' function or press ctrl+f to open the 'Find' dialog box.

3. Search for your stop: i.e. 'California (Blue)' or 'Kimball' or 'California (Green)' etc.  Note the 'stop_id'
 corresponding to your stop.

4. Edit cta_tracker.py:  replace 41410 in TRAIN_STATION variable with your 'stop_id'

Train tracking should now be set


* You can set up multiple bus stations (up to 10) by replacing 563,615,5500,5525 in the BUS_STATION with comma
separated station IDs.

1. Find station IDs by going to the CTA Bus tracker app and locating your route and direction and make note of the
corresponding station ID:  http://www.ctabustracker.com/bustime/eta/eta.jsp

2. Once you select the Route, Direction, and Stop the stop ID will be populated in the 'Find by Stop' in the top left
of the window.

3. Enter up to 10 of these in the BUS_STATION variable.  You should be all set.


<b>Refresh interval</b>

* Lastly, you can adjust the interval between updates by changing the UPDATE_TIME variable to the number of seconds
you want between updates.


Enjoy.

