SET work_mem = '4096MB';
SHOW work_mem;
COPY offers (
    hotelid,
    outbounddeparturedatetime,
    inbounddeparturedatetime,
    countadults,
    countchildren,
    price,
    inbounddepartureairport,
    inboundarrivalairport,
    inboundarrivaldatetime,
    outbounddepartureairport,
    outboundarrivalairport,
    outboundarrivaldatetime,
    mealtype,
    oceanview,
    roomtype
)
FROM '/offers.csv' DELIMITER ',' CSV HEADER;
RESET work_mem;