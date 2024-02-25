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
    Farm_Acre DECIMAL,
    Irrigation_Source TEXT,
    User_id TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for crop allocation
CREATE TABLE IF NOT EXISTS crop_allocation (
    crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Crop_Name TEXT,
    Crop_Quantity DECIMAL,
    User_id TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for seeds data
CREATE TABLE IF NOT EXISTS seed (
    Seed_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Seed_Name TEXT,
    Quantity DECIMAL,
    Seed_Price DECIMAL,
    User_id TEXT,
    Crop_Name TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for pesticides data
CREATE TABLE IF NOT EXISTS pesticide (
    Pesticide_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Pesticide_Name TEXT,
    Quantity DECIMAL,
    Pesticide_Price DECIMAL,
    User_id TEXT,
    Crop_Name TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for fertilizers data
CREATE TABLE IF NOT EXISTS fertilizer (
    Fertilizer_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Fertilizer_Name TEXT,
    Quantity DECIMAL,
    Fertilizer_Price DECIMAL,
    User_id TEXT,
    Crop_Name TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for labor data
CREATE TABLE IF NOT EXISTS labour (
    Labour_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    First_Name TEXT,
    Last_Name TEXT,
    Address TEXT,
    Contact_No INTEGER,
    work TEXT,
    Working_Hours TEXT,
    Salary DECIMAL,
    User_id TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for warehouse data
CREATE TABLE IF NOT EXISTS warehouse (
    Warehouse_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_stored TEXT,
    Total_Capacity DECIMAL,
    User_id TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);

-- Create table for crop market data
CREATE TABLE IF NOT EXISTS crop_market (
    Market_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Address TEXT,
    Selling_Quantity DECIMAL,
    Selling_Price DECIMAL,
    User_id TEXT,
    Crop_Name TEXT,
    Selling_Date TEXT,
    FOREIGN KEY (User_id) REFERENCES farmer(User_id)
);
