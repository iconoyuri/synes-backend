from py2neo.ogm import Property,RelatedFrom,RelatedTo, GraphObject, Property

class User(GraphObject):

    __primarykey__ = 'adresse_mail'

    matricule = Property()
    nom = Property()
    age = Property()
    sexe = Property()
    specialite = Property()
    nationalite = Property()
    adresse_mail = Property()
    phone_number = Property()
    mot_de_passe = Property()

    etablissement = RelatedTo("Etablissement",'belong')
    section = RelatedTo("Section",'belong')
    biens_crees = RelatedTo("Bien",'create')
    depenses_creees = RelatedTo("Depense", 'create')
    caisses_creees = RelatedTo('Caisse', 'create')
    fonds_creees = RelatedTo("Fond", 'create')
    fonds_contribues = RelatedTo("Fond", 'contribute')
    activites_modereees = RelatedTo("Activite",'moderate')


    photo = RelatedFrom("Photo",'illustrate')
    activites_creees = RelatedTo("Activite",'create')
    activites_invite = RelatedFrom("Activite",'invite')
    notifications = RelatedFrom('Notification','notify')
    

class Etablissement(GraphObject):

    __primarykey__ = "nom"

    nom = Property()

    enseignants = RelatedFrom('User', 'belong')
    sections = RelatedFrom('Section', 'belong')

class Section(GraphObject):

    __primarykey__ = "nom"

    nom = Property()

    etablissement = RelatedTo('Etablissement', 'belong')

    enseignants = RelatedFrom('User', 'belong')
    biens = RelatedFrom('Bien', 'belong')

class Bien(GraphObject):

    nom = Property()
    description = Property()
    valeur = Property()

    createur = RelatedFrom('User','create')
    photos = RelatedFrom('Photo','illustrate')

    section = RelatedTo('Section', 'belong')
    syndicat = RelatedTo('Syndicat', 'belong')

class Syndicat(GraphObject):

    nom = Property(default="SYNES")

    biens = RelatedFrom('Bien', 'belong')

class Photo(GraphObject):

    link = Property()

    bien = RelatedTo('Bien', 'illustrate')
    user = RelatedTo('User', 'illustrate')
    activite = RelatedTo('Activite', 'illustrate')

class Notification(GraphObject):

    sujet = Property()
    contenu = Property()
    type = Property(default="Simple")
    lien_associe = Property()
    date = Property()

    utilisateurs_notifies = RelatedTo('User', 'notify')

class Activite(GraphObject):
    
    titre = Property()
    lieu = Property()
    date_debut = Property()
    date_fin = Property()

    photos = RelatedFrom('Photo', 'illustrate')
    createur = RelatedFrom('User', 'create')
    moderateurs = RelatedFrom('User','moderate')
    invites = RelatedTo('User','invite')


class Depense(GraphObject):

    titre = Property()
    description = Property()
    montant = Property()

    createur = RelatedFrom('User','create')
    caisse = RelatedFrom('Caisse', 'affect')

class Caisse(GraphObject):

    nom = Property()
    description = Property()
    montant_courant = Property()

    createur = RelatedFrom('User','create')
    fonds = RelatedFrom('Fond', 'affect')
    depenses = RelatedFrom('Depense', 'affect')

class Fond(GraphObject):

    titre = Property()
    description = Property()
    montant = Property()

    createur = RelatedFrom('User','create')
    contributeurs = RelatedFrom('User','contribute')

    caisse = RelatedTo('Caisse', 'affect')

