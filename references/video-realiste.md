# Vidéos IA réalistes : outils, méthode, règles

Veille du 31/10/2026. « Officiel » = vu sur la page de l'éditeur. Le reste vient de blogs : à revérifier dans le compte
avant de compter dessus. Les prix et quotas changent vite.

## Outils
| Outil | Gratuit / prix | Clip | Points forts | Usage commercial |
|---|---|---|---|---|
| **Veo 3.1 (Google Flow)** | Officiel : 50 crédits/jour sans abonnement, non cumulables. Lite = 10, Fast = 20, Quality = 100 crédits (environ 5 clips Lite/jour). Génération parfois bloquée pour les gratuits entre 14 h et 17 h UTC | Officiel : 4, 6 ou 8 s, 720p/1080p, 16:9 ou 9:16 | Son natif (dialogues, bruitages), images de référence, première et dernière image imposées | Non vérifié. Filigrane invisible SynthID toujours présent |
| **Kling 3.0 / 4.0** | Crédits quotidiens gratuits annoncés par des blogs, non vérifié. Standard environ 8,80 $/mois (blogs) | Jusqu'à 30 s et 4K annoncés pour la 4.0 (non officiel) | Souvent cité comme le meilleur sur les visages et mouvements humains | Gratuit : filigrane, pas d'usage commercial (blogs). Standard : oui |
| **Seedance 2.x (Dreamina / CapCut)** | Environ 120 crédits/jour (blog Dreamina, août 2026, « à confirmer dans le compte ») | Jusqu'à 30 s avec son (ByteDance) | Très photoréaliste selon certains tests | Selon le plan. Export sans filigrane non garanti en gratuit |
| **Hailuo / MiniMax** | Non vérifié (sources contradictoires) | Environ 6 s en 720p en gratuit (blogs) | Rapide | Gratuit : filigrane, pas d'usage commercial (blogs) |
| **Runway** | Officiel : 125 crédits une seule fois. Standard 15 $/mois | — | Accès à Gen-4.5, Kling, Seedance en payant | Non indiqué |
| **Pika** | Officiel : pas de crédits gratuits mensuels. Starter 10 $/mois | — | — | Officiel : à partir de Starter |
| **Wan 2.2** (open source, Apache 2.0) | Gratuit | Environ 5 s en 720p | Libre | Oui. Mais 24 Go de VRAM officiellement : Colab gratuit seulement avec des versions communautaires allégées |
| **Sora** | Fermé (API arrêtée le 24/09/2026, doc OpenAI) | — | — | — |

## Méthode pour un rendu réaliste
1. **Partir d'une image, pas d'un texte.** Fixer d'abord le personnage en images fixes (face, profil, trois quarts : 3 à 5
   références, par exemple avec Fooocus), puis les animer. Google indique que Veo 3.1 suit mieux le prompt à partir d'une image.
2. **Formule du prompt (guide Google)** : cadrage et mouvement de caméra + sujet + action + décor + style et ambiance.
   Nommer la lumière, l'objectif, la profondeur de champ. Décrire ce qu'on veut voir, pas ce qu'on ne veut pas.
3. **Son dans le prompt** (Veo) : dialogue entre guillemets, `SFX:` pour les bruitages, `Ambient noise:` pour l'ambiance.
4. **Même personnage d'un plan à l'autre** : images de référence, première et dernière image, un repère visuel fixe
   (casquette, veste), règle des 180°, un seul personnage par scène si possible.
5. **Plans de 4 à 8 s**, 5 à 10 essais par plan, au moins 8 plans pour une minute.
6. **Montage** dans CapCut ou DaVinci Resolve : coupes rapides, sous-titres, musique de la bibliothèque.

Exemples de prompts (guide officiel Google pour Veo 3.1) :
- `Close-up with very shallow depth of field, a young woman's face, looking out a bus window at the passing city lights with her reflection faintly visible on the glass, inside a bus at night during a rainstorm, melancholic mood with cool blue tones, moody, cinematic.`
- `Crane shot starting low on a lone hiker and ascending high above, revealing they are standing on the edge of a colossal, mist-filled canyon at sunrise, epic fantasy style, awe-inspiring, soft morning light.`
- `[00:00-00:02] Medium shot from behind a young female explorer… [00:02-00:04] Reverse shot of the explorer's freckled face… SFX: The rustle of dense leaves…`
- `The camera performs a smooth 180-degree arc shot, starting with the front-facing view of the singer and circling around her to seamlessly end on the POV shot from behind her on stage.`

## Formats qui tournent (fin 2026)
- Vlogs de personnages IA récurrents (le « Bigfoot vlog » : @big_yowie, environ 151 000 abonnés TikTok, mais environ 100 $ de
  production par vidéo selon Kapwing).
- Une photo transformée en courte vidéo pour suivre une tendance du moment.
- Comptes sans visage avec une voix ou un avatar constant : accroche dans les 2 à 3 premières secondes, 15 à 60 s.
- Rémunération TikTok (Creator Rewards) : vidéos de plus de 60 s, 10 000 abonnés, 100 000 vues sur 30 jours (blogs, non vérifié).

## Règles
- **TikTok (officiel)** : étiqueter tout contenu IA réaliste. Sinon : suppression, restriction, ou étiquette ajoutée par TikTok.
  Interdit même étiqueté : tromper sur un sujet d'intérêt public, nuire à une personne, faire parler une personnalité pour un
  produit ou une cause politique.
- **YouTube (officiel)** : déclarer une vraie personne qui fait ou dit ce qu'elle n'a pas fait, une scène réaliste inventée,
  une musique IA centrale. Depuis le 16/07/2026, pas de monétisation pour le contenu générique produit en série, le contenu
  choquant ou manipulateur, et les avatars IA qui parlent santé ou finance.
- **Union européenne** : obligation de signaler les contenus truqués (AI Act, article 50), applicable à partir d'août 2026 selon
  certaines sources. Date à revérifier.
- **Pour un client** : ne livrer que des clips issus d'un plan qui donne l'usage commercial.

## Enchaînement gratuit conseillé (sans carte graphique)
1. Script et voix : `scripts/fabriquer_video.py` (ou seulement la voix et les sous-titres).
2. Images de départ avec Fooocus sur Colab, en 9:16.
3. Animation : Google Flow, Veo 3.1 Lite (environ 5 clips de 8 s par jour), à lancer avant 14 h UTC. En complément, les crédits
   gratuits de Kling ou Dreamina, à vérifier dans le compte.
4. Montage CapCut, puis étiquette « contenu IA » à la publication.

## Sources
- https://support.google.com/flow/answer/16526234
- https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- https://runway.com/pricing · https://pika.art/pricing · https://github.com/Wan-Video/Wan2.2
- https://developers.openai.com/api/docs/deprecations
- https://dreamina.capcut.com/ai-video/free-ai-video-generator-usable-clips-guide-2026
- https://www.kapwing.com/resources/what-it-takes-to-make-viral-ai-video-content-we-asked-bigfoot/
- https://www.tiktok.com/community-guidelines/en/integrity-authenticity
- https://support.google.com/youtube/answer/14328491
- https://techcrunch.com/2026/07/20/youtube-clarifies-policies-around-ai-slop-and-upsetting-videos/

## Retour d'expérience Google Flow (testé le 31/10/2026)
- Compte Google : vérification d'âge obligatoire en Europe (pièce d'identité ou selfie, à faire par le titulaire du compte).
- Flow passe maintenant par un assistant (panneau de droite) : on importe les images (« + » → Importer, puis accepter les
  « Droits d'utilisation »), puis on lui demande par écrit d'animer telle image. Il annonce le coût et attend « Approuver ».
- En gratuit, **Veo 3.1 Lite ne fait que des clips de 8 s** (10 crédits). 50 crédits par jour = 5 clips = 40 s.
  Autre choix proposé : Omni 1.1 Flash, 6 s, 5 crédits en 360p ou 10 crédits en 720p.
- Téléchargement : icône de téléchargement → « 720p (taille d'origine) ». 1080p et 4K demandent un abonnement.
  Fichier obtenu : 720×1280, environ 7,9 s, avec le son de Veo (le script le coupe et garde la voix off).
- File d'attente : 3 à 5 minutes par clip le samedi soir. 1 clip sur 5 a échoué (« échec de la génération de l'audio »),
  crédits remboursés. Demander « sans son » évite peut-être cet échec (à tester).
- 4 clips de 8 s suffisent pour une voix off de 33 s : le script donne à chaque clip une part égale de la voix.
