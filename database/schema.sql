-- Banner Table
CREATE TABLE IF NOT EXISTS banners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    image TEXT,
    display_order INTEGER,
    status TEXT
);

-- Vision & Mission Table
CREATE TABLE IF NOT EXISTS vision_mission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vision_title TEXT,
    vision_description TEXT,
    mission_title TEXT,
    mission_description TEXT
);

-- Statistics Table
CREATE TABLE IF NOT EXISTS statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT,
    value TEXT,
    display_order INTEGER,
    status TEXT
);

-- Initiatives Table
CREATE TABLE IF NOT EXISTS initiatives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    image TEXT,
    status TEXT
);

-- Our Story Table
CREATE TABLE IF NOT EXISTS our_story (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
);



-- Programs Table
CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

-- Team Members Table
CREATE TABLE IF NOT EXISTS team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    designation TEXT,
    image TEXT
);

CREATE TABLE IF NOT EXISTS core_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);