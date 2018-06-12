docker build -t ibex_image .
docker stop ibex 
docker rm ibex
export FLASK_ENV=development
docker run --name ibex -d -p 5000:5000 -it ibex_image
docker logs -f ibex