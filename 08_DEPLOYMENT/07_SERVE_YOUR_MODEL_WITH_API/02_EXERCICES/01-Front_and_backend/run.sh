docker run -it \
-v "$(pwd):/home/app" \
-p 7860:7860 \
-e PORT=7860 \
jedha/fast_api_image # BUILD FIRST THE IMAGE - docker build . -t jedha/fast_api_image OR use the remote image jedha/fast_api_demo_app

