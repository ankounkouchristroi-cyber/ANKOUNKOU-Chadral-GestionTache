from mysql.connector import  Error 
import mysql.connector

CONFIG ={
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "gestionTache",
    "charset": "utf8mb4"
}
def obtenir_connexion():
    try:
        conn = mysql.connector.connect(**CONFIG)
        return conn
    except Error as e:
        print(f"Erreur base de donnees :{e}")
        return None
    
def fermer_connexion(conn):
    if conn is not None:
        conn.close()

def test_connexion():
    conn=obtenir_connexion()
    if conn:
        print("connexion reussie")
        fermer_connexion(conn)
    else:
        print("connexion échouée")

if __name__ == "__main__":
    test_connexion()
