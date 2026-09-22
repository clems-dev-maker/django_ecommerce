# 🛒 E-Commerce Django

Une application e-commerce complète développée avec **Django**, **Bootstrap 5**, **JavaScript (AJAX)** et **Stripe**.

L'objectif de ce projet est de proposer une boutique en ligne moderne avec gestion des utilisateurs, panier dynamique, liste de favoris, intégration du paiement Stripe et interface responsive.

---

# ✨ Aperçu du projet

Cette application permet aux utilisateurs de :

- Créer un compte
- Se connecter et se déconnecter
- Parcourir les produits
- Consulter les détails d'un produit
- Ajouter des produits au panier
- Ajouter des produits aux favoris
- Gérer les quantités du panier
- Supprimer des produits du panier
- Effectuer un paiement avec Stripe
- Consulter leur profil utilisateur
- Visualiser leurs favoris
- Recevoir des notifications visuelles (Toast)

---

# 🚀 Fonctionnalités

## 👤 Authentification

- Inscription
- Connexion
- Déconnexion
- Profil utilisateur

---

## 🛍️ Catalogue produits

- Liste des produits
- Fiche produit détaillée
- Images produits
- Gestion du stock
- Affichage de la disponibilité

---

## 🛒 Panier dynamique

- Ajout au panier
- Suppression de produits du panier
- Modification des quantités
- Mise à jour du compteur en temps réel
- Dropdown panier dans la navbar
- Calcul automatique du total

---

## ❤️ Wishlist

- Ajout aux favoris
- Suppression des favoris
- Page dédiée aux favoris
- Bouton dynamique

---

## 💳 Paiement Stripe

- Intégration de Stripe Checkout
- Paiement via Stripe
- Redirection après paiement
- Gestion des commandes

---

## ⭐ Avis clients

- Notes produits
- Commentaires
- Historique des avis

---

## 🔍 Recherche & Filtres

- Recherche par nom
- Filtre par catégorie
- Filtre par prix

---

## 📱 Responsive Design

- Bootstrap 5
- Compatible mobile
- Compatible tablette
- Compatible desktop

---

# 🛠️ Technologies utilisées

## Backend

- Python 3
- Django
- SQLite (développement)
- Stripe API

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- AJAX (Fetch API)

## Bibliothèques

- Pillow
- Stripe
- Font Awesome

---

# 📸 Captures d'écran

## Accueil

![Accueil](screenshots/home.png)

---

## Détail produit

![Produit](screenshots/product_detail.png)

---

## Panier

![Panier](screenshots/cart.png)

---

## Favoris

![Favoris](screenshots/wishlist.png)

---

## Paiement Stripe

![Paiement](screenshots/payment.png)

---

## Profil utilisateur

![Profil](screenshots/profile.png)

---

## 🎬 Démonstration

![Démonstration](screenshots/e_commerce_app.gif)

---

# ⚙️ Installation

## 1. Cloner le projet

```bash
git clone https://github.com/clems-dev-maker/django_ecommerce.git
cd django_ecommerce
2. Créer un environnement virtuel
python -m venv venv
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
3. Installer les dépendances
pip install -r requirements.txt
4. Créer le fichier .env

Créer un fichier .env à la racine du projet :

SECRET_KEY=your_secret_key

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_application_password

STRIPE_PUBLIC_KEY=pk_test_xxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxx

⚠️ Les valeurs ci-dessus sont uniquement des exemples. Ne publiez jamais vos véritables clés ou mots de passe dans le dépôt Git.

5. Effectuer les migrations
python manage.py migrate
6. Créer un super utilisateur
python manage.py createsuperuser
7. Lancer le serveur
python manage.py runserver

Accéder ensuite au site :

http://127.0.0.1:8000/
📂 Structure du projet
django_ecommerce/
│
├── ecommerce/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── shop/
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── templates/
│   │   ├── registration/
│   │   │   ├── login.html
│   │   │   └── signup.html
│   │   │
│   │   └── shop/
│   │       ├── base.html
│   │       ├── product_list.html
│   │       ├── product_detail.html
│   │       ├── cart_detail.html
│   │       ├── wishlist.html
│   │       ├── payment.html
│   │       └── profile.html
│   │
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── context_processors.py
│
├── media/
├── requirements.txt
├── manage.py
├── .gitignore
└── README.md
🔐 Sécurité
Variables d'environnement

Les informations sensibles ne sont pas stockées directement dans le dépôt Git.

Elles sont chargées via un fichier .env.

Exemple
SECRET_KEY=xxxxxxxxxxxx

EMAIL_HOST_USER=xxxxxxxx@gmail.com
EMAIL_HOST_PASSWORD=xxxxxxxx

STRIPE_PUBLIC_KEY=pk_test_xxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxx
Ajouter .env dans .gitignore

Le fichier .env doit être exclu du dépôt Git :

.env
Stripe

Les clés Stripe utilisées en développement sont des clés de test :

STRIPE_PUBLIC_KEY=pk_test_xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx

Ne jamais publier les clés Stripe de production.

📈 Améliorations futures
Historique des commandes
Statuts des commandes
Factures PDF
Coupons de réduction
Recherche AJAX
Pagination
Notifications temps réel
Dashboard administrateur avancé
Déploiement Docker
👨‍💻 Auteur

Clément Cathala

GitHub : clems-dev-maker

Projet réalisé dans le cadre de l'apprentissage du développement web avec Django.

🔗 Voir le projet sur GitHub

📄 Licence

Projet distribué sous licence MIT.

Vous êtes libre de l'utiliser, de le modifier et de le partager.
