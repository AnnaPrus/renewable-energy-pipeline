select
    cast(utc_timestamp as timestamp) as utc_timestamp,

    -- Germany
    DE_load_actual_entsoe_transparency as load_de,
    DE_solar_generation_actual as solar_de,
    DE_wind_onshore_generation_actual as wind_de,

    -- Austria
    AT_load_actual_entsoe_transparency as load_at,
    AT_solar_generation_actual as solar_at,
    AT_wind_onshore_generation_actual as wind_at

from {{ source('energy', 'energy_clean') }}