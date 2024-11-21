aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.us-west-2.amazonaws.com

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 303673948954.dkr.ecr.us-west-2.amazonaws.com


docker build --platform=linux/amd64 -t background-removal-inference-image .                                      

aws ecr create-repository --repository-name background-removal-inference-image --region us-west-2

#get account ID
aws sts get-caller-identity \
    --query Account \
    --output text

docker tag background-removal-inference-image:latest 303673948954.dkr.ecr.us-west-2.amazonaws.com/background-removal-inference-image:latest

docker push 303673948954.dkr.ecr.us-west-2.amazonaws.com/background-removal-inference-image:latest

