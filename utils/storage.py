import os
import psycopg2
from psycopg2 import sql
import logging

logger = logging.getLogger('discord')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except Exception as e:
        logger.error("Fehler beim Verbinden mit der Datenbank:", exc_info=e)
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS cwl (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) NOT NULL,
                        townhall INTEGER NOT NULL
                    )
                ''')
                conn.commit()
                logger.info("Datenbank initialisiert.")
        except Exception as e:
            logger.error("Fehler beim Initialisieren der Datenbank:", exc_info=e)
        finally:
            conn.close()

def add_entry(username, townhall):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO cwl (username, townhall) VALUES (%s, %s)', (username, townhall))
                conn.commit()
                logger.info(f'Eintrag hinzugefügt: {username} (Rathaus: {townhall})')
        except Exception as e:
            logger.error("Fehler beim Hinzufügen eines Eintrags:", exc_info=e)
        finally:
            conn.close()

def remove_entry(username):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM cwl WHERE LOWER(username) = LOWER(%s)', (username,))
                conn.commit()
                if cur.rowcount > 0:
                    logger.info(f'Eintrag entfernt: {username}')
                else:
                    logger.warning(f'Kein Eintrag gefunden zum Entfernen: {username}')
        except Exception as e:
            logger.error("Fehler beim Entfernen eines Eintrags:", exc_info=e)
        finally:
            conn.close()

def get_all_entries():
    conn = get_db_connection()
    entries = []
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT username, townhall FROM cwl ORDER BY id ASC')
                entries = cur.fetchall()
        except Exception as e:
            logger.error("Fehler beim Abrufen der Einträge:", exc_info=e)
        finally:
            conn.close()
    return entries


async def get_cwl_list_from_db():
    query = "SELECT username, townhall FROM cwl;"
    try:
        conn = await get_db_connection()
        records = await conn.fetch(query)
        await conn.close()
        return records
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der CWL-Liste: {e}")
        return []
    

def test_entry_exists(username) -> bool:
    query = "SELECT username FROM cwl WHERE username = %s"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (username, ))
        records = cursor.fetchall()
        logger.info(f"Records gefunden: {records}")
        cursor.close()
        conn.close()
        return bool(records)
    except Exception as e:
        logger.error(f"Fehler beim Abrufen aus der CWL-Liste: {e}")
        return False

