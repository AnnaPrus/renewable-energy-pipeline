with base as (

    select * from {{ ref('energy_long') }}

),

pivoted as (

    select
        utc_timestamp,
        country,
        sum(case when metric = 'load' then value end) as load,
        sum(case when metric = 'solar' then value end) as solar,
        sum(case when metric = 'wind' then value end) as wind
    from base
    group by 1, 2

),

final as (

    select
        utc_timestamp,
        country,
        load,
        solar,
        wind,

        (solar + wind) as renewable_generation,

        (solar + wind) / nullif(load, 0) as renewable_share,

        load - (solar + wind) as energy_gap,

        solar / nullif(solar + wind, 0) as solar_share,
        wind / nullif(solar + wind, 0) as wind_share,

        (load - (solar + wind)) / nullif(load, 0) as deficit_ratio,

        case 
            when (solar + wind) >= load then 1 else 0 
        end as is_renewable_dominant,

        case 
            when load > avg(load) over (partition by country) 
            then 1 else 0 
        end as is_peak_load

    from pivoted

)

select * from final