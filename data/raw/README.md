# Données brutes

Ce dossier doit contenir les cinq fichiers de l'archive **EdStats** de la Banque mondiale.
Ils ne sont pas versionnés : `EdStatsData.csv` pèse 326 Mo, au-delà de la limite de
100 Mio par fichier appliquée par GitHub.

## Récupération

1. Télécharger l'archive CSV : <https://databank.worldbank.org/data/download/EdStats_CSV.zip>
   (page du jeu de données : <https://datacatalog.worldbank.org/search/dataset/0038480>)
2. Décompresser le contenu directement dans ce dossier.

## Fichiers attendus

| Fichier | Lignes | Colonnes |
|---|---:|---:|
| `EdStatsCountry.csv` | 241 | 32 |
| `EdStatsCountry-Series.csv` | 613 | 4 |
| `EdStatsSeries.csv` | 3 665 | 21 |
| `EdStatsFootNote.csv` | 643 638 | 5 |
| `EdStatsData.csv` | 886 930 | 70 |

Volumétrie observée lors de l'analyse (novembre 2025). Le jeu de données étant
mis à jour par la Banque mondiale, ces valeurs peuvent différer d'un
téléchargement ultérieur.

Licence : Creative Commons Attribution 4.0.
