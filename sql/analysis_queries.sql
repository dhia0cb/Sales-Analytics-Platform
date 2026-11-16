
-- 1. Display all sales records

SELECT *
FROM sales;


-- 2. Calculate total revenue

SELECT SUM(revenue) AS total_revenue
FROM sales;


-- 3. Calculate total profit

SELECT SUM(profit) AS total_profit
FROM sales;


-- 4. Revenue by category

SELECT
    category,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;


-- 5. Revenue by region

SELECT
    region,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;


-- 6. Top 5 products

SELECT
    product,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC;



-- 7. Monthly revenue

SELECT
    order_month,
    SUM(revenue) AS monthly_revenue
FROM sales
GROUP BY order_month
ORDER BY order_month;


-- 8. Average profit margin

SELECT
    AVG(profit_margin_pct) AS average_profit_margin
FROM sales;
