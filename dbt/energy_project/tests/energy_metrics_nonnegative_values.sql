select *
from {{ ref('energy_metrics') }}
where load < 0
   or solar < 0
   or wind < 0
   or renewable_generation < 0
