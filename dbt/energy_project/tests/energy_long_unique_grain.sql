select
    utc_timestamp,
    country,
    metric,
    count(*) as row_count
from {{ ref('energy_long') }}
group by 1, 2, 3
having count(*) > 1
