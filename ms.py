import pyodbc

import requests
import json


def gestion_randonnee():
    print_bold("\n\n\t\t\t****************************      ")
    print_bold("\n\t\t\tRANDONNEE AVEC 'Ny dia-tsika'\n ")
    print_bold("\t\t\t****************************    ")
    print("\t\tVeuillez choisir parmi les 4 propositions:")
    print(" \t\t\t1- Lister les réservations  \n \t\t\t2- Reserver \n \t\t\t3- Modifier votre réservation\n \t\t\t4- Supprimer votre réservation'\n \t\t\t5- Très prochain réservations \n \t\t\t6- Recherche entre deux date  \n")

    
     

    server = 'DESKTOP-TFQNRQ4\SQLEXPRESS'
    database = 'Mabase'
    trusted_connection = 'yes'
    choix_utilisateur = input("\t\tVeuillez entrer votre choix (1 à 5) : ")
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=' + trusted_connection
        ) 
        
        if choix_utilisateur == "2":
             choix1(conn)
             retour()
        if choix_utilisateur == "1":
             choix2(conn)
             retour()
             
        if choix_utilisateur == "3":
             choix3(conn)
             retour()
        if choix_utilisateur == "4":
             choix4(conn)
             retour()
             
        if choix_utilisateur == "5":
             choix5(conn)
             retour()
             
                          
        if choix_utilisateur == "6":
             choix6(conn)
             retour()
    except pyodbc.Error as e:
       print("Erreur de connexion:", e)



def retour():
    
    retour=input_red("\t\tVoulez vous retourner à la racine ou quiter(Retour:1 / Quitter:0)")
    if retour =="1":
          gestion_randonnee() 
    else:
            print_red("\t\tVous avez quitté")
# Appel de la fonction

def choix2(conn):
            print("\n\t\tVous avez choisi de LISTER :\n")
            cursor = conn.cursor()
            cursor.execute("SELECT idReservation, villeReservation,dateReservation,nomReservateur FROM Reservation")
            results = cursor.fetchall()
            isa=0
            for row in results:
                nomReservateur=row.nomReservateur
                idReservation = row.idReservation
                villeReservation = row.villeReservation
                dateReservation= row.dateReservation
                print("\t\t\t id:",idReservation,"Randonneur:",nomReservateur, "\t\tDate:", dateReservation,"\tVille:", villeReservation)
                isa +=1
            cursor.close()      
            print('\n\t\t\tNombre total des enregistrements :',isa,'  résevation(s)')
            print("\t\t\t ______FIN DU LISTAGE______\n") 
                        



def choix1(conn): 
        print("\n\t\tVous avez choisi de RESERVER :")
        print("\t\tchoix 1: Antananarivo ")
        print("\t\tchoix 2: Mahajanga ")
        print("\t\tchoix 3: Isalo ")
        print("\t\tchoix 4: Morondava ")
        print("\t\tchoix 5: Antsirabe  ")
        print("\t\tchoix 6: Andasibe  ")
        print("\t\tchoix 7: Itasy\n  ") 
        
        villeReservation = input("\t\tEntrez la ville que vous préferiez (1 à 7): ")
        if villeReservation=="1":
            ville='Antananarivo'
        if villeReservation=="2":
            ville='Mahajanga'
        if villeReservation=="3":
            ville='Isalo'
        if villeReservation=="4":
            ville='Morondava'  
        if villeReservation=="5":
                ville='Antsirabe'
        if villeReservation=="6":
                ville='Andasibe'
        if villeReservation=="7":
                ville='Itasy'         
        
        print("\t")
        print("Vous avez entré: ",ville)
        print("\n\t")   
        date_valide = False

        while not date_valide:
            date_saisie = input("\t\tVeuillez entrer la date  (ex:2024-06-15) : ")
            
            try:
                # Vérifier si la date saisie est au format AAAA-MM-JJ
                annee, mois, jour = map(str, date_saisie.split('-'))
                date_valide = True
            except ValueError:
                print("Format de date invalide. Veuillez réessayer.\t")

         
        dateReservation= annee+"-"+mois+"-"+jour
        nom = input("\n\t\tEntrez le nom du randonneur(se):") 
        
        
        
        
        
        
        
         
        print("\n\t\tVous allez résérver une randonnée à",ville,"le",dateReservation, "pour",nom)
        res=input("\t\tVous-en êtes sûr? (oui/non)")
        if res=="oui":
        
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Reservation ( villeReservation, dateReservation,nomReservateur) VALUES (?, ?,?)",
                        ville, dateReservation,nom)
            conn.commit()
            cursor.close()
            print("\n\t")
            print("Vous avez résérvé une randonnée à",ville,"le",dateReservation)
            print("\n\t")
            
        else:
           print("\n\t")    
           print_red("Enregistrement de la réservation annulée")
           
        

 


def choix5(conn): 
    print("\n\t\t\tVous avez choisi de LISTER les très prochains réservations :\n")
    print("\n\n\t\t\t\t\t☁☁☀☀☔☔☔Ceci affiche en plus la météo☔☔☔☀☀☁☁\n")
    cursor = conn.cursor()
    cursor.execute("SELECT  idReservation , villeReservation, dateReservation FROM Reservation WHERE dateReservation BETWEEN GETDATE() AND DATEADD(DAY, 4, GETDATE())")
    results = cursor.fetchall()
    isa = 0
    print("\t\t\tid\tVille\t\tDate\t\tT(°K)\t\tT(°C)\t\tDescription")
    print("\t\t",("-" * 90))  # Ligne de séparation
    for row in results:
        
        idReservation = row.idReservation
        villeReservation = row.villeReservation
        dateReservation = row.dateReservation       
        
        api_key = 'API_KEY' 

        url = f"http://api.openweathermap.org/data/2.5/forecast?q={villeReservation}&appid={api_key}"
        response = requests.get(url)
        data = json.loads(response.text)

        # Recherche des données météorologiques pour la date spécifiée
       

        for forecast in data['list']:
            if forecast['dt_txt'].split()[0] == dateReservation:
                temperature = forecast['main']['temp']
                description = forecast['weather'][0]['description']
                precipitation = forecast['rain'] if 'rain' in forecast else 0  # Vérifie si la clé 'rain' existe dans les données
                temp= temperature - 273
                temp= round(temp)
                print("\t\t\t{:<5}\t{:<10}\t{:<10}\t{:<10}\t{:<10} \t{:<20}".format(idReservation, villeReservation, dateReservation, temperature,temp,  description))
                break
    
        
        
        

        isa = isa + 1
         
    cursor.close()
    print("\n\t\tNombre total des prochains réservation:", isa)
    print("\t\t\t-----Fin du listage-----\n")









def choix3(conn): 
            print("\n\t\t\t\tMODIFIER RESERVATION ")
            mod=input("\n\t\tVeuillez entrer le id du réservation à modifier: ")
            cursor = conn.cursor()
            cursor.execute("SELECT idReservation, villeReservation,dateReservation,nomReservateur FROM Reservation where idReservation=?",mod)
            results = cursor.fetchall()
            isa=0
            for row in results:
                nom=row.nomReservateur
                id = row.idReservation
                ville = row.villeReservation
                date= row.dateReservation
                print("\n\t\t id:",id,"\t(a) Randonneur(se):",nom, "\t(b) Date:", date,"\t(c) Ville:", ville,"\n")
                isa +=1
            
            colonne=input("\n\t\tVeuillez entrer la colonne à modifier  (a ou b ou c): ")
            if colonne=="a": 
                Ncoll= 'nomReservateur'
                coll=nom 
                
            elif colonne=="b": 
                Ncoll= 'dateReservation'
                coll=date 
                
            elif colonne=="c": 
                Ncoll='villeReservation'
                coll=ville 
                 
            else :
                 updt(colonne,nom ,date ,ville )
            
            
            
            nouveau = input("\t\tVeuillez entrer sa nouvelle valeur: ")
            print("\n\t\tVous allez modifier ",coll , " par ",nouveau)
            res=input_red("\t\tVous-en êtes sûr? (oui/non)")
            if res=="oui":
                req = "UPDATE Reservation SET {} = '{}' WHERE idReservation = {}".format(Ncoll , nouveau, mod)
 
 
                print("\n\t")
                cursor.execute(req )
                conn.commit()
                cursor.close() 
                print("\t\tModification du",Ncoll , "par",nouveau ,"réussie")
                print("\n\t")
            
            else:
                print("\n\t")    
                print("Modification annulée")              
            
                
  



def updt(colonne,nom ,date ,ville ):
                colonne=input("\t\t Veuillez entrer a ou b ou c): ") 
                if colonne=="a": 
                    Ncoll='nomReservateur'
                    coll=nom  
                    
                elif colonne=="b": 
                    Ncoll='dateReservation'
                    coll=date 
                    
                elif colonne=="c": 
                    Ncoll='villeReservation'
                    coll=ville 
                else:
                    updt(colonne,nom ,date ,ville )



 


def choix4(conn): 
            print("\n\t\t\t\tSUPRIMER RESERVATION ")
            mod=input("\n\t\tVeuillez entrer le id du réservation à suprimer: ")
            cursor = conn.cursor()
            cursor.execute("SELECT idReservation, villeReservation,dateReservation,nomReservateur FROM Reservation where idReservation=?",mod)
            results = cursor.fetchall()
            isa=0
            for row in results:
                nom=row.nomReservateur
                id = row.idReservation
                ville = row.villeReservation
                date= row.dateReservation
                print("\n\t\t id:",id,"\t(a) Randonneur(se):",nom, "\t(b) Date:", date,"\t(c) Ville:", ville,"\n")
                isa +=1
            
             
            
            
            
             
            print("\n\t\tVous allez suprimer la réservation ci-dessous ")
            res=input_red("\t\tVous-en êtes sûr? (oui/non)")
            if res=="oui":
                req = "DELETE from Reservation WHERE idReservation = {}".format(id)
 
 
                print("\n\t")
                cursor.execute(req )
                conn.commit()
                cursor.close() 
                print("\t\tSupression du  du réservation réussie")
                print("\n\t")
            
            else:
                print("\n\t")    
                print("Supression annulée")              
            
                
   

def print_bold(text):
    print("\033[5m" + text + "\033[0m")

def print_red(text):
    print("\033[91m" + text + "\033[0m") 
 
 
     
def input_red(prompt):
    print("\033[92m", end="")
    user_input = input(prompt)
    print("\033[0m", end="")
    return user_input   
     
     
     


def choix6(conn):
            print("\n\t\tVous avez choisi la recherche entre 2 dates :\n")
            date1=input("\t\t\tEntrez la date 1: ")
            date2=input("\t\t\tEntrez la date 2: ")
            cursor = conn.cursor()
            cursor.execute("SELECT idReservation, villeReservation,dateReservation,nomReservateur FROM Reservation where dateReservation between ?  and ?",date1,date2)
            results = cursor.fetchall()
            isa=0
            for row in results:
                nomReservateur=row.nomReservateur
                idReservation = row.idReservation
                villeReservation = row.villeReservation
                dateReservation= row.dateReservation
                print("\t\t\t id:",idReservation,"Randonneur:",nomReservateur, "\t\tDate:", dateReservation,"\tVille:", villeReservation)
                isa +=1
            cursor.close()      
            print('\n\t\t\tNombre total des enregistrements :',isa,'  résevation(s)')
            print("\t\t\t ______FIN DU LISTAGE______\n") 
                        
     
              
gestion_randonnee()

 


 
