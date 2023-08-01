# CHECK24-GenDev

This project is part of the CHECK24 GenDev Holiday Challenge.
The app is built with a SvelteKit frontend, a FastAPI backend interfaced with a PostgreSQL database, and also incorporates a Redis cache for performance enhancement.

## About

### Database

PostgreSQL database with 2 utilized tables: `hotels` and `offers_1`.
The data was loaded into the database with the same schema as that of the CSV file.

To enable a quick search, I used an indexing method using a B-Tree. The specific index is:

<details> 
<summary>index</summary>
`"idx_offers_optimized_new_2" btree (outbounddepartureairport, countadults, countchildren, outbounddeparturedatetime, inboundarrivaldatetime, hotelid DESC)`
</details>

<details>
  <summary>offers table</summary>
```
                                 Table "public.offers_1"
          Column           |            Type             | Collation | Nullable | Default
---------------------------+-----------------------------+-----------+----------+---------
 hotelid                   | integer                     |           |          |
 outbounddeparturedatetime | timestamp without time zone |           |          |
 inbounddeparturedatetime  | text                        |           |          |
 countadults               | integer                     |           |          |
 countchildren             | integer                     |           |          |
 price                     | integer                     |           |          |
 inbounddepartureairport   | text                        |           |          |
 outboundarrivalairport    | text                        |           |          |
 inboundarrivaldatetime    | timestamp without time zone |           |          |
 outbounddepartureairport  | text                        |           |          |
 inboundarrivalairport     | text                        |           |          |
 outboundarrivaldatetime   | text                        |           |          |
 mealtype                  | text                        |           |          |
 oceanview                 | boolean                     |           |          |
 roomtype                  | text                        |           |          |
Indexes:
    "idx_offers_optimized_new_2" btree (outbounddepartureairport, countadults, countchildren, outbounddeparturedatetime, inboundarrivaldatetime, hotelid DESC)
```

</details>

### Backend

Das Backend ist in Python mit FastAPI geschrieben. Es kann sich unter URL `http://localhost:xxxx/docs` die doku der Endpointe angeschaut werden.

### Cache

FastAPI uses a Redis cache to temporarily store results from OpenAI queries and database queries. The database itself already does a good job at caching, but the Redis cache proves to be very helpful when working with the OpenAI API. This would be extremely advantageous in a real-world scenario, to optimize costs associated with using the OpenAI API.

### Frontend

The frontend utilizes the SvelteKit framework. SvelteKit is built on Svelte, but offers server-side rendering and features like routing out of the box. For styling, I predominantly use TailwindCSS and Flowbite's components.
When designing the frontend, it was important to me that the UI is relatively pleasing, but most importantly, the user interface is clear and easily understandable.

### Additional Features

#### OpenAI

- Initially, I assumed that there would be multiple travel destinations, so I devised a function that would make it easier for the user to search for targets. In the search field, the user can not only search for destinations like Mallorca or Paris, but also for features like a beach, etc. For example, they can search for "I want to go to the beach". To test other destinations, you could search for "City break by the sea", "I want to go to a historical city", etc. However, I still think the function is a good idea, so I kept it in.

- I implemented another function with OpenAI. This generates a travel recommendation based on the destination, date, and number of people. This recommendation is displayed between the offers.
- For detailed functionality and the predefined prompts, see controller.py.

_Note: The OpenAI API is relatively slow, so these functions always take a bit of time._

#### Filter: hotel offer page

- On the page for all offers of a hotel, you can filter by price and date, in both ascending and descending order.

### Optimizations

Speed:

- Database indexing
- Database queries are cached using Redis
- OpenAI queries are cached using Redis

Further optimizations:

- Docker

### Notes

- currently, only one airport per search is supported

### Improvements that could be implemented

- Adjusting the database schema
- Additional filter options for search
