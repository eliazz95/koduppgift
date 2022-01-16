Simple script to get a prediction from an image

# How to deploy using Docker
This is the preferred and intended way.
1. Build image using `docker build -t koduppgift .`
2. Run the image with an exposed ip using `docker run -d -p <YOUR_HOST_IP>:5000:5000 koduppgift`
3. To send images use `curl -D POST -F file=@'<FILENAME_FOR_IMAGE>' http://<YOUR_HOST_IP>:5000/predict`