# video-ia : un skill Claude pour des vidéos IA « faceless »

Un skill pour [Claude Code](https://claude.com/claude-code) qui produit une vidéo courte de A à Z :
script → voix off IA → images → montage automatique (zoom lent + sous-titres mot à mot) → MP4 prêt pour TikTok,
Reels, Shorts ou YouTube. Pas de tournage, pas de visage à l'écran, pas de logiciel payant.

## Ce que fait le script
```
python scripts/fabriquer_video.py --texte script.txt --images images --sortie ma_video
```
- Voix off avec [edge-tts](https://github.com/rany2/edge-tts) et la position de chaque mot.
- Sous-titres de 4 mots, ponctuation reprise du texte d'origine, coupés à la fin des phrases.
- Chaque image prend une part égale de la durée, recadrée pour remplir l'écran, avec un zoom lent.
- Assemblage ffmpeg en 1080×1920 (ou 1920×1080 / 1080×1080), H.264 + AAC, prêt à publier.

Test : un texte de 37 mots et 3 images donnent une vidéo de 14,4 s en environ 35 s sur un portable sans carte graphique.

## Installation
1. Python 3.9 ou plus, puis `pip install edge-tts`.
2. ffmpeg dans le PATH (Windows : `winget install Gyan.FFmpeg`, macOS : `brew install ffmpeg`).
3. Copier le dossier `video-ia` dans `~/.claude/skills/`. Claude le propose dès qu'on parle de vidéo IA.

Le script marche aussi seul, sans Claude.

## Contenu
- `SKILL.md` : la méthode complète (cadrage, script, images, voix, publication, dépannage).
- `scripts/fabriquer_video.py` : le montage automatique.
- `references/fooocus-colab.md` : générer les images gratuitement avec Fooocus sur Google Colab (recette Python 3.10 qui marche en 2026).
- `references/video-realiste.md` : outils et méthodes pour des clips vidéo IA réalistes.

## À savoir
- edge-tts utilise un service non officiel de Microsoft. Pour une vidéo **monétisée**, générez la voix finale avec
  Azure AI Speech (mêmes voix, droits commerciaux), puis `--voix-fichier` et `--srt`.
- Déclarez le contenu généré par IA sur TikTok et YouTube.
- N'utilisez pas le visage ou la voix d'une personne réelle sans son accord.

## Licence
MIT. Voir `LICENSE`.
