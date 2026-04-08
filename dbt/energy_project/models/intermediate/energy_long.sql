with base as (

    select * from {{ ref('stg_energy') }}

),

unpivoted as (

    select
        utc_timestamp,
        'DE' as country,
        'load' as metric,
        load_de as value
    from base

    union all

    select
        utc_timestamp,
        'DE',
        'solar',
        solar_de
    from base

    union all

    select
        utc_timestamp,
        'DE',
        'wind',
        wind_de
    from base

    union all

    select
        utc_timestamp,
        'AT',
        'load',
        load_at
    from base

    union all

    select
        utc_timestamp,
        'AT',
        'solar',
        solar_at
    from base

    union all

    select
        utc_timestamp,
        'AT',
        'wind',
        wind_at
    from base

)

select * from unpivoted
where value is not null