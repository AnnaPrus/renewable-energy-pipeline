with base as (

    select *
    from {{ ref('stg_energy') }}

)

select
    timestamp,
    'DE' as country,
    load_de as load,
    solar_de as solar,
    wind_de as wind
from base

union all

select
    timestamp,
    'AT' as country,
    load_at as load,
    solar_at as solar,
    wind_at as wind
from base