COPY atms(id, latitude, longitude)
FROM '/tmp/files/atms.csv' CSV DELIMITER '|' NULL AS 'None' HEADER;

COPY companies(id, "type", "name", country)
FROM '/tmp/files/companies.csv' CSV DELIMITER '|' NULL AS 'None' HEADER;

COPY clients(id, first_name, last_name, age, email, occupation, political_views, nationality, university, academic_degree, "address", postal_code, country, city)
FROM '/tmp/files/clients.csv' CSV DELIMITER '|' NULL AS 'None' HEADER;

COPY transactions(id, source, "target", "date", "time", amount, currency)
FROM '/tmp/files/transactions.csv' CSV DELIMITER '|' NULL AS 'None' HEADER;
