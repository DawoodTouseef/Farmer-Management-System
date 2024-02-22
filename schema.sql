-- Create table for farmer data
CREATE TABLE IF NOT EXISTS farmer (
    F_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    F_Firstname TEXT,
    F_Lastname TEXT,
    F_Gender TEXT,
    F_Address TEXT,
    F_ContactNo TEXT,
    User_id TEXT UNIQUE,
    Password TEXT
);

-- Create table for farm data
CREATE TABLE IF NOT EXISTS farm (
    Farm_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Farm_Name TEXT,
    Farm_Location TEXT,
    Farm_Area DECIMAL,
    User_id TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for crop allocation
CREATE TABLE IF NOT EXISTS crop_allocation (
    Allocation_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Crop_Name TEXT,
    Crop_Area DECIMAL,
    User_id TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for seeds data
CREATE TABLE IF NOT EXISTS seed (
    Seed_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Seed_Name TEXT,
    Seed_Price DECIMAL,
    User_id TEXT,
    Crop_Name TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for pesticides data
CREATE TABLE IF NOT EXISTS pesticide (
    Pesticide_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Pesticide_Name TEXT,
    Pesticide_Price DECIMAL,
    User_id TEXT,
    Crop_Name TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for fertilizers data
CREATE TABLE IF NOT EXISTS fertilizer (
    Fertilizer_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Fertilizer_Name TEXT,
    Fertilizer_Price DECIMAL,
    User_id TEXT,
    Crop_Name TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for labor data
CREATE TABLE IF NOT EXISTS labour (
    Labour_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Labour_Name TEXT,
    Salary DECIMAL,
    User_id TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for warehouse data
CREATE TABLE IF NOT EXISTS warehouse (
    Warehouse_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Warehouse_Name TEXT,
    Capacity DECIMAL,
    User_id TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for crop market data
CREATE TABLE IF NOT EXISTS crop_market (
    Market_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Market_Name TEXT,
    Selling_Price DECIMAL,
    User_id TEXT,
    Crop_Name TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);
