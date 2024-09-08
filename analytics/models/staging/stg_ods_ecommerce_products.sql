{{
    config(
        materialized='view'
    )
}}

with productdata as (

    select *,
    row_number() over (partition by sku, date) as rn
    from {{ source('staging', 'ods_ecommerce_products') }}
    where sku is not null

)
select
    {{ dbt_utils.generate_surrogate_key(['sku', 'date']) }} AS unique_record_id,
    cast(brand as string) as brand_name,
    cast(sku as string) as sku,
    cast(name as string) as product_name,
    cast(actual_price as numeric) as actual_price,
    cast(discounted_price as numeric) as discounted_price,
    cast(discount as numeric) as discount,
    cast(discount_percentage as numeric) as discount_percentage,
    cast(date as DATE) as record_capture_date
from productdata

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
-- {% if var('is_test_run', default=true) %}

-- limit 100

-- {% endif %}
