---
name: video-ia
description: Produire une vidéo IA « faceless » de A à Z (script, voix off IA, images ou clips IA, montage automatique avec sous-titres, publication TikTok/Reels/Shorts/YouTube). À utiliser quand on demande une vidéo IA, une voix off, un Short/TikTok/Reel, une vidéo à partir d'un texte ou d'images, ou des visuels animés pour les réseaux.
---

# Vidéo IA « faceless »

But : sortir une vidéo propre, sourcée et publiable sans tournage ni visage à l'écran. Le montage se fait tout seul
avec `scripts/fabriquer_video.py` (texte + images → voix off + sous-titres mot à mot + zoom lent → MP4).

## 1. Cadrer (2 minutes)
- **Plateforme et format** : TikTok / Reels / Shorts = vertical 9:16, 20 à 60 s. YouTube = 16:9 (`--format paysage`).
- **Une seule idée par vidéo**, une promesse dans les 2 premières secondes (question, chiffre, erreur courante).
- **Public visé** et **appel à l'action** (suivre, commenter un mot, lien en bio).

## 2. Script
- 130 à 150 mots par minute de vidéo. Phrases courtes, à dire à voix haute.
- Structure : accroche (1 phrase) → 3 points concrets → chute ou appel à l'action.
- Pas de chiffre sans source. Pas de promesse de résultat garanti.
- S'il existe une charte de rédaction dans le projet (ex. `CHARTE-REDACTION-HUMAINE.md`), la suivre et passer le
  vérificateur avant d'enregistrer la voix.
- Enregistrer le script en UTF-8 dans `script.txt`.

## 3. Images
- Une image toutes les 3 à 5 secondes : `nombre d'images ≈ durée / 4`.
- Nommer `01.png`, `02.png`… : le script les prend dans l'ordre alphabétique.
- Sources possibles :
  - **Images IA gratuites** : Fooocus sur Google Colab. Recette qui marche en 2026, avec Python 3.10 et les paquets fixés :
    `references/fooocus-colab.md`. Prompts en anglais, ex. « artisan plumber working in a modern bathroom, natural light, photo ».
    Réglages pour TikTok : Advanced → Aspect Ratios 768×1344, Image Number 1 (environ 50 s par image sur une T4).
    Récupérer une image : son adresse dans la page est `…gradio.live/file=/tmp/fooocus/…/AAAA-MM-JJ_hh-mm-ss_NNNN.png`,
    à télécharger avec `curl -o 01.png "<adresse>"` (le navigateur bloque l'envoi direct vers le PC).
    Défaut connu : le texte affiché sur les écrans de téléphone est illisible. Éviter les gros plans d'écran, ou les cacher
    sous un sous-titre.
  - **Captures d'écran** ou photos réelles du sujet. C'est souvent plus crédible que l'IA pour une vidéo d'expert.
  - **Clips vidéo IA** (images animées, mouvement réaliste) : outils et prompts dans `references/video-realiste.md`.
    Le script les accepte directement (`.mp4`, `.mov`, `.webm`, `.mkv`), mélangés ou non avec des images fixes :
    chaque clip est recadré, son propre son est coupé, et sa dernière image reste affichée s'il est plus court que sa part
    de la voix. Méthode conseillée : faire l'image avec Fooocus, puis l'animer (Veo 3.1 dans Google Flow, 4 à 8 s).
- Interdit : le visage d'une personne réelle sans son accord, les logos et marques d'autrui, les images « à la manière de »
  d'un artiste vivant nommé.

## 4. Fabriquer la vidéo
```bash
pip install edge-tts          # mettre à jour si erreur 403 : pip install --upgrade edge-tts
python scripts/fabriquer_video.py --texte script.txt --images images --sortie ma_video
```
Options utiles :
- `--voix fr-FR-DeniseNeural` (féminine), `fr-FR-HenriNeural` (défaut), `fr-FR-RemyMultilingualNeural`.
  Liste complète : `edge-tts --list-voices`.
- `--debit +10%` pour un rythme plus nerveux sur TikTok.
- `--mots-par-ligne 3` pour des sous-titres plus courts.
- `--format paysage` pour YouTube, `--format carre`.
- `--voix-fichier voix.mp3 --srt voix.srt` pour monter avec une voix déjà enregistrée (ex. rendu Azure, voir §5).

Sortie : `ma_video/voix.mp3`, `ma_video/sous-titres.srt`, `ma_video/video.mp4`.

**Vérifier avant de livrer** : regarder la vidéo en entier. Extraire une image pour contrôle rapide :
`ffmpeg -ss 5 -i ma_video/video.mp4 -frames:v 1 apercu.png`. Contrôler :
- que les sous-titres sont lisibles et non coupés ;
- que les mots sont prononcés correctement (corriger l'orthographe phonétique dans le script si besoin) ;
- que rien n'est affirmé sans source.

## 5. Voix off : produire vs publier
| Usage | Outil | Pourquoi |
|---|---|---|
| Produire, tester, itérer | `edge-tts` (gratuit, sans compte) | Instantané. Mais il passe par un service non officiel de Microsoft : droits commerciaux non garantis. |
| Publier une vidéo **monétisée** | **Azure AI Speech** (palier gratuit, droits commerciaux) | Mêmes voix neuronales, rendu identique. |

Pour la version monétisée : générer la voix finale avec Azure (fichier audio + sous-titres), puis
`--voix-fichier` et `--srt`.

## 6. Publier
- **Cocher l'étiquette « contenu généré par IA »** sur TikTok (« AI-generated content ») et sur YouTube
  (« contenu modifié ou synthétique ») dès qu'une voix ou une image réaliste est générée.
- Musique : uniquement la bibliothèque de la plateforme ou une musique libre de droits avec licence.
- Titre et description : la promesse de l'accroche, 3 à 5 hashtags précis, pas de mots-clés trompeurs.
- Une vidéo longue YouTube peut donner 3 à 5 Shorts : relancer le script avec un extrait du texte.

## 7. Dépannage
- `403 Invalid response status` avec edge-tts : `pip install --upgrade edge-tts` (Microsoft change sa clé).
- `ffmpeg introuvable` : installer ffmpeg (Windows : `winget install Gyan.FFmpeg`) puis rouvrir le terminal.
- Sous-titres décalés : texte avec abréviations ou chiffres (« 3 € » lu « trois euros »). Écrire en toutes lettres.
- Vidéo trop longue pour TikTok : couper le script, pas la vidéo.
