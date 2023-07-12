from py2neo.ogm import Property,RelatedFrom,RelatedTo, GraphObject, Property

class CreatedEntity(GraphObject):
    date_creation = Property()


class User(CreatedEntity):

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

    etablissement = RelatedTo("Etablissement",'belong_to_school')
    section = RelatedTo("Section",'attached_to')
    biens_crees = RelatedTo("Bien",'create_good')
    depenses_creees = RelatedTo("Depense", 'create_expense')
    caisses_creees = RelatedTo('Caisse', 'create_bank')
    fonds_creees = RelatedTo("Fond", 'create_fund')
    fonds_contribues = RelatedTo("Fond", 'contribute')
    activites_modereees = RelatedTo("Activite",'moderate')


    photo = RelatedFrom("Photo",'is_profile_photo')
    activites_creees = RelatedTo("Activite",'create_activity')
    activites_invite = RelatedFrom("Activite",'invited')
    notifications = RelatedFrom('Notification','notify')
    

class Etablissement(CreatedEntity):

    # __primarykey__ = "nom"

    nom = Property()

    enseignants = RelatedFrom('User', 'belong_to_school')
    sections = RelatedTo('Section', 'related_school')

class Section(CreatedEntity):

    # __primarykey__ = "nom"

    nom = Property()

    enseignants = RelatedFrom('User', 'attached_to')
    etablissement = RelatedFrom('Etablissement', 'related_school')
    
    biens = RelatedFrom('Bien', 'belong_section')

class Bien(CreatedEntity):

    nom = Property()
    description = Property()
    valeur = Property()

    createur = RelatedFrom('User','create_good')
    photos = RelatedFrom('Photo','illustrate')

    section = RelatedTo('Section', 'belong_section')
    syndicat = RelatedTo('Syndicat', 'belong_syndicate')

class Syndicat(CreatedEntity):

    nom = Property(default="SYNES")

    biens = RelatedFrom('Bien', 'belong_syndicate')

class Photo(CreatedEntity):

    link = Property()

    bien = RelatedTo('Bien', 'illustrate')
    user = RelatedTo('User', 'is_profile_photo')
    activite = RelatedTo('Activite', 'is_snapshot')

class Notification(CreatedEntity):

    sujet = Property()
    contenu = Property()
    type = Property(default="Simple")
    lien_associe = Property(default="")

    utilisateurs_notifies = RelatedTo('User', 'notify')

class Activite(CreatedEntity):
    
    titre = Property()
    lieu = Property()
    date_debut = Property()
    date_fin = Property()

    photos = RelatedFrom('Photo', 'is_snapshot')
    createur = RelatedFrom('User', 'create_activity')
    moderateurs = RelatedFrom('User','moderate')
    invites = RelatedTo('User','invited')


class Depense(CreatedEntity):

    titre = Property()
    description = Property()
    montant = Property()

    createur = RelatedFrom('User','create_expense')
    caisse = RelatedFrom('Caisse', 'expense_related_bank')

class Caisse(CreatedEntity):

    nom = Property()
    description = Property()
    montant_courant = Property()

    createur = RelatedFrom('User','create_bank')
    fonds = RelatedFrom('Fond', 'fund_related_bank')
    depenses = RelatedFrom('Depense', 'expense_related_bank')

class Fond(CreatedEntity):

    titre = Property()
    description = Property()
    montant = Property()

    createur = RelatedFrom('User','create_fund')
    contributeurs = RelatedFrom('User','contribute')

    caisse = RelatedTo('Caisse', 'fund_related_bank')

