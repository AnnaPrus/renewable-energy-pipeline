with base as (

    select * from {{ ref('energy_metrics') }}

),

daily as (

    select
        date(utc_timestamp) as date,
        country,

        avg(load) as avg_load,
        avg(renewable_generation) as avg_renewable_generation,
        avg(renewable_share) as avg_renewable_share,
        avg(energy_gap) as avg_energy_gap

    from base
    group by 1, 2

)

select * from daily