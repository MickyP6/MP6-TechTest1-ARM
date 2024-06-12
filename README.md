## For Task 1: Python application for Google Trend Data

Requirements:
`Docker version 24.0.0+`

Bash terminal in the local repo:

`$docker compose up --build`

Wait while it loads, when finished it should look like this:
![image](https://github.com/MickyP6/AllResponseMedia-Test/assets/172441098/1c2c14be-5562-48fb-8440-03ac38603b23)
It may take a little longer on the first pull.

In a web browser open

`localhost:5000`

It will then open the page and look like this:
![image](https://github.com/MickyP6/AllResponseMedia-Test/assets/172441098/50a3b0fd-30a9-4542-bbf6-a6ba61cf16a3)

To shutdown the server:

`CTRL+C`

To remove the container and network:

`docker compose down`

## For Task 2: Sql

In the root directory, please take a look at file `sql_task.sql`.

Note: since no googling was allowed and I have not used t-sql, I have written this in psql under the assumption that the syntax is similar given that t-sql is an extention of sql.
Briefly, the thought process was to minimise the number of times the table was queried. The datetime was offset by 1 row per group in order to search against itself for offending
overlaps:
![image](https://github.com/MickyP6/MP6-TechTest1-ARM/assets/172441098/508034e0-db16-4d58-9e88-61747bb3b29e)

A reverse index was also created to speed up time range queries under the assumption that this table would be much larger 100k+ records)
