select *
from {{ ref('energy_metrics') }}
where renewable_share < 0
