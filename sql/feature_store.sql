-- Feature Store & Target Variable Engineering (Phase 3)

DROP TABLE IF EXISTS feature_store_olist;

CREATE TABLE feature_store_olist AS
WITH order_items_summary AS (
    SELECT 
        item.order_id,
        COUNT(item.order_item_id) AS total_items,
        SUM(item.price) AS total_price,
        SUM(item.freight_value) AS total_freight,
        MAX(seller.seller_state) AS seller_state
    FROM order_items item
    LEFT JOIN sellers seller ON item.seller_id = seller.seller_id
    GROUP BY item.order_id
),
order_payments_summary AS (
    SELECT 
        order_id,
        MAX(payment_installments) AS max_installments,
        SUM(payment_value) AS total_payment_value,
        MAX(payment_type) AS primary_payment_type
    FROM order_payments
    GROUP BY order_id
)
SELECT 
    o.order_id,
    o.customer_id,
    c.customer_state,
    ois.seller_state,
    CASE WHEN c.customer_state = ois.seller_state THEN 1 ELSE 0 END AS is_same_state,
    
    -- Delivery duration features
    EXTRACT(DAY FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) AS actual_delivery_days,
    EXTRACT(DAY FROM (o.order_estimated_delivery_date - o.order_purchase_timestamp)) AS estimated_delivery_days,
    
    -- Financial & item metrics
    COALESCE(ois.total_items, 0) AS total_items,
    COALESCE(ois.total_price, 0) AS total_price,
    COALESCE(ois.total_freight, 0) AS total_freight,
    COALESCE(ops.max_installments, 0) AS max_installments,
    COALESCE(ops.total_payment_value, 0) AS total_payment_value,
    ops.primary_payment_type,
    
    -- Target Variable: 1 if delivered after estimated date, 0 otherwise
    CASE 
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 
        ELSE 0 
    END AS is_late_delivery

FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_items_summary ois ON o.order_id = ois.order_id
LEFT JOIN order_payments_summary ops ON o.order_id = ops.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL;