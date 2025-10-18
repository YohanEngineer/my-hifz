# My Hifz Planner - Frontend

Interface web moderne et accessible pour la génération de plannings de mémorisation du Coran.

## 🎨 Caractéristiques

### Design & Thème
- **Thème de couleur** : Vert et Blanc
- **Framework** : Bootstrap 5.3.2
- **Responsive** : Compatible web, tablette et mobile
- **Icons** : Bootstrap Icons

### Accessibilité (WCAG 2.1 AA)
- ✅ Navigation au clavier complète
- ✅ Support des lecteurs d'écran (ARIA labels)
- ✅ Contraste de couleurs élevé
- ✅ Focus indicators visibles
- ✅ Skip links pour navigation rapide
- ✅ Messages d'état dynamiques (aria-live)
- ✅ Support du mode sombre (prefers-color-scheme)
- ✅ Support du mode contraste élevé (prefers-contrast)
- ✅ Support réduction de mouvement (prefers-reduced-motion)

### Fonctionnalités
- Formulaire de configuration du planning
- Validation en temps réel des champs
- Génération et téléchargement de PDF
- Messages d'erreur et de succès
- Indicateur de chargement
- Interface multilingue (Français)

## 📁 Structure

```
frontend/
├── index.html          # Page principale
├── css/
│   └── style.css      # Styles personnalisés (thème vert/blanc)
├── js/
│   └── app.js         # Logique de l'application
├── assets/            # Images et autres ressources (vide pour l'instant)
└── README.md          # Cette documentation
```

## 🚀 Utilisation

### Prérequis

Le backend doit être en cours d'exécution sur `http://localhost:8000`.

Pour démarrer le backend :
```bash
cd ..  # Retour au répertoire racine
source .venv/bin/activate
uvicorn main:app --reload
```

### Lancement du Frontend

#### Option 1 : Serveur HTTP Python (Recommandé)
```bash
cd frontend
python3 -m http.server 8080
```

Puis ouvrez : `http://localhost:8080`

#### Option 2 : Serveur Node.js (http-server)
```bash
cd frontend
npx http-server -p 8080
```

#### Option 3 : Ouvrir directement dans le navigateur
Double-cliquez sur `index.html` (les appels API fonctionneront si le backend est actif)

## 🎯 Utilisation de l'Interface

1. **Pages par période** : Entrez le nombre de pages à mémoriser (1-604)
2. **Type de période** : Choisissez Quotidien ou Hebdomadaire
3. **Page de départ** : Entrez la page de début (1-604)
4. **Ordre** : Sélectionnez Croissant (1→604) ou Décroissant (604→1)
5. Cliquez sur **"Générer mon planning PDF"**
6. Le PDF sera téléchargé automatiquement

## 🎨 Personnalisation du Thème

Les couleurs principales sont définies dans `css/style.css` :

```css
:root {
    --primary-green: #2d8659;
    --primary-green-dark: #236b47;
    --primary-green-light: #3fa673;
    --primary-green-lighter: #e8f5f0;
}
```

## 📱 Responsive Design

L'interface s'adapte automatiquement aux différentes tailles d'écran :

- **Desktop** : Layout complet avec colonnes multiples
- **Tablette** : Ajustement des espacements et tailles
- **Mobile** : Layout en colonne unique, boutons pleine largeur

Points de rupture :
- `768px` : Tablette
- `576px` : Mobile

## ♿ Accessibilité

### Navigation au Clavier
- `Tab` : Navigation entre les éléments
- `Shift + Tab` : Navigation arrière
- `Enter` / `Space` : Activer boutons/liens
- `Escape` : Fermer les alertes

### Lecteurs d'Écran
- Tous les champs ont des labels appropriés
- Messages d'erreur associés aux champs (aria-describedby)
- Annonces dynamiques pour les actions (aria-live)
- Skip link pour aller au contenu principal

### Tests d'Accessibilité Recommandés
- WAVE (Web Accessibility Evaluation Tool)
- axe DevTools
- NVDA / JAWS (lecteurs d'écran)
- Lighthouse (Chrome DevTools)

## 🔧 Configuration API

Par défaut, l'API est configurée pour `http://localhost:8000`.

Pour changer l'URL, modifiez dans `js/app.js` :

```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',  // Modifier ici
    API_ENDPOINT: '/api/v1/plan/generate'
};
```

## 🌐 Compatibilité Navigateurs

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Opera 76+
- ✅ Mobile browsers (iOS Safari, Chrome Android)

## 📝 Notes de Développement

### Dépendances CDN
- Bootstrap 5.3.2 (CSS + JS)
- Bootstrap Icons 1.11.1

### Pas de Build Process
Le frontend utilise du HTML/CSS/JS vanilla sans build process. Aucune compilation nécessaire.

### Support Offline
Pour une utilisation offline, téléchargez Bootstrap localement :
```bash
npm install bootstrap bootstrap-icons
# Puis copiez les fichiers dans assets/vendor/
```

## 🐛 Dépannage

### Le PDF ne se télécharge pas
- Vérifiez que le backend est en cours d'exécution
- Ouvrez la console du navigateur (F12) pour voir les erreurs
- Vérifiez que l'URL de l'API est correcte

### Erreur CORS
Si vous avez des erreurs CORS, vérifiez que le backend autorise votre origine dans `main.py` :
```python
allow_origins=["http://localhost:8080", "*"]
```

### Problèmes de style
- Effacez le cache du navigateur (Ctrl+Shift+R)
- Vérifiez que `style.css` est chargé dans les DevTools

## 📄 Licence

Même licence que le projet principal.
