import psycopg2

# Maak een verbinding met de PostgreSQL-database. Staat op localhost!!
conn = psycopg2.connect(
    database="steam",
    user="postgres",
    password="@Hilversum02@",
    port="5432"
)

# Maak een cursor
c = conn.cursor()

# Voeg nieuwe kolommen toe aan de database als deze nog niet bestaan
c.execute("ALTER TABLE IF EXISTS gameproperties ADD COLUMN IF NOT EXISTS verhouding_rating float")
c.execute("ALTER TABLE IF EXISTS gameproperties ADD COLUMN IF NOT EXISTS total_reviews integer")

# Haal de positive and negative ratings op van de games en maak een verhouding ervan
def add_and_update_columns():
    # Haal de positive and negative ratings op van de games
    c.execute("SELECT appid, positive_ratings, negative_ratings FROM gameproperties")
    result = c.fetchall()

    for x in result:
        # Bereken de verhouding van positieve beoordelingen
        totaal = x[1] + x[2]
        verhouding = x[1] / totaal * 100 if totaal != 0 else 0

        # Update de nieuwe kolommen met de berekende waarden
        c.execute("UPDATE gameproperties SET verhouding_rating = %s, total_reviews = %s WHERE appid = %s", (verhouding, totaal, x[0]))

    # Commit de wijzigingen aan de database
    conn.commit()

# Roep de functie aan om de kolommen toe te voegen en bij te werken
add_and_update_columns()

# Sluit de databaseverbinding
c.close()
conn.close()
