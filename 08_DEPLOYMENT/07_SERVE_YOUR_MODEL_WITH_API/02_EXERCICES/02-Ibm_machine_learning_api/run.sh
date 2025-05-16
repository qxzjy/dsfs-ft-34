docker run -it \
-v "$(pwd):/home/app" \
-p 7860:7860 \
-e PORT=7860 \
-e MLFLOW_TRACKING_URI="THIS_IS_SECRET" \
-e AWS_ACCESS_KEY_ID="THIS_IS_SECRET" \
-e AWS_SECRET_ACCESS_KEY="THIS_IS_SECRET" \
-e ARTIFACT_ROOT="THIS_IS_SECRET" \
jedha/ibm_attrition_api # Don't forget to build the image first