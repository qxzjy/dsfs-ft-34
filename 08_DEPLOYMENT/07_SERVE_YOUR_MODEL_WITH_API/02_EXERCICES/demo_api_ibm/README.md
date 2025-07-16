# Demo api machine learning

## Etape 0 :

- lancer docker-desktop
- serveur Neon db
- S3 -> bucket/folder ainsi que les acces key (IAM)
- un compte huggingface et aller dans les spaces

## Etape 1

- On se rend dans mlflowserverapi dans notre terminal, on crée un nouveau space sur hugging face et on clone son repo dans mlflowserverapi, on y glisse nos fichiers: dokcerfile, requirements, et eventuellement un train.py pour tester notre serveur.

  ` git add .`

  `git commit -m "oui oui baguette"`

  `git push`

- On precise nos creds et variables d'env dans les settings de notre space

  - PORT=7860
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - BACKEND_STORE_URI
  - ARTIFACT_ROOT

- On peut alors acceder à notre serveur depuis les spaces HF ou alors directement depuis un lien de la forme https://nomuser-nomspace.hf.space/ , correspondant à notre MLFLOW_TRACKING_URI. (on peut aussi récupérer ce lien depuis les 3 petits points en allant dans l'onglet "Embed this space")

## Etape 2

- Entrainer notre modele et l'envoyer sur MLflow
  On se rend dans notre terminal dans le sous dossier ML, dans le sous dossier docker, ls on vérifie que le dockerfile et le requirements sont bien là. On va créer un environnement python semblable à celui de notre image mlflow que l'on a construit pour notre serveur afin de s'assurer de la compatibilité des versions de nos différents objets. Aussi bien l'env python dans notre terminal pour lancer le run, ainsi que l'image mlflow que l'on va build sur laquelle on va faire tourner notre MLproject.
- Ainsi:
  - `docker build . -t mlflowmehdi`
  - `conda create -n mlflowenv python=3.9`
  - `conda activate mlflowenv`
  - `pip install -r requirements.txt`
- On retourne dans ML on modifie le nom de l'image dans le MLproject et on met mlflowmehdi.
- Dans le terminal aussi on revient en arriere, un petit ls pour s'assurer que MLProject, train.py et secrets.sh sont bien là.
- Ici au choix, on push nos variables d'env comme on veut (on peut) sous mac moi je fais un `source secrets.sh` faites ce qui marche chez vous en vérifiant bien que vous avez mis à jour toutes vos creds dans votre secret. Mais il faut bien le faire sinon on n'aura acces à rien et nos runs ne vont jamais arriver dans notre serveur mlflow.
- Une fois nos creds précisées et nos var env set up :
  - `mlflow run .`
- Dès que l'entrainement a fini on se rend sur MLflow pour récupérer notre "model_uri" dans les artifacts, il sera de la forme 'runs:/d84491e834d34774ba7b6d403ec8a5b8/ibm_attrition_detector'. Dans app.py on remplace 'logged_model' par cette nouvelle valeur, aussi bien dans predict que dans le batch predict.

## Etape 3

On va pouvoir maintenant déployer notre api avec notre modèle implémenter à l'intérieur.

- On se rend dans ibmapi dans notre terminal, on crée un nouveau space sur hugging face et on clone son repo dans ibmapi, on y glisse nos fichiers: dockerfile, requirements, app.py, data et eventuellement un test.py pour tester notre app.

  ` git add .`

  `git commit -m "non non croissant"`

  `git push`

- On precise nos creds et variables d'env dans les settings de notre space, en ajoutant cette fois aussi les creds du serveur mlflow ainsi que de notre experiment:

  - PORT=7860
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - BACKEND_STORE_URI
  - ARTIFACT_ROOT
  - MLFLOW_EXPERIMENT_NAME
  - MLFLOW_TRACKING_URI

- On peut finalement la requêter toujours via la même URL pour acceder à un space soit:
  - https://nomuser-nomspace.hf.space/
  - https://nomuser-nomspace.hf.space/docs
