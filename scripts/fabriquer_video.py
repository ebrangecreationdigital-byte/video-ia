"""Fabrique une vidéo « faceless » à partir d'un texte et d'un dossier d'images.

    python fabriquer_video.py --texte script.txt --images dossier_images --sortie ma_video

Étapes :
  1. Voix off avec edge-tts, plus la position de chaque mot.
  2. Sous-titres courts (quelques mots à la fois) tirés de ces positions → sous-titres.srt
  3. Chaque image reçoit une part égale de la durée, avec un zoom lent (effet « Ken Burns »).
  4. Assemblage avec ffmpeg : images + voix + sous-titres incrustés → video.mp4

Dépendances : Python 3.9+, `pip install edge-tts`, ffmpeg dans le PATH.
Formats : 9:16 (TikTok, Reels, Shorts) par défaut, 16:9 avec --format paysage.

⚠️ edge-tts passe par un service non officiel de Microsoft : très bien pour produire et tester.
Pour une vidéo monétisée, générez la voix finale avec Azure AI Speech (mêmes voix, droits commerciaux),
puis passez le fichier avec --voix-fichier et --srt.
"""

import argparse
import asyncio
import re
import shutil
import subprocess
import sys
from pathlib import Path

FORMATS = {"vertical": (1080, 1920), "paysage": (1920, 1080), "carre": (1080, 1080)}
VIDEOS = {".mp4", ".mov", ".webm", ".mkv"}
EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"} | VIDEOS


def horodatage(secondes):
    ms = int(round(secondes * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


async def generer_voix(texte, voix, debit, mp3):
    """Écrit le MP3 et renvoie la liste (mot, début en s, fin en s)."""
    import edge_tts

    com = edge_tts.Communicate(texte, voix, rate=debit, boundary="WordBoundary")
    mots = []
    with open(mp3, "wb") as f:
        async for bloc in com.stream():
            if bloc["type"] == "audio":
                f.write(bloc["data"])
            elif bloc["type"] == "WordBoundary":
                debut = bloc["offset"] / 1e7  # unités de 100 ns
                mots.append((bloc["text"], debut, debut + bloc["duration"] / 1e7))
    return mots


def remettre_ponctuation(mots, texte):
    """edge-tts renvoie les mots sans ponctuation : on les reprend dans le texte d'origine,
    avec tout ce qui les suit jusqu'au mot suivant (« client ? », « Un : »)."""
    positions, curseur = [], 0
    for mot, _, _ in mots:
        i = texte.find(mot, curseur)
        positions.append(i)
        if i >= 0:
            curseur = i + len(mot)
    resultat = []
    for k, (mot, debut, fin) in enumerate(mots):
        i = positions[k]
        if i < 0:
            resultat.append((mot, debut, fin))
            continue
        suivant = next((p for p in positions[k + 1:] if p >= 0), len(texte))
        resultat.append((texte[i:suivant].strip() or mot, debut, fin))
    return resultat


def ecrire_srt(mots, srt, par_ligne):
    """Regroupe les mots par paquets courts ; coupe aussi après une ponctuation forte."""
    paquets, courant = [], []
    for mot in mots:
        courant.append(mot)
        if len(courant) >= par_ligne or mot[0].rstrip()[-1:] in ".!?…":
            paquets.append(courant)
            courant = []
    if courant:
        paquets.append(courant)
    with open(srt, "w", encoding="utf-8") as f:
        for i, p in enumerate(paquets, 1):
            fin = paquets[i][0][1] if i < len(paquets) else p[-1][2]  # pas de trou entre deux lignes
            # Trait d'union insécable (U+2011) : libass coupait « avant-après » en « avant / -après ».
            ligne = re.sub(r"(?<=\w)-(?=\w)", "‑", " ".join(m[0] for m in p))
            f.write(f"{i}\n{horodatage(p[0][1])} --> {horodatage(fin)}\n{ligne}\n\n")


def duree_audio(fichier):
    sortie = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(fichier)],
        capture_output=True, text=True, check=True)
    return float(sortie.stdout.strip())


def monter(images, mp3, srt, dossier, largeur, hauteur, fps, police):
    duree = duree_audio(mp3)
    images_par_segment = max(1, round(duree / len(images) * fps))
    segments = []
    for i, img in enumerate(images):
        seg = dossier / f"segment_{i:03}.mp4"
        if img.suffix.lower() in VIDEOS:
            # Clip animé (Veo, Kling, Wan…) : recadré pour remplir le cadre, son coupé (la voix off reste seule),
            # dernière image figée si le clip est plus court que sa part de la voix.
            filtre = (f"scale={largeur}:{hauteur}:force_original_aspect_ratio=increase,crop={largeur}:{hauteur},"
                      f"fps={fps},tpad=stop_mode=clone:stop_duration=600,format=yuv420p")
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", str(img), "-vf", filtre, "-an",
                 "-frames:v", str(images_par_segment), "-c:v", "libx264", "-preset", "veryfast", str(seg)],
                check=True)
            segments.append(seg)
            continue
        # Image fixe : on agrandit (x2) puis recadre pour remplir le cadre, puis zoom lent de 1,00 à 1,15.
        filtre = (
            f"scale={largeur * 2}:{hauteur * 2}:force_original_aspect_ratio=increase,"
            f"crop={largeur * 2}:{hauteur * 2},"
            f"zoompan=z='min(zoom+{0.15 / images_par_segment:.6f},1.15)':d={images_par_segment}:"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={largeur}x{hauteur}:fps={fps},"
            "format=yuv420p"
        )
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(img), "-vf", filtre,
             "-frames:v", str(images_par_segment), "-c:v", "libx264", "-preset", "veryfast", str(seg)],
            check=True)
        segments.append(seg)

    liste = dossier / "segments.txt"
    liste.write_text("".join(f"file '{s.name}'\n" for s in segments), encoding="utf-8")
    # libass travaille dans un cadre de 384x288 : taille et marge sont exprimées dans ce repère.
    # En vertical, sous-titres remontés vers le tiers bas (MarginV=85, soit environ 30 % du bas) : sur TikTok,
    # Reels et Shorts, la légende et les boutons recouvrent le bas de l'écran.
    vertical = hauteur > largeur
    style = (f"FontName={police},FontSize={16 if vertical else 18},Bold=1,"
             "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,"
             f"Alignment=2,MarginV={85 if vertical else 30}")
    # Chemins relatifs + cwd = dossier : évite l'échappement des « C:\ » dans le filtre subtitles.
    commande = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", liste.name,
                "-i", Path(mp3).name]
    if srt:
        commande += ["-vf", f"subtitles={Path(srt).name}:force_style='{style}'"]
    commande += ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "192k",
                 "-shortest", "-movflags", "+faststart", "video.mp4"]
    subprocess.run(commande, check=True, cwd=dossier)
    for s in segments:
        s.unlink()
    liste.unlink()
    return dossier / "video.mp4", duree


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--texte", help="fichier texte du script (UTF-8)")
    p.add_argument("--images", required=True, help="dossier d'images, utilisées dans l'ordre alphabétique")
    p.add_argument("--sortie", required=True, help="dossier de sortie (créé si besoin)")
    p.add_argument("--voix", default="fr-FR-HenriNeural", help="voix edge-tts (ex. fr-FR-DeniseNeural)")
    p.add_argument("--debit", default="+0%", help="vitesse de la voix, ex. +10%%")
    p.add_argument("--format", choices=FORMATS, default="vertical")
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--mots-par-ligne", type=int, default=4)
    p.add_argument("--police", default="Arial")
    p.add_argument("--sans-sous-titres", action="store_true")
    p.add_argument("--voix-fichier", help="voix déjà enregistrée (ex. rendu Azure) à la place d'edge-tts")
    p.add_argument("--srt", help="sous-titres existants, avec --voix-fichier")
    a = p.parse_args()

    for outil in ("ffmpeg", "ffprobe"):
        if not shutil.which(outil):
            sys.exit(f"{outil} introuvable : installez ffmpeg et ajoutez-le au PATH.")
    images = sorted(f.resolve() for f in Path(a.images).iterdir() if f.suffix.lower() in EXTENSIONS)
    if not images:
        sys.exit(f"Aucune image ({', '.join(sorted(EXTENSIONS))}) dans {a.images}")
    dossier = Path(a.sortie).resolve()
    dossier.mkdir(parents=True, exist_ok=True)

    mp3 = dossier / "voix.mp3"
    srt = None if a.sans_sous_titres else dossier / "sous-titres.srt"
    if a.voix_fichier:
        shutil.copy(a.voix_fichier, mp3)
        if srt:
            if not a.srt:
                sys.exit("--voix-fichier demande aussi --srt (ou --sans-sous-titres).")
            shutil.copy(a.srt, srt)
    else:
        if not a.texte:
            sys.exit("Indiquez --texte (ou --voix-fichier).")
        texte = Path(a.texte).read_text(encoding="utf-8").strip()
        mots = asyncio.run(generer_voix(texte, a.voix, a.debit, mp3))
        if srt:
            if not mots:
                sys.exit("edge-tts n'a renvoyé aucune position de mot : sous-titres impossibles.")
            ecrire_srt(remettre_ponctuation(mots, texte), srt, a.mots_par_ligne)

    largeur, hauteur = FORMATS[a.format]
    video, duree = monter(images, mp3, srt, dossier, largeur, hauteur, a.fps, a.police)
    print(f"OK : {video} ({duree:.1f} s, {len(images)} images, {largeur}x{hauteur})")


if __name__ == "__main__":
    main()
