select
    utc_timestamp,
    country,
    count(*) as row_count
from {{ ref('energy_metrics') }}
group by 1, 2
having count(*) > 1
