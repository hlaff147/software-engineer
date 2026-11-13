-- Initialize isolated databases for microservices (Database-per-service pattern)
CREATE DATABASE products_db;
CREATE DATABASE inventory_db;
CREATE DATABASE reviews_db;
CREATE DATABASE orders_db;

GRANT ALL PRIVILEGES ON DATABASE products_db TO app_user;
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO app_user;
GRANT ALL PRIVILEGES ON DATABASE reviews_db TO app_user;
GRANT ALL PRIVILEGES ON DATABASE orders_db TO app_user;
