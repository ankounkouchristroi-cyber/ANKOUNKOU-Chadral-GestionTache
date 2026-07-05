from connexion import *
import hashlib
utilisateur=None
def hasher_mp(mot_de_passe):
    return hashlib.sha256(mot_de_passe.encode()).hexdigest()

def verification_mdp(mdpsaisie,mdp):
    return hasher_mp(mdpsaisie)==mdp

def inscription():
    if utilisateur is not None:
        print("vous vous etes deja inscrit")
        return
    conn= None
    cursor=None
    print("="*20)
    print("Inscription")
    print("="*20)
    try:
        nom_utilisateur = input("Nom d'utilisateur : ")
        email = input("Email : ").lower()
        while '@' not in email or not email.endswith(".com") or  len(email)<14:
            print("email doit contenir un '@' et un domaine (.com) et contenir plus de 14 Caracteres!!!!" )
            email = input("Email : ").lower()
        
        mot_de_passe = input("Mot de passe : ")
        while len(mot_de_passe)<10:
            print("le mot de passe doit contenir plus de 10 Caracteres" )
            mot_de_passe = input("Mot de passe : ")

        mot_de_passe1=""
        attempts=0
        while mot_de_passe1 != mot_de_passe and attempts<3  :
            mot_de_passe1= input("retape le mot de passe : ")
            if mot_de_passe1!=mot_de_passe:
                attempts+=1
                print(f"mot de passe invalide, il vous reste {attempts}/3")
        if mot_de_passe!=mot_de_passe1:
                print("nombre de tentative atteint")
                return
        
        conn=obtenir_connexion()
        cursor=conn.cursor(dictionary=True)
        sql="""
        select id_user
        from utilisateur 
        where nom_utilisateur =%s
        """
        cursor.execute(sql,(nom_utilisateur,))
        resultat=cursor.fetchone()
        if resultat:
            print("cette utilisateur existe deja")
            return
        mdp_hash=hasher_mp(mot_de_passe)
        sql="""
        insert into utilisateur(nom_utilisateur,mot_de_passe,email)
        values(%s,%s,%s)
        """
        cursor.execute(sql,(nom_utilisateur,mdp_hash,email))
        conn.commit() 
        print(f"Vous vous etes incrit avec succes {nom_utilisateur}")
    except Error as e:
        conn.rollback()
        print(f"Erreur dans la base de donnee {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def connexion():
    global utilisateur
    if utilisateur is not None:
        print("vous etes deja connecte. Voulez-vous vous connectez")
        choix=0
        attempts=0
        while True:
            choix=input("vous choisissez quoi (y/n)?").lower()
            attempts+=1
            if attempts==4:
                print("Veuillez reessayer Plus tard!")
                return
            if choix=='y':
                deconnexion()
                connexion()
                return
            if choix=='n':
                return
    conn=None
    cursor=None
    print("="*30)
    print("Connexion au compte")
    print("="*30)
    try:
        tentative=0
        while tentative<5:
            nom_utilisateur=input("Entrez le nom d'utilisateur : ")
            mot_de_passe=input("Entrez le mot de passe : ")
            mdp=hasher_mp(mot_de_passe)
            conn=obtenir_connexion()
            cursor=conn.cursor(dictionary=True)
            sql="""
            select id_user
            from utilisateur
            where nom_utilisateur =%s and mot_de_passe=%s

            """
            cursor.execute(sql,(nom_utilisateur,mdp))
            resultat=cursor.fetchone()
            if resultat:
                utilisateur={
                    'id': resultat['id_user'],
                    'nom':nom_utilisateur,
                }
                print(f"Connecte sous le nom de {utilisateur['nom']}")
                return True
            else:
                tentative+=1
                print(f"Identification impossible, il vous reste {tentative}/4")
    except Error as e:
        print(f"Erreur de la base de donnee : {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def deconnexion():
    global utilisateur
    if utilisateur is not None:
        utilisateur=None
        print("Seen you soon!")
        return 
    else:
        print("Vous etes pas connecte pour que vous puissiez vous deconnecte")      
            
def test_utilisateur():
    choix=0
    while choix!=4:
        print("1.Inscription")
        print("2.Connexion")
        print("3.deconnexion")
        choix=int(input("entrez votre choix"))
        match choix:
            case 1:
                inscription()
            case 2:
                connexion()
            case 3:
                deconnexion()
            case 4:
                print("Seen you soon!!!!")
            case _:
                print("entrez une valeur entre (1-4)")


if __name__=="__main__":
    test_utilisateur()

