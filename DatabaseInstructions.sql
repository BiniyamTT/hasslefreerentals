-- SQLite
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    email TEXT NOT NULL,
    phonenumber TEXT NOT NULL,
    usertype TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS equipments(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    owner_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    fuel_type TEXT NOT NULL,
    hp INTEGER NOT NULL,
    year INTEGER NOT NULL,
    hourly_rate TEXT NOT NULL,
    advance TEXT NOT NULL,
    duration TEXT NOT NULL,
    location TEXT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
)
