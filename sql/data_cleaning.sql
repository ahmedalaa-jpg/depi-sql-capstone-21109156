-- 1. Text Standardization & Whitespace Removal (TRIM)

-- Clean customers table
UPDATE customers 
SET customer_city = LOWER(TRIM(customer_city)), 
    customer_state = UPPER(TRIM(customer_state)),
    customer_unique_id = TRIM(customer_unique_id);

-- Clean sellers table
UPDATE sellers 
SET seller_city = LOWER(TRIM(seller_city)), 
    seller_state = UPPER(TRIM(seller_state));

-- Clean order payments table
UPDATE order_payments 
SET payment_type = LOWER(TRIM(payment_type));

-- Clean closed deals table
UPDATE closed_deals
SET business_segment = LOWER(TRIM(business_segment)),
    business_type = LOWER(TRIM(business_type)),
    lead_type = LOWER(TRIM(lead_type));

-- 2. Deduplication (Fast Window Function Approach)

-- Delete exact duplicates using ROW_NUMBER() CTE (Executes in < 1 second)
WITH duplicates AS (
    SELECT ctid,
           ROW_NUMBER() OVER (
               PARTITION BY order_id, payment_sequential, payment_type, payment_installments, payment_value
               ORDER BY ctid
           ) AS rn
    FROM order_payments
)
DELETE FROM order_payments
WHERE ctid IN (SELECT ctid FROM duplicates WHERE rn > 1);