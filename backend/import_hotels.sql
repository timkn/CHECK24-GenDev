COPY hotels (id, name, stars)
FROM '/hotelsa.csv' DELIMITER ';' CSV HEADER;