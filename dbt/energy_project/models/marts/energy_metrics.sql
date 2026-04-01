select
    date(timestamp) as date,
    country,
    avg(load) as avg_load,
    avg(solar + wind) as renewable_energy,
    avg((solar + wind) / load) as renewable_share
from {{ ref('energy_long') }}
group by 1, 2