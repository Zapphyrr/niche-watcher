# Comprendre l’objectif du projet
Pourquoi Niche Watcher a été créé

## À quoi sert ce projet ?
Niche Watcher est un agrégateur de contenu pensé pour centraliser la veille des développeurs.
L’idée est simple : éviter de perdre du temps à consulter plusieurs sources séparément et recevoir à la place un résumé clair, automatisé et utile.

Le projet récupère des contenus depuis plusieurs sources techniques, les organise, puis les diffuse sous une forme exploitable sur une application mobile et via une newsletter.

Veille automatiséeCentralisation des sourcesGain de temps

# Les statistiques techniques du projet
Ce que l’architecture montre concrètement

## Les points techniques clés
Le projet repose sur une base technique compacte mais complète :

- **Backend FastAPI** pour exposer les endpoints, gérer l’authentification et servir les pages web.
- **Application Flutter** pour proposer une interface mobile moderne et cross-platform.
- **PostgreSQL** comme base de données principale pour stocker les utilisateurs, les posts et les préférences.
- **Scheduler Python** exécuté de façon planifiée pour automatiser la collecte et l’envoi.
- **Sources RSS + Reddit** pour agréger du contenu provenant de plusieurs flux dev.
- **Envoi d’emails** pour distribuer la newsletter hebdomadaire aux utilisateurs inscrits.

API moderneApplication mobileBase de données relationnelleAutomatisation

# Le fonctionnement du projet
Voici comment Niche Watcher transforme plusieurs sources en une veille claire et centralisée.

## 1. Connexion des sources de contenu
Le système récupère les articles depuis des flux RSS techniques et les publications les plus pertinentes d’une communauté Reddit orientée développement.

Cette étape permet d’agréger automatiquement plusieurs points de veille sans intervention manuelle.

## 2. Stockage et organisation des données
Les contenus collectés sont enregistrés dans PostgreSQL avec les informations utiles pour le tri, l’affichage et le suivi.

La base contient aussi les données utilisateurs, comme l’adresse email, le token de connexion et l’état d’inscription à la newsletter.

## 3. Authentification des utilisateurs
Le projet propose un espace connecté avec inscription, connexion et gestion du profil utilisateur.

Cela permet de personnaliser l’accès aux contenus et de gérer les préférences de diffusion.

## 4. Automatisation hebdomadaire
Un scheduler Python lance les tâches planifiées chaque semaine pour collecter les nouvelles données et préparer l’envoi.

Le but est de garder un système vivant sans dépendre d’une action manuelle quotidienne.

## 5. Diffusion de la newsletter
Les utilisateurs inscrits reçoivent une synthèse des contenus sélectionnés.

Le projet ne se limite donc pas à afficher de l’information : il la transforme en expérience utile et récurrente.

# Ce que le projet permet de réaliser

## Résultat final
Niche Watcher démontre la mise en place d’un produit complet de veille technique : collecte automatisée, stockage, authentification, interface web, application mobile et distribution par newsletter.

## Compétences mises en avant
Ce projet montre une bonne maîtrise de plusieurs sujets essentiels :

- Architecture backend avec API.
- Gestion des utilisateurs et des permissions.
- Manipulation de bases de données relationnelles.
- Automatisation de tâches planifiées.
- Intégration de sources externes.
- Conception d’une interface mobile claire et exploitable.

## Ce que j’ai appris
Ce projet m’a permis de travailler sur une vraie chaîne complète de produit : récupérer l’information, la traiter, la stocker, la présenter et la diffuser.

Il m’a aussi aidé à structurer une application avec plusieurs couches techniques qui collaborent ensemble pour offrir une expérience simple côté utilisateur.
