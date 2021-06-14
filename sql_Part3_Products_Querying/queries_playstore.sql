-- Comments in SQL Start with dash-dash --

--Find the app with an ID of 1880.
playstore=# SELECT * FROM analytics WHERE id = 1880;
  id  |        app_name         |   category   | rating | reviews |        size        | min_installs | price | content_rating |     genres     | last_updated | current_version |  android_version   
------+-------------------------+--------------+--------+---------+--------------------+--------------+-------+----------------+----------------+--------------+-----------------+--------------------
 1880 | Web Browser for Android | PRODUCTIVITY |    4.3 |  144879 | Varies with device |     10000000 |     0 | Everyone       | {Productivity} | 2016-01-24   | 3.5.0           | Varies with device
(1 row)

--Find the ID and app name for all apps that were last updated on August 01, 2018.
playstore=# SELECT id, app_name FROM analytics WHERE last_updated = '2018-08-01';
  id  |                                     app_name                                      
------+-----------------------------------------------------------------------------------
   10 | Clash Royale
   11 | Candy Crush Saga
   12 | UC Browser - Fast Download Private & Secure
   74 | Score! Hero
  101 | Tiny Flashlight + LED
  102 | Crossy Road
  103 | SimCity BuildIt
  111 | FIFA Soccer
  112 | Angry Birds 2
  125 | Need for Speed™ No Limits
etc....

--Count the number of apps in each category, e.g. “Family | 1972”.
playstore=# SELECT category, COUNT(*) FROM analytics GROUP BY category;
 
      category       | count 
---------------------+-------
 BOOKS_AND_REFERENCE |   191
 COMMUNICATION       |   342
 BEAUTY              |    46
 EVENTS              |    52
 PARENTING           |    59
 PHOTOGRAPHY         |   313
 GAME                |  1110
 BUSINESS            |   313
 SOCIAL              |   269
 MEDICAL             |   350
etc....
(33 rows)

--Find the top 5 most-reviewed apps and the number of reviews for each.
playstore=# SELECT app_name, reviews FROM analytics ORDER BY reviews DESC LIMIT 5;
                 app_name                 | reviews  
------------------------------------------+----------
 Facebook                                 | 78158306
 WhatsApp Messenger                       | 78128208
 Instagram                                | 69119316
 Messenger – Text and Video Chat for Free | 69119316
 Clash of Clans                           | 69109672
(5 rows)

OR 
playstore=# SELECT * FROM analytics ORDER BY reviews DESC LIMIT 5;

--Find the app that has the most reviews with a rating greater than equal to 4.8.
playstore=#  SELECT * FROM analytics WHERE rating >= 4.8 ORDER BY reviews DESC LIMIT 1;
 id  |  app_name  |      category      | rating | reviews |        size        | min_installs | price | content_rating |        genres        | last_updated |  current_version   |  android_version   
-----+------------+--------------------+--------+---------+--------------------+--------------+-------+----------------+----------------------+--------------+--------------------+--------------------
 260 | Chess Free | HEALTH_AND_FITNESS |    4.8 | 4559407 | Varies with device |    100000000 |     0 | Everyone       | {"Health & Fitness"} | 2018-08-01   | Varies with device | Varies with device
(1 row)
(END)

--Find the average rating for each category ordered by the highest rated to lowest rated.
playstore=# SELECT category, AVG(rating) FROM analytics GROUP BY category ORDER BY AVG(rating) DESC;
      category       |        avg         
---------------------+--------------------
 EVENTS              |  4.395238104320708
 EDUCATION           |   4.38903223006956
 ART_AND_DESIGN      |  4.347540949211746
 BOOKS_AND_REFERENCE | 4.3423728633061645
 PERSONALIZATION     |    4.3283387457509
 BEAUTY              |  4.299999970656175
 GAME                |  4.287167731498383
 PARENTING           |  4.285714266251545
 HEALTH_AND_FITNESS  | 4.2743944663902464
 etc...
(33 rows)

--Find the name, price, and rating of the most expensive app with a rating that’s less than 3.
playstore=# SELECT app_name, price, rating FROM analytics WHERE rating < 3 ORDER BY price DESC Limit 1;
      app_name      | price  | rating 
--------------------+--------+--------
 Naruto & Boruto FR | 379.99 |    2.9
(1 row)

--Find all apps with a min install not exceeding 50, that have a rating. Order your results by highest rated first.
playstore=# SELECT * FROM analytics WHERE min_installs <=50 AND rating IS NOT NULL ORDER BY rating DESC;
  id  |                    app_name                    |      category       | rating | reviews | size | min_installs | price | content_rating |        genres         | last_updated |  current_version   | android_version 
------+------------------------------------------------+---------------------+--------+---------+------+--------------+-------+----------------+-----------------------+--------------+--------------------+-----------------
 9468 | DT                                             | FAMILY              |      5 |       4 | 52M  |           50 |     0 | Everyone       | {Education}           | 2018-04-03   | 1.1                | 4.1 and up
 9464 | DQ Akses                                       | PERSONALIZATION     |      5 |       4 | 31M  |           50 |  0.99 | Everyone       | {Personalization}     | 2018-04-27   | 1.1                | 4.1 and up
 9453 | DM Adventure                                   | MEDICAL             |      5 |       4 | 25M  |            1 |     0 | Everyone       | {Medical}             | 2018-08-02   | 1.0.72             | 4.0.3 and up
 9427 | db Meter - sound level meter with data logging | GAME                |      5 |       5 | 4.6M |           10 |     0 | Everyone       | {Racing}              |
 etc....

--Find the names of all apps that are rated less than 3 with at least 10000 reviews.
playstore=# SELECT app_name FROM analytics WHERE rating < 3 AND reviews >= 10000; 
                    app_name                     
-------------------------------------------------
 The Wall Street Journal: Business & Market News
 Vikings: an Archer’s Journey
 Shoot Em Down Free
(3 rows)

--Find the top 10 most-reviewed apps that cost between 10 cents and a dollar.
playstore=# SELECT app_name FROM analytics WHERE price BETWEEN 0.10 AND 1 ORDER BY reviews DESC LIMIT 10;
                  app_name                   
---------------------------------------------
 Free Slideshow Maker & Video Editor
 Couple - Relationship App
 Anime X Wallpaper
 Dance On Mobile
 Marvel Unlimited
 FastMeet: Chat, Dating, Love
 IHG®: Hotel Deals & Rewards
 Live Weather & Daily Local Weather Forecast
 DreamMapper
 Můj T-Mobile Business
(10 rows)

OR
playstore=# SELECT * FROM analytics WHERE price BETWEEN 0.10 AND 1 ORDER BY reviews DESC LIMIT 10;

--Find the most out of date app. Hint: You don’t need to do it this way, but it’s possible to do with a subquery: http://www.postgresqltutorial.com/postgresql-max-function/
playstore=# SELECT * FROM analytics ORDER BY last_updated LIMIT 1;
  id  |  app_name  | category | rating | reviews | size | min_installs | price | content_rating |     genres      | last_updated | current_version | android_version 
------+------------+----------+--------+---------+------+--------------+-------+----------------+-----------------+--------------+-----------------+-----------------
 5701 | CP Clicker | FAMILY   |    4.2 |    1415 | 209k |       100000 |     0 | Everyone       | {Entertainment} | 2010-05-21   | 3.1             | 1.5 and up
(1 row)

--Find the most expensive app (the query is very similar to #11).
playstore=# SELECT * FROM analytics ORDER BY price DESC LIMIT 1;
  id  |      app_name      | category  | rating | reviews | size | min_installs | price | content_rating |   genres    | last_updated | current_version | android_version 
------+--------------------+-----------+--------+---------+------+--------------+-------+----------------+-------------+--------------+-----------------+-----------------
 6766 | Cardi B Piano Game | LIFESTYLE |    3.6 |     275 | 7.3M |        10000 |   400 | Everyone       | {Lifestyle} | 2018-05-03   | 1.0.1           | 4.1 and up
(1 row)

--Count all the reviews in the Google Play Store.
playstore=# SELECT SUM(reviews) FROM analytics; 
    sum     
------------
 4814575866
(1 row)

--Find all the categories that have more than 300 apps in them.
playstore=# SELECT category FROM analytics GROUP BY category HAVING COUNT(*) > 300;
    category     
-----------------
 COMMUNICATION
 PHOTOGRAPHY
 GAME
 BUSINESS
 MEDICAL
 TOOLS
 LIFESTYLE
 PRODUCTIVITY
 PERSONALIZATION
 FINANCE
 SPORTS
 FAMILY
(12 rows)

--Find the app that has the highest proportion of min_installs to reviews, among apps that have been installed at least 100,000 times. Display the name of the app along with the number of reviews, the min_installs, and the proportion.
playstore=# SELECT app_name, reviews, min_installs,  min_installs / reviews AS proportion FROM analytics WHERE min_installs >= 100000 ORDER BY proportion DESC LIMIT 1;
 
     app_name     | reviews | min_installs | proportion 
------------------+---------+--------------+------------
 Kim Bu Youtuber? |      66 |     10000000 |     151515
(1 row)
