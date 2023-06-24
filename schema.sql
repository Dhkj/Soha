CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    admin boolean DEFAULT False,
    created TIMESTAMP
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    profile_name TEXT UNIQUE NOT NULL,
    created TIMESTAMP
);

CREATE TABLE profile_informations (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER UNIQUE REFERENCES profiles ON DELETE CASCADE,
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

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    content TEXT,
    profile_id INTEGER REFERENCES profiles ON DELETE CASCADE, --necessary?
    sent_at TIMESTAMP
);

-- Currently not implemented:
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    profile_id INTEGER REFERENCES profiles ON DELETE CASCADE,
    post_id INTEGER REFERENCES posts ON DELETE CASCADE,
    sent_at TIMESTAMP
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER REFERENCES profiles ON DELETE CASCADE,
    post_id INTEGER REFERENCES posts ON DELETE CASCADE,
    comment_id INTEGER REFERENCES comments ON DELETE CASCADE, -- Currently not implemented.
    likes boolean DEFAULT False,
    sent_at TIMESTAMP
);

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

-- Currently not implemented:
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);
