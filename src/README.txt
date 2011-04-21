== Import csv file ==
mongoimport --host localhost --db urlshort --collection url_2 --type csv --file top.csv --headerline --upsert