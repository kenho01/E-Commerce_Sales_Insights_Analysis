{{
    config(
        materialized='table'
    )
}}

with ecommerce_data as (
    select *
    from {{ ref('stg_ods_ecommerce_products')}}
),

dim_events as (
    select *
    from {{ ref('dim_events') }}
)

select
    ecommerce_data.unique_record_id,
    ecommerce_data.brand_name,
    ecommerce_data.sku,
    ecommerce_data.product_name,
    ecommerce_data.actual_price,
    ecommerce_data.discounted_price,
    ecommerce_data.discount,
    ecommerce_data.discount_percentage,
    ecommerce_data.record_capture_date,
    dim_events.event_name
from ecommerce_data
left join dim_events
on ecommerce_data.record_capture_date BETWEEN dim_events.start_date AND dim_events.end_date