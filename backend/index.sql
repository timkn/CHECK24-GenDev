CREATE INDEX index_offers_2 ON offers (
    outbounddepartureairport,
    countadults,
    countchildren,
    outbounddeparturedatetime,
    inboundarrivaldatetime,
    hotelid DESC
)