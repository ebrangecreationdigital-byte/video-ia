# Fooocus sur Google Colab (gratuit) : relancer en 5 minutes

Mis en place le 31/10/2026. Tout tourne sur les serveurs de Google (carte T4 gratuite), rien sur le PC.

## Pourquoi une recette spéciale
Le notebook officiel ne marche plus tel quel. Colab utilise maintenant Python 3.13, trop récent pour Fooocus 2.5.5.
La solution : installer Python 3.10 dans Colab, puis fixer quatre paquets.

## Marche à suivre
1. Ouvrir https://colab.research.google.com/github/lllyasviel/Fooocus/blob/main/fooocus_colab.ipynb
   (connecté au compte Google, carte « T4 » en haut à droite).
2. Lancer la première cellule. Elle télécharge Fooocus, puis échoue : c'est normal. Si Colab demande,
   cliquer « Exécuter malgré tout ».
3. Ajouter une cellule (« + Code »), coller ce bloc et le lancer :

```
!pip install -q uv
!uv python install 3.10
!uv venv --seed -p 3.10 /content/fv
!/content/fv/bin/python -m pip install -q pygit2==1.15.1 fastapi==0.104.1 starlette==0.27.0 pydantic==2.9.2
%cd /content/Fooocus
!MPLBACKEND=Agg /content/fv/bin/python entry_with_update.py --share --always-high-vram
```

   Au premier lancement, Fooocus installe ses paquets et télécharge le modèle Juggernaut XL (6,6 Go) :
   compter environ 5 minutes.
4. Si une erreur apparaît encore (`'FieldInfo' object has no attribute 'in_'` ou `unhashable type: 'dict'`),
   arrêter la cellule et relancer seulement les lignes `pip install` des paquets fixés puis la dernière ligne :
   Fooocus réinstalle parfois des versions plus récentes à son démarrage.
5. Cliquer sur le lien `https://xxxx.gradio.live` (« Running on public URL ») qui apparaît en bas.

## À savoir
- Écrire la description en anglais. Exemple testé : « artisan plumber working in a modern bathroom, natural light, photo ».
  Il génère 2 images en environ 20 secondes.
- Garder l'onglet Colab ouvert. Une session fermée ou inactive est coupée, et il faut tout relancer.
- Télécharger ses images : elles sont effacées à la fin de la session.
- Licence : Fooocus est sous GPL-3.0. Les images produites peuvent servir aux vidéos et aux clients.
