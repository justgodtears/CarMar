### TODO
1. Database with all voivodeships as batch data with historical information. Date range is 01.01.2000 - 20.05.2026. ✅
<h6> Done. Saved as only_cars table. Filtered to only passenger cars</h6>

2. ~~Automatic daily API fetching to keep the database up to date.~~
<h6> Deprecated </h6>
3. Frontend for statistical analytics built with ~~Reflex~~ Streamlit.
4. Daily stats of newly registered cars from previous days. (i.e. nr.2 but its needs to be done later)
5. Incremental data loading — fetch only new registrations (delta), not a full reload every day.
6. Data quality checks — handle dirty records (invalid dates, misspelled brand names, missing values).
7. Historical snapshots — ability to compare fleet state across time (e.g. this year vs. last year).
8. Regional breakdown by powiat — not just voivodeship-level aggregations.
9. Fuel type trend analysis — tracking EV/hybrid penetration over time.
10. Enrichment with external data sources (GUS, fuel prices, demographics).


### What we have now
First batch of data. Currently testing the utility of all columns. Simple DataFrame with filtering for cars younger than 27 years old.