# WatermarkRemover

Application moderne de suppression de filigrane vidéo avec interface glassmorphism ultra-moderne.

## Vue d'ensemble

WatermarkRemover est un outil de traitement vidéo qui utilise ProPainter pour effectuer de l'inpainting haute qualité sur des zones définies par l'utilisateur. L'interface utilise un design glassmorphism avec effets Acrylic/Mica sous Windows 10/11.

**Version:** 2.0.0

## Stack technique

### UI Framework
- **PySide6** (Qt for Python) - Framework UI principal
- **qframelesswindow** - Effets Acrylic/Mica natifs Windows
- **PySide6-Fluent-Widgets** - Composants UI modernes
- **pyqt-frameless-window** - Fenêtre sans bordure personnalisée
- **darkdetect** - Détection du thème système

### Traitement vidéo
- **PyTorch** (>=2.0.0) - Deep learning backend
- **torchvision** - Transformations et modèles vision
- **OpenCV** (opencv-python) - Manipulation vidéo/image
- **Pillow** - Traitement d'images supplémentaire
- **imageio** + **imageio-ffmpeg** - I/O vidéo

### Utilities
- **numpy** - Calculs numériques
- **tqdm** - Barres de progression
- **requests** - Téléchargement de modèles

## Architecture

```
WatermarkRemover/
├── main.py                      # Point d'entrée principal
├── src/
│   ├── app.py                   # Application orchestrator
│   ├── core/                    # Logique métier
│   │   ├── video_player.py      # Lecteur vidéo
│   │   └── keyframe_manager.py  # Gestion des keyframes/zones
│   ├── ui/                      # Composants UI principaux
│   │   ├── main_window.py       # Fenêtre principale (Acrylic)
│   │   ├── sidebar.py           # Barre latérale de contrôle
│   │   ├── canvas_area.py       # Zone d'affichage vidéo
│   │   └── timeline.py          # Timeline de navigation
│   ├── components/              # Composants UI réutilisables
│   │   ├── glass_panel.py       # Panel avec effet glassmorphism
│   │   ├── glow_button.py       # Bouton avec effet de lueur
│   │   ├── gradient_progress.py # Barre de progression dégradée
│   │   └── icon_button.py       # Bouton icône
│   ├── styles/
│   │   ├── stylesheet.qss       # Styles globaux glassmorphism
│   │   └── colors.py            # Palette de couleurs
│   └── icons/                   # Icônes et ressources
├── propainter/                  # Module ProPainter (inpainting)
├── output/                      # Vidéos traitées
└── requirements.txt
```

## Design System

### Thème: Deep Space + Vibrant Orange Glow

**Couleurs principales:**
- Background: `#0f0f1e` → `#1a1a2e` (gradient deep space)
- Accent primaire: `#ff6b35` → `#f7931e` (orange vibrant)
- Glass panels: `rgba(42, 42, 72, 0.85)` avec blur backdrop
- Text primaire: `#ffffff`
- Text secondaire: `#8a8aa0`

**Effets visuels:**
- Glassmorphism avec blur et transparence
- Acrylic/Mica effects (Windows 10/11)
- Glow effects sur les boutons primaires
- Animations smooth sur hover/press
- Ombres portées douces

### Composants personnalisés

#### GlassPanel
Panel avec effet verre dépoli:
```python
from src.components.glass_panel import GlassPanel

panel = GlassPanel()
panel.set_padding(24)
```

#### GlowButton
Bouton primaire avec effet de lueur orange:
```python
from src.components.glow_button import GlowButton

btn = GlowButton("Process Video")
btn.clicked.connect(handler)
```

#### GradientProgress
Barre de progression avec gradient orange:
```python
from src.components.gradient_progress import GradientProgress

progress = GradientProgress()
progress.set_progress(50, 100)
```

## Patterns de code

### Architecture MVC-like

**Model:** `VideoPlayer`, `KeyframeManager`
**View:** Components UI (`MainWindow`, `Sidebar`, etc.)
**Controller:** `WatermarkRemoverApp` (orchestration)

### Signal/Slot Pattern (Qt)

Communication entre composants via signals:
```python
# Définition
class Sidebar(GlassPanel):
    process_clicked = Signal()

# Connexion
self.sidebar.process_clicked.connect(self._start_processing)

# Émission
self.process_clicked.emit()
```

### Worker Thread Pattern

Traitement vidéo en arrière-plan:
```python
# Création worker + thread
worker = ProcessingWorker(video_path, output_path, keyframes)
thread = QThread()

worker.moveToThread(thread)
thread.started.connect(worker.run)
worker.progress.connect(self._on_progress)
worker.finished.connect(self._on_finished)

thread.start()
```

### Keyframe Zone Management

Les zones sont interpolées entre keyframes:
```python
keyframes = {
    0: [(x1, y1, x2, y2)],      # Frame 0: une zone
    100: [(x1, y1, x2, y2)],    # Frame 100: zone mise à jour
    200: []                     # Frame 200: zone supprimée
}
```

Frames 0-99: utilise la zone du keyframe 0
Frames 100-199: utilise la zone du keyframe 100
Frames 200+: aucune zone

## Commandes utiles

### Installation
```bash
# Installer les dépendances
pip install -r requirements.txt

# Télécharger le modèle ProPainter
python download_model.py
```

### Exécution
```bash
# Lancer l'application
python main.py

# Ou avec les batch files
run.bat
```

### Développement
```bash
# Recharger les styles (pendant dev)
# Modifier src/styles/stylesheet.qss
# Redémarrer l'app pour voir les changements
```

## Workflow utilisateur

1. **Charger une vidéo**: Sidebar → "Open Video"
2. **Naviguer**: Timeline slider ou boutons frame par frame
3. **Définir zones**: Dessiner des rectangles sur les filiganes
4. **Ajouter keyframes**: Définir des zones à différents moments
5. **Sauvegarder keyframes**: Sidebar → "Save Keyframes" (JSON)
6. **Sélectionner output**: Sidebar → "Select Output Folder"
7. **Traiter**: Sidebar → "Process Video"
8. **Résultat**: Vidéo nettoyée dans `output/clean_*.mp4`

## Points techniques importants

### High DPI Support
```python
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)
```

### Gestion des imports relatifs/absolus
Le code supporte à la fois:
- Exécution directe: `python src/app.py`
- Import module: `from src.app import WatermarkRemoverApp`

Grâce au pattern:
```python
if __name__ == "__main__" and __package__ is None:
    # Imports absolus
else:
    # Imports relatifs
```

### Stylesheet injection
Les styles QSS sont chargés au démarrage:
```python
stylesheet_path = Path(__file__).parent / "src" / "styles" / "stylesheet.qss"
with open(stylesheet_path, "r", encoding="utf-8") as f:
    app.setStyleSheet(f.read())
```

### Canvas drawing
Le canvas utilise QPainter pour dessiner:
- Frame vidéo en background
- Overlay des zones (rectangles semi-transparents)
- Zones en cours de dessin

## Fichiers de configuration

### Keyframes JSON
Sauvegardés automatiquement comme `{video_name}_keyframes.json`:
```json
{
  "0": [
    [100, 100, 300, 200]
  ],
  "150": [
    [110, 105, 310, 205]
  ]
}
```

## ProPainter Integration

Le module `propainter/` contient la logique d'inpainting:
```python
from propainter import process_video

process_video(
    video_path="input.mp4",
    output_path="output.mp4",
    keyframes={0: [(x1, y1, x2, y2)]},
    progress_callback=lambda cur, total: print(f"{cur}/{total}")
)
```

## TODO / Améliorations futures

- [ ] Batch processing UI
- [ ] Undo/Redo pour les zones
- [ ] Preview en temps réel avec inpainting
- [ ] Export de keyframes réutilisables
- [ ] Support de masques personnalisés (pas que rectangles)
- [ ] Optimisation GPU configurable
- [ ] Support Linux/macOS (actuellement optimisé Windows)

## Dépannage

**Erreur: "ProPainter module not found"**
→ Exécuter `python download_model.py`

**Interface non glassmorphism**
→ `qframelesswindow` non installé ou pas sur Windows
→ Fallback automatique vers interface standard

**Vidéo ne charge pas**
→ Vérifier que ffmpeg est accessible
→ Formats supportés: mp4, avi, mov, mkv, webm
