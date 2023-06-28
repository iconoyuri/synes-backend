from mail.account_activation_handler import AccountActivationHandler
from functions import graph_driver, encode_password
from globals import DATABASE_DEFAULT_USERNAME,DATABASE_DEFAULT_PASSWORD
from datetime import datetime

def database_setup():
    from schemas import UserData

    driver = graph_driver({'email':DATABASE_DEFAULT_USERNAME,'password':DATABASE_DEFAULT_PASSWORD})

    time = datetime.now()
    time_str = str(time)
    timestamp = str(time.timestamp()).replace('.','')
    password = encode_password(timestamp)
    
    link=""
    profile = UserData(
        matricule='19M2222',
        nom='MELIE URIEL',
        age=12,
        sexe='Masculin',
        specialite='Informatique',
        nationalite='cmr',
        phone_number='4894156',
        etablissement='ngoakele',
        adresse_mail='uriel.melie@facsciences-uy1.cm' 
    )
    query = """
        MERGE (user:User{adresse_mail:$adresse_mail})
            ON CREATE
                SET
                    user.matricule = $matricule,
                    user.nom = $nom,
                    user.age = $age,
                    user.sexe = $sexe,
                    user.specialite = $specialite,
                    user.nationalite = $nationalite,
                    user.phone_number = $phone_number,
                    user.mot_de_passe = $mot_de_passe,
                    user.date_creation = $now

        MERGE (etablissement:Etablissement{nom:$nom_etablissement})
            ON CREATE 
                SET etablissement.date_creation = $now

        MERGE (section:Section{nom:$nom_etablissement})
            ON CREATE 
                SET section.date_creation = $now

        MERGE (user)-[:belong_to_school]->(etablissement)
        MERGE (etablissement)-[:related_school]->(section)
        MERGE (user)-[:attached_to]->(section)

        MERGE (user)<-[:is_profile_photo]-(photo:Photo)
            ON CREATE 
                SET photo.date_creation = $now, photo.link = $link
    """
    params = {
        'adresse_mail':profile.adresse_mail,
        'matricule':profile.matricule,
        'nom':profile.nom,
        'age':profile.age,
        'sexe':profile.sexe,
        'specialite':profile.specialite,
        'nationalite':profile.nationalite,
        'phone_number':profile.phone_number,
        'mot_de_passe':password,
        'nom_etablissement':profile.etablissement,
        'now':time_str,
        'link':link
    }

    AccountActivationHandler.send_credentials_mail(profile.nom, profile.adresse_mail, timestamp)

    driver.run(query, params)
    import py2neo
    try:
        driver.run("CREATE CONSTRAINT FOR (n:User) REQUIRE n.adresse_mail IS UNIQUE")
        driver.run("CREATE CONSTRAINT FOR (n:Etablissement) REQUIRE n.nom IS UNIQUE")
        driver.run("CREATE CONSTRAINT FOR (n:Section) REQUIRE n.nom IS UNIQUE")
    except py2neo.errors.ClientError:
        ...
    # driver.run()
