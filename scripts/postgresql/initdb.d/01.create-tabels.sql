CREATE TABLE atms (
  id CHAR(36) NOT NULL,
  latitude REAL NOT NULL,
  longitude REAL NOT NULL,

  CONSTRAINT atms_pkey PRIMARY KEY (id)
);

CREATE TABLE companies (
  id CHAR(36) NOT NULL,
  "type" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  country CHAR(50) NOT NULL,

  CONSTRAINT companies_pkey PRIMARY KEY (id)
);

CREATE TABLE clients (
  id CHAR(36) NOT NULL,
  first_name CHAR(50) NOT NULL,
  last_name CHAR(50) NOT NULL,
  age INT NOT NULL,
  email CHAR(50) NOT NULL,
  occupation TEXT NOT NULL,
  political_views TEXT NOT NULL,
  nationality CHAR(50) NOT NULL,
  university CHAR(200) NOT NULL,
  academic_degree CHAR(50),
  "address" TEXT NOT NULL,
  postal_code INT NOT NULL,
  country char(50) NOT NULL,
  city CHAR(50) NOT NULL,

  CONSTRAINT clients_pkey PRIMARY KEY (id)
);

CREATE TABLE transactions (
  id CHAR(36) NOT NULL,
  source CHAR(36) NOT NULL,
  "target" CHAR(36) NOT NULL,
  "date" DATE NOT NULL,
  "time" CHAR(16) NOT NULL,
  amount REAL NOT NULL,
  currency CHAR(3),

  CONSTRAINT transactions_pkey PRIMARY KEY (id)
);
