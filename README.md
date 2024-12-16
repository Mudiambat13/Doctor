# 🏥 MediConnect

[![Repo](https://img.shields.io/badge/GitHub-Doctor%20Connect-blue?style=flat-square&logo=github)](https://github.com/Mudiambat13/Doctor)
[![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 À propos
Doctor Connect est une plateforme web innovante permettant des consultations médicales en ligne entre patients et médecins. Notre solution vise à démocratiser l'accès aux soins médicaux, particulièrement pour les personnes à mobilité réduite ou recherchant un diagnostic rapide à domicile.

## ✨ Fonctionnalités principales

🏥 **Consultations en ligne**
- Connexion en temps réel entre patients et médecins
- Interface intuitive pour les consultations virtuelles

👥 **Gestion des utilisateurs**
- Système d'authentification sécurisé
- Gestion des rôles (patients/médecins)
- Profils personnalisables

🔒 **Sécurité & Confidentialité**
- Protection des données médicales
- Conformité aux normes de santé

## 🛠️ Technologies utilisées

### Backend
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/-Django%20REST-ff1709?style=for-the-badge&logo=django&logoColor=white)

### Frontend
![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Tailwind](https://img.shields.io/badge/-Tailwind%20CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## 📋 Prérequis
- Python 3.x
- pip (gestionnaire de paquets Python)
- Node.js et npm (pour Tailwind CSS)

## 🚀 Installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/Mudiambat13/Doctor.git
cd Doctor
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances Python**
```bash
pip install -r requirements.txt
```

4. **Installer les dépendances Node.js**
```bash
npm install
```

5. **Configurer Tailwind CSS**
```bash
npm install -D tailwindcss
npx tailwindcss init
```

## 📦 Dépendances principales

### Python
```
Django==5.0.1
djangorestframework==3.14.0
django-cors-headers==4.3.1
python-dotenv==1.0.0
pillow==10.2.0
django-allauth==0.60.0
dj-rest-auth==5.0.2
djangorestframework-simplejwt==5.3.1
requests==2.31.0
cryptography==42.0.2
```

### Node.js
```json
{
  "devDependencies": {
    "tailwindcss": "^3.x",
    "autoprefixer": "^10.x",
    "postcss": "^8.x"
  }
}
```

## 📝 License
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou soumettre une pull request.