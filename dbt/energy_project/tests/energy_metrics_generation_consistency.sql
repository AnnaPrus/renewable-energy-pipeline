select *
from {{ ref('energy_metrics') }}
where abs(renewable_generation - (solar + wind)) > 0.0001
