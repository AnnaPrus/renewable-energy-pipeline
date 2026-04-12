select *
from {{ ref('energy_metrics') }}
where abs(energy_gap - (load - renewable_generation)) > 0.0001
