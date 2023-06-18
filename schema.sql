CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    admin boolean DEFAULT False,
    created TIMESTAMP
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    profile_name TEXT UNIQUE NOT NULL,
    created TIMESTAMP
);



CREATE TABLE profile_informations (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER UNIQUE REFERENCES profiles,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    institution TEXT,
    city TEXT,
    country TEXT,
    motto TEXT,
    hobbies TEXT,
    status_text TEXT,
    profile_text TEXT
);
--created TIMESTAMP


CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
)


--CREATE TABLE profile_informations (
--    id SERIAL PRIMARY KEY,
--    profile_id INTEGER UNIQUE REFERENCES profiles, --UNIQUE??
--    first_name TEXT, -- NOT NULL,
--    last_name TEXT, -- NOT NULL,
--    email TEXT,
--    institution TEXT,
--    city TEXT,
--    country TEXT, --place?
--    motto TEXT,
--    hobbies TEXT,
--    status_text TEXT,
--    profile_text TEXT
    --created TIMESTAMP
--);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);
