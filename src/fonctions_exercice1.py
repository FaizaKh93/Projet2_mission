#=============================================================================================================
# Créée le 26/11/2025
# Par Faïza Khelladi
# Ce fichier contient plusieurs fonctions utilisées dans l'exercice du projet 2
#=============================================================================================================
# Fonction 1 : retourne les réponses aux questions de l'éxercice étape1 pour tout les fichiers csv fournis
#=============================================================================================================
def DataProcessing(Data, fileName):
    # Fonction qui traite les questions de l'exercice 1 - projet 2

    #================================================
    print("1.2 Visualisation des 5 premières lignes")
    #================================================
    display(Data.head())
    #================================================
    print("Etape 2")
    #================================================
    print("2.1 Ce que représente chaque ligne :")
    #================================================
    if fileName == "EdStatsSeries.csv":
        print("Ce fichier décrit une liste d'indicateurs où chaque ligne correspond à un indicateur unique avec son 'Series Code', son 'Indicator Name', sa 'Short definition', etc.")
    elif fileName == "EdStatsCountry.csv":
        print("Chaque ligne représente un pays avec ces informations : code, nom court, etc.")
    elif fileName == "EdStatsCountry-Series.csv":
        print("Chaque ligne correspond à une combinaison entre pays et indicateurs. On y trouve le code du pays, le code de l'indicateur et une description")
    elif fileName == "EdStatsFootNote.csv":
        print("Chaque ligne représente une note associant un pays avec un indicateur pour une année donnée")
    elif fileName == "EdStatsData.csv":
        print("Chaque ligne représente les données annuels d'un indicateur pour un pays donné")
    else:
        print("Fichier inconnu")
        
    #================================================
    print("2.2 Nombre de lignes et de colonnes")
    #================================================
    Data.shape
    print("le nombre de lignes est de", Data.shape[0], "et le nombre de colonnes est de", Data.shape[1])


    #================================================
    print("2.3 Nombre de doublons dans le jeu de données")
    #================================================
    Nb_doublons_Data = Data.duplicated().sum()
    print("le nombre de doublons est de",Nb_doublons_Data)
    print("Suppression des doublons (inutile dans ce cas, mais à garder pour les autres fichiers csv)")
    Data = Data.drop_duplicates()
    display(Data.head())
    
    #================================================
    print("2.4 Calcul de la proportion de valeurs manquantes par colonne")
    #================================================
    valeursManquantes = Data.isna()
    display(valeursManquantes.head())
    
    print("Moyenne en % des valauers manquantes par colonne")

    valeursManquantes_moyenne= Data.isna().mean()*100
    display(valeursManquantes_moyenne)

    print("Suppression des colonnes vides où valeursManquantes_moyenne vaut une certaine valeur")
    #Data_clean = Data.drop(columns=valeursManquantes_moyenne[valeursManquantes_moyenne>=94].index)
    #display(Data_clean)

    if (fileName == "EdStatsSeries.csv") | (fileName == "EdStatsCountry.csv") | (fileName == "EdStatsCountry-Series.csv" )| (fileName == "EdStatsFootNote.csv"):
        print("Suppression des colonnes vides où valeursManquantes_moyenne == 60 %")
        Data_clean = Data.drop(columns=valeursManquantes_moyenne[valeursManquantes_moyenne>=60].index)
        display(Data_clean)

    elif fileName == "EdStatsData.csv":
        print("Suppression des colonnes vides où valeursManquantes_moyenne == 98 %")
        Data_clean = Data.drop(columns=valeursManquantes_moyenne[valeursManquantes_moyenne>=98].index)
        display(Data_clean)
    else:
        print("Fichier inconnu")


    

    #Data_clean.tail(20)

    #================================================
    print("2.5 Calcul des statistiques descriptives basiques en utilisant describe() pour les colonnes numériques")
    #================================================
    colonnes_numeriques = Data_clean.select_dtypes(include = 'number')
    print("nombre de colonnes numérique =",colonnes_numeriques.shape[1])

    display(colonnes_numeriques.info(verbose=True))

    #================================================
    print("2.6 Calcul du nombre d'occurrences de chaque valeur possible de la colonne pour les colonnes catégorielles")
    #================================================
    colonnes_categorielles = Data_clean.select_dtypes(include = 'object')
    colonnes_categorielles.shape
    for col_cat in colonnes_categorielles:
        print(Data_clean[col_cat].value_counts())
        print("==============================================================================================")
        print("==============================================================================================")

    #================================================
    print("Etape 3")
    #================================================
    if fileName == "EdStatsCountry.csv":
        print("3.1 Définitions des faux pays")
        print("Chaque pays a un code alpha-2 de deux lettres et une région, les pays ne respectant pas ce format de code sont de faux pays")
        #mask_2alpha= Data_clean["2-alpha code"].str.len().eq(2) & Data_clean["2-alpha code"].str.isalpha()

        # les pays n'ayant qu'une "Région" et pas de "2-alpha code" sont considérés comme vrais pays (manque de données)
        mask_2alpha= (((Data_clean["2-alpha code"].str.len().eq(2)) & (Data_clean["2-alpha code"].str.isalpha())) & (~Data_clean['Region'].isna())) | ((~Data_clean['Region'].isna()) & (Data_clean['2-alpha code'].isna()))

        display(mask_2alpha)
        
        print("Cases vides dans la colonne code alpha-2")
        display(Data_clean["2-alpha code"].isnull())

        print("Liste des faux pays :")
        #falseCountries =Data_clean[mask_2alpha == False | (Data_clean["2-alpha code"].isna())]["Country Code"].tolist()
        falseCountries =Data_clean[mask_2alpha == False]["Country Code"].tolist()

        display(falseCountries)
        print("Nombre de faux pays :", len(falseCountries))


        print("3.2 Définitions des vrais pays")
        print("Liste des vrais pays :")
        trueCountries = Data_clean[~Data_clean["Country Code"].isin(falseCountries)].reset_index()
        display(trueCountries.head(10))
        trueCountries.reset_index(drop=True)
        display(trueCountries.head(10))
        print("Nombre de vrais pays :", len(trueCountries))
    else:
        trueCountries = []
        falseCountries = []
        print("Fichier non concerné")
        
    return Data_clean, trueCountries, falseCountries

#=============================================================================================================
#=============================================================================================================
#=============================================================================================================
#=============================================================================================================
# Fonction 2 : retourne la dernière valeur renseignée non null
#=============================================================================================================
def derniere_valeur_non_nulle(row):
    # On récupère les valeurs non NaN et non nulles
    derniere_valeur = row.dropna() # supprimer les valeurs manquantes
    derniere_valeur = derniere_valeur[derniere_valeur != 0] # filtrer les valeurs nulles

    if len(derniere_valeur) > 1:
        Q1 = derniere_valeur.quantile(0.25)
        Q3 = derniere_valeur.quantile(0.75)
        IQR = Q3 - Q1

        borne_basse = Q1 - 1.5 * IQR
        borne_haute = Q3 + 1.5 * IQR
        
    # filtrage des outliers
    derniere_valeur = derniere_valeur[(derniere_valeur >= borne_basse) & (derniere_valeur <= borne_haute)]
    
    # Si au moins une valeur valide existe → on prend la dernière
    if len(derniere_valeur) > 0:
        return derniere_valeur.iloc[-1] # prendre la dernière valeurs renseignée 
    else:
        return 0  # ou np.nan si tu préfères


#def DataMerge(Data, fileName):