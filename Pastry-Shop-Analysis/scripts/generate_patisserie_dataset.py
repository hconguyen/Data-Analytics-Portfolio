# ------------------------------------------------------------
# Auteur : Huy-Co Nguyen
# Date : 2026-02-07
# Projet : Génération de données simulées – Pâtisserie CT
#
# Description :
#   Script Python générant des données synthétiques pour le menu,
#   les ingrédients, les recettes, les employés, les absences,
#   les dépenses fixes et les ventes, exportées en CSV pour Power BI.
# ------------------------------------------------------------


import csv
from tracemalloc import start
from numpy import average
import pandas as pd
from tkinter import FIRST
from faker import Faker
import random
from datetime import date, timedelta
import unicodedata

#######################################################################################################################
#
# Données Ventes  
#
#######################################################################################################################


# On configure Faker pour utiliser le français du Canada (pour les noms/adresses)
fake = Faker('fr_CA')

# Configuration du projet
NB_PRODUCTS = 6     # Nombre de lignes de produits à générer
NB_INGREDIENTS = 20 # Nombre de lignes d'ingrédients à générer
NB_RECIPES = 25     # Nombre de lignes de recettes à générer
NB_SALES = 1000     # Nombre de lignes de ventes à générer
# NB_STAFF = 5        # Nombre de lignes d'employés à générer
NB_EXPENSES = 7     # Nombre de lignes de dépenses à générer
NB_EMPLOYEES = 40   # Nombre de lignes d'employés à générer
# NB_TRANSACTIONS = 1000 # Nombre de lignes de transactions à générer

# On définit : "Nom": [Categorie, Style, Size, CostPerProduct, PricePerProduct, PrepTimeMinutes] - MENU
PRODUCTS = {
    "Croissant": ["Viennoiserie", "Classique", "Individuel" , 0.80, 2.50, 12],
    "Éclair chocolat": ["Pâtisserie", "Classique", "Individuel", 1.20, 4.50, 8],
    "Gâteau au pandan et durian": ["Pâtisserie", "Signature", "5-6 pers", 15.00, 45.00, 25],
    "Latté à la citrouille": ["Boisson", "Édition limitée", "12 oz", 0.50, 4.25, 3],
    "Muffin aux bleuets": ["Viennoiserie", "Saisonnier", "Individuel", 0.90, 2.75, 4],
    "Pain au levain": ["Boulangerie", "Artisanal", "500g", 1.15, 5.75, 15]
}

# On définit : "Nom": [Category, UnitOfMeasure, UnitCost] - INGREDIENTS
INGREDIENTS = {
    "Farine tout-usage": ["Base", "kg", 1.20],
    "Farine de force": ["Base", "kg", 1.45],
    "Beurre de baratte": ["Laitier", "kg", 14.50],
    "Oeufs de calibre gros": ["Laitier", "Unité (12)", 4.25],
    "Sucre blanc granulé": ["Base", "kg", 1.80],
    "Sel de mer": ["Base", "kg", 0.95],
    "Levure boulangère": ["Base", "kg", 12.00],
    "Chocolat noir 70 %": ["Spécialité", "kg", 22.00],
    "Pâte de Pandan": ["Spécialité", "Unité (pot)", 8.50],
    "Chair de durian": ["Spécialité", "kg", 35.00],
    "Levure boulangère": ["Base", "kg", 12.00],
    "Lait 3,25 %": ["Laitier", "Litre", 2.10],
    "Crème 35 %": ["Laitier", "Litre", 5.50],
    "Fécule de maïs": ["Base", "kg", 3.25],
    "Bleuets frais": ["Fruits", "kg", 9.00],
    "Fécule de maïs": ["Base", "kg", 3.25],
    "Purée de citrouille": ["Fruits", "kg", 4.50],
    "Mélange d'épices": ["Spécialité", "kg", 18.00],
    "Grains de café Espresso": ["Boisson", "kg", 28.00],
    "Levain chef": ["Base", "kg", 0.50],
    "Extrait de vanille pur": ["Spécialité", "Litre", 85.00],
    "Boîte pâtissière": ["Emballage", "Unité", 1.15],
}

RECIPES = {
    # PRD-0001 : Croissant (Beurre, Farine force, Levure, Sel, Œufs)
    "PRD-0001": [("ING-0002", 0.110), ("ING-0003", 0.060), ("ING-0007", 0.005), ("ING-0006", 0.002), ("ING-0004", 0.010)],
    
    # PRD-0002 : Éclair (Farine TU, Lait, Beurre, Œufs, Chocolat, Crème)
    "PRD-0002": [("ING-0001", 0.050), ("ING-0011", 0.100), ("ING-0003", 0.040), ("ING-0004", 0.080), ("ING-0008", 0.030), ("ING-0012", 0.050)],
    
    # PRD-0003 : Gâteau Pandan/Durian (Farine TU, Pandan, Durian, Crème, Sucre, Boîte)
    "PRD-0003": [("ING-0001", 0.350), ("ING-0009", 0.015), ("ING-0010", 0.200), ("ING-0012", 0.400), ("ING-0005", 0.150), ("ING-0020", 1.0)],
    
    # PRD-0004 : Latté Citrouille (Café, Lait, Purée Citrouille, Épices)
    "PRD-0004": [("ING-0017", 0.020), ("ING-0011", 0.250), ("ING-0015", 0.045), ("ING-0016", 0.005)],
    
    # PRD-0005 : Muffin Bleuets (Farine TU, Bleuets, Sucre, Œufs, Lait)
    "PRD-0005": [("ING-0001", 0.150), ("ING-0014", 0.080), ("ING-0005", 0.050), ("ING-0004", 0.040), ("ING-0011", 0.050)],
    
    # PRD-0006 : Pain au Levain (Farine force, Levain, Sel, Eau)
    "PRD-0006": [("ING-0002", 0.500), ("ING-0018", 0.150), ("ING-0006", 0.010)]
}

# Données de l'équipe [First Name, Last Name, Role, HourlyRate]
STAFF = [
    ("Julie", "Martin", "Chef Pâtissière", 28.00),
    ("Marc", "Tremblay", "Boulanger", 24.50),
    ("Sophie", "Labelle", "Pâtissière Junior", 18.50),
    ("Antoine", "Roy", "Serveur/Barista", 16.50),
    ("Lucie", "Bouchard", "Serveuse/Barista", 16.75)
]

# Configuration : (Catégorie, Nom, Montant de base)
FIXED_EXPENSES = [
    ("Occupation", "Loyer Local Brossard", 2500.00),
    ("Occupation", "Taxes Municipales", 300.00),
    ("Énergie", "Hydro-Québec", 450.00),
    ("Énergie", "Gaz Métro", 180.00),
    ("Marketing", "Publicité Facebook/IG", 250.00),
    ("RH", "Assurances Collectives", 150.00),
    ("Technologie", "Abonnement POS & Internet", 130.00)
]

# Définition des canaux avec des probabilités différentes
# On simule : 50% sur place, 30% à emporter, 20% livraison
SALES_CHANNELS = ["Sur place", "À emporter", "Livraison"]
SALES_CHANNEL_WEIGHTS = [0.5, 0.3, 0.2]

# Définition des canaux avec des probabilités différentes
# On simule : 70% quotidien, 15% corporate, 2% mariage, 8% anniversaire, 5% atelier
EVENT_CHANNELS = ["Quotidien", "Corporate", "Mariage", "Anniversaire", "Atelier"]
EVENT_CHANNEL_WEIGHTS = [0.70, 0.15, 0.02, 0.08, 0.05]

SUPPLIER = ["Costco", "Mayrand Alimentation", "Distribution Alimentaire Aubut Inc"]

# Création du fichier CSV - Menu
with open('Menu.csv', mode='w', newline='', encoding='utf-8') as fichier:
    writer = csv.writer(fichier)
    
    # En-têtes des colonnes
    writer.writerow(['ProductID', 'ProductName', 'ProductCategory', 'ProductStyle', 'ProductSize', 'CostPerProduct', 'PricePerProduct', 'PrepTimeMinutes'])


    for i, (name, info) in enumerate(PRODUCTS.items(), start=1):
        # Création de mes IDs
        id_trans = f"PRD-{i:04d}" # Génère PRD-0001, PRD-0002...

        writer.writerow([
            id_trans,
            name,        # Le nom est la clé du dictionnaire
            info[0],     # Catégorie (1er élément de la liste)
            info[1],     # Style (2e élément)
            info[2],     # Taille (3e élément)
            str(info[3]).replace('.', ','), # Coût
            str(info[4]).replace('.', ','),  # Prix
            str(info[5]).replace('.', ',')  # Temps de préparation en minutes
        ])

print(f"Succès ! Le fichier 'Menu.csv' avec {NB_PRODUCTS} PRODUCTS a été créé.")


# Création du fichier CSV - Ingredients
with open('Ingredients.csv', mode='w', newline='', encoding='utf-8') as fichier:
    writer = csv.writer(fichier)

    # En-têtes des colonnes
    writer.writerow(['IngredientID', 'IngredientName', 'IngredientCategory', 'IngredientUnitOfMeasure', 'IngredientUnitCost', 'IngredientPurchasedDate', 'IngredientSupplier'])

    for i, (name, info) in enumerate(INGREDIENTS.items(), start=1):
        # Création de mes IDs
        id_trans = f"ING-{i:04d}" # Génère ING-0001, ING-0002...

        writer.writerow([
            id_trans,
            name,                                                                                 # Le nom est la clé du dictionnaire
            info[0],                                                                              # Catégorie (1er élément de la liste)
            info[1],                                                                              # Unité de mesure (2e élément)
            str(info[2]).replace('.', ','),                                                       # Coût à l'unité
            fake.date_between(start_date=date(2024, 10, 1), end_date=date(2024, 12, 31)),         # Ingrédients achetés au dernier trimestre 2024
            random.choice(SUPPLIER)                                                               # Fournisseur de l'ingrédient
        ])

print(f"Succès ! Le fichier 'Ingredients.csv' avec {NB_INGREDIENTS} INGREDIENTS a été créé.")


# Création du fichier CSV - Recipe
with open('Recipes.csv', mode='w', newline='', encoding='utf-8') as fichier:
    writer = csv.writer(fichier)

    # En-têtes des colonnes
    writer.writerow(['ProductID', 'IngredientID', 'QuantityNeeded'])

    for prd_id, ingredients in RECIPES.items():
        for ing_id, qty in ingredients:
            writer.writerow([
                prd_id, 
                ing_id, 
                str(qty).replace('.', ',')
            ])

print(f"Succès ! Le fichier 'Recipes.csv' avec {NB_RECIPES} RECIPES a été créé.")


# Création du fichier CSV - Staff
# with open('Staff.csv', mode='w', newline='', encoding='utf-8') as fichier:
#     writer = csv.writer(fichier)

#     # En-têtes des colonnes
#     writer.writerow(['StaffID', 'StaffFirstName', 'StaffLastName', 'Role', 'HourlyRate', 'HireDate', 'Email'])

#     for i, (employee_fname, employee_lname, employee_role, employee_rate) in enumerate(STAFF, start=1):
#         id_trans = f"STF-{i:04d}"
#         # On génère un email professionnel automatiquement
#         employee_email = f"{employee_fname.lower()}.{employee_lname.lower()}@patisseriect.ca"
        
#         writer.writerow([
#             id_trans, 
#             employee_fname, 
#             employee_lname, 
#             employee_role, 
#             str(employee_rate).replace('.', ','),
#             fake.date_between(start_date=date(2022, 1, 1), end_date=date(2024, 12, 31)),
#             employee_email
#         ])

# print(f"Succès ! Le fichier 'Staff.csv' avec {NB_STAFF} STAFF a été créé.")


# Création du fichier CSV - Fixed Expenses
with open('Fixed_Expenses.csv', mode='w', newline='', encoding='utf-8') as fichier:
    writer = csv.writer(fichier)

    # En-têtes des colonnes
    writer.writerow(['ExpenseID', 'ExpenseCategory', 'ExpenseName', 'MonthlyCost', 'PaymentDate'])

    for i, (fe_category, fe_name, fe_monthlycost) in enumerate(FIXED_EXPENSES, start=1):
        # Assigner une date logique selon la catégorie
        if fe_category == "Occupation":
            day = 1  # Loyer toujours le 1er
        elif fe_category == "Énergie":
            day = 15 # Factures de milieu de mois
        else:
            day = random.randint(18, 28) # Autres frais en fin de mois
            
        month = random.randint(1, 12)
        payment_date = f"{day:02d}/{month:02d}/2025"
        id_trans = f"EXP-{i:04d}"

        writer.writerow([
            id_trans, 
            fe_category, 
            fe_name, 
            str(fe_monthlycost).replace('.',','), 
            payment_date
        ])

print(f"Succès ! Le fichier 'Fixed_Expenses.csv' avec {NB_EXPENSES} FIXEDEXPENSES a été créé.")


#######################################################################################################################
#
# Données RH  
#
#######################################################################################################################

# On définit : "Nom": ['EmployeeID', 'EmployeeLastName', 'EmployeeFirstName', 'EmployeeGenre', 'EmployeeDateOfBirth', 'EmployeeHiringDate', 'EmployeeDepartment', 'EmployeeJobPosition', 'EmployeeContract', 'EmployeeAnnualSalary']] - EMPLOYEES
# Exemple de ce que Python génère en mémoire

# Vos règles métier
POSITION = {
    "Production": ["Chef Pâtissier", "Boulanger-Viennoisier", "Pâtissier", "Aide-Pâtissier", "Plongeur"],
    "Boutique": ["Gérant de boutique", "Commis aux ventes"],
    "Admin": ["Adjoint administratif", "Livreur"]
}

types_absence = ["Maladie", "Personnel", "Accident de travail", "Congé parental"]
poids_absence = [70, 20, 5, 5] # La maladie est la plus fréquente

def clean_email(text):
    # Étape 1 : Normalisation (sépare la lettre de l'accent)
    # Étape 2 : Encodage ASCII en ignorant ce qui ne passe pas (les accents)
    # Étape 3 : Décodage pour revenir en texte simple
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

# Création du fichier CSV - Employees
with open('Employees.csv', mode='w', newline='', encoding='utf-8') as fichier:
    writer = csv.writer(fichier)
    
    # En-têtes des colonnes
    writer.writerow(['EmployeeID', 'EmployeeLastName', 'EmployeeFirstName', 'EmployeeGenre', 'EmployeeDateOfBirth', 'EmployeeHiringDate', 'EmployeeDepartment', 'EmployeeJobPosition', 'EmployeeContract', 'EmployeeAnnualSalary', 'EmployeeHourlyRate', 'EmployeeEmail'])

    for i in range(1, 41):
        genre = random.choice(['H', 'F'])

        if genre == 'H':
            first_name = fake.first_name_male()
            last_name = fake.last_name()
        else:
            first_name = fake.first_name_female()
            last_name = fake.last_name()
            
        # On génère un email professionnel automatiquement
        employee_email = f"{first_name.lower()}.{last_name.lower()}@patisseriect.ca"

        dept = random.choice(list(POSITION.keys()))
        emp_position = random.choice(POSITION[dept])

        # On définit d'abord le type de contrat
        types_contrat = ["Permanent - Temps plein", "Permanent - Temps partiel", "Temporaire"]
        contrat = random.choices(types_contrat, weights=[70, 20, 10])[0]

        if "Chef" in emp_position:
            salaire = random.randint(65000, 85000)
        elif "Gérant" in emp_position or "Adjoint" in emp_position:
            salaire = random.randint(50000, 60000)
        elif "Pâtissier" == emp_position or "Viennoisier" in emp_position:
            salaire = random.randint(42000, 52000) # Environ 21$-25$/h
        else:
            # Aide-pâtissier, Commis, Livreur, Plongeur
            salaire = random.randint(34000, 38000) # Environ 17$-19$/h

        # On ajuste selon le type de contrat
        if "Temps partiel" in contrat:
            salaire_reel = int(salaire * 0.6) # On réduit le salaire annuel
        else:
            salaire_reel = salaire
        
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=65)
        minimum_hiringyear = date_of_birth.year + 18
        minimum_hiringdate = date(minimum_hiringyear, 1, 1)

        # Si la personne a 50 ans, on peut dire qu'elle a pu être embauchée 
        # n'importe quand entre ses 18 ans et aujourd'hui.
        # Pour une PME, on limite souvent à l'historique des 10 dernières années.
        start_point = max(minimum_hiringdate, date.today() - timedelta(days=365*10))

        hiring_date = fake.date_between(start_date=start_point, end_date='today')

        hourly_rate = round((salaire_reel / 2080), 2)

        # Création de mes IDs
        id_trans = f"EMP-{i:04d}" # Génère EMP-0001, EMP-0002...

        writer.writerow([
            id_trans,
            last_name,                          # Nom de famille
            first_name,                         # Prénom de famille
            genre,                              # Genre
            date_of_birth,                      # Date de naissance
            hiring_date,                        # Date d'embauche
            dept,                               # Département
            emp_position,                       # Poste
            contrat,                            # Type de contrat
            salaire_reel,                       # Salaire annuel
            str(hourly_rate).replace('.', ','), # Salaire de l'heure
            clean_email(employee_email)         # Adresse courriel
        ])

print(f"Succès ! Le fichier 'Employees.csv' avec {NB_EMPLOYEES} EMPLOYEES a été créé.")


# Création du fichier CSV - Absences
with open('Absences.csv', mode='w', newline='', encoding='utf-8') as fichier:
    writer = csv.writer(fichier)
    
    # En-têtes des colonnes
    writer.writerow(['AbsenceID', 'EmployeeID', 'AbsenceType', 'AbsenceStartDate', 'AbsenceEndDate', 'AbsenceNumDays'])

    # Charger les données générées précédemment
    df_employees = pd.read_csv("Employees.csv")

    abs_counter = 1

    for index, row in df_employees.iterrows():
        occupied_date = []
        
        # On décide si cet employé a eu des absences cette année (ex: 60% de chance)
        if random.random() < 0.60:

            # Création de mes IDs
            id_trans = f"ABS-{index:04d}" # Génère ABS-0001, ABS-0002...
            employees = df_employees['EmployeeID'].tolist()

            # La date de début doit être après sa date d'embauche !
            start_date_unclean = pd.to_datetime(row['EmployeeHiringDate'])
            start_date_clean = fake.date_between(start_date=start_date_unclean, end_date='today')

            # Durée aléatoire : souvent courte (1-3 jours), parfois longue (10 jours)
            duration = random.choices([1, 2, 3, 5, 10], weights=[40, 30, 15, 10, 5])[0]
            end_date = start_date_clean + timedelta(days=duration)

            # Vérification simple : est-ce que cette date a déjà été tirée ?
            if start_date_clean not in occupied_date:
                occupied_date.append(start_date_clean)

                writer.writerow([
                    id_trans,
                    random.choice(employees),
                    random.choices(types_absence, weights=poids_absence)[0],
                    start_date_clean,
                    end_date,
                    (end_date - start_date_clean).days + 1
                ])

                abs_counter += 1

print(f"Succès ! Le fichier 'Absences.csv' avec {abs_counter - 1} ABSENCES a été créé.")


# Création du fichier CSV - Sales
with open('Sales.csv', mode='w', newline='', encoding='utf-8') as fichier:
    writer = csv.writer(fichier)

    df_employees = pd.read_csv("Employees.csv")

    # En-têtes des colonnes
    writer.writerow(['OrderID', 'OrderDate', 'EmployeeID', 'ProductID', 'OrderQuantity', 'OrderType', 'ClientName', 'EventType'])

    for i in range(1, 1001):
        # Création de mes IDs
        id_trans = f"ORD-{i:04d}" # Génère ORD-0001, ORD-0002...
        ord_prd_id = [f"PRD-{i:04d}" for i in range(1, 7)]
        salespersons = df_employees[df_employees['EmployeeJobPosition'] == 'Commis aux ventes']['EmployeeID'].tolist()

        # Sélection de type de vente et d'événement aléatoires
        SALES_TYPE = random.choices(SALES_CHANNELS, weights=SALES_CHANNEL_WEIGHTS)[0]
        EVENT_TYPE = random.choices(EVENT_CHANNELS, weights=EVENT_CHANNEL_WEIGHTS)[0]

        # Logique de Quantité intelligente selon l'événement
        if EVENT_TYPE == "Corporate":
            ord_quantity = random.randint(12, 48)
        elif EVENT_TYPE == "Mariage":
            ord_quantity = random.randint(1, 2) # Souvent 1 gros gâteau (PRD-0003)
        elif EVENT_TYPE == "Quotidien":
            ord_quantity = random.randint(1, 6)
        else: # Anniversaire ou Atelier
            ord_quantity = random.randint(1, 10)

        writer.writerow([
            id_trans,
            fake.date_between(start_date=date(2025, 1, 1), end_date=date(2025, 12, 31)),         # Ventes sur l'année civile 2025
            random.choice(salespersons),                                                         # Code de l'employé
            random.choice(ord_prd_id),                                                           # Code du produit
            ord_quantity,                                                                        # Quantité de la vente
            SALES_TYPE,                                                                          # Type de vente
            fake.name(),                                                                         # Le nom est la clé du dictionnaire
            EVENT_TYPE                                                                           # Type d'événement
        ])

print(f"Succès ! Le fichier 'Sales.csv' avec {NB_SALES} SALES a été créé.")


# Création du fichier CSV - Transactions
# with open('Transactions.csv', mode='w', newline='', encoding='utf-8') as fichier:
#     writer = csv.writer(fichier)
    
#     # En-têtes des colonnes
#     writer.writerow(['TransactionID', 'SalesDate', 'EmployeeID', 'ProductCategory', 'SalesAmount'])

#     # Charger les données générées précédemment
#     df_employees = pd.read_csv("Employees.csv")

#     salespersons = df_employees[df_employees['EmployeeDepartment'] == 'Boutique']['EmployeeID'].tolist()

#     ventes_data = []
#     categories = ["Gâteaux", "Viennoiseries", "Pains", "Café & Boissons"]
#     average_price = [45, 15, 6, 5] # Les gâteaux coûtent plus cher

#     for i in range(1000):
#         # Création de mes IDs
#         id_trans = f"TRA-{i:04d}" # Génère TRA-0001, TRA-0002...
        
#         salesperson = random.choice(salespersons)
#         cat_index = random.choices(range(len(categories)), weights=[10, 40, 30, 20])[0]

#         # Un peu de variation dans les prix
#         amount = average_price[cat_index] + random.uniform(-2, 10)

#         # Date sur la dernière année
#         sales_date = fake.date_between(start_date='-1y', end_date='today')       

#         writer.writerow([
#             id_trans,
#             sales_date,
#             salesperson,
#             categories[cat_index],
#             str(round(amount, 2)).replace('.',',')
#         ])

# print(f"Succès ! Le fichier 'Transactions.csv' avec {NB_TRANSACTIONS} TRANSACTIONS a été créé.")