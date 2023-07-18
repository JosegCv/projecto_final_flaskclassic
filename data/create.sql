CREATE TABLE "movements" (
	"id"	INTEGER UNIQUE,
	"date_hour"	TEXT NOT NULL,
	"currency_from"	TEXT NOT NULL,
	"quantity_from"	REAL NOT NULL,
	"currency_to"	TEXT NOT NULL,
	"quantity_to"	REAL NOT NULL,
	"unit_price"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);