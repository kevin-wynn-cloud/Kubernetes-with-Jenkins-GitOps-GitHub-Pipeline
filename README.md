# Deployment with Jenkins GitOps GitHub Pipeline on Kubernetes

## Introduction:
With lab guidance provided by user saha-rajdeep (Solutions Architect at AWS), I deploy to Kubernetes with Jenkins GitOps GitHub Pipeline. 

## GitOps Flow:
I have app.py and push the code to a GitHub repository named KubernetesCode. As soon as I push the code, a Jenkins job is triggered and builds the Docker container image. The Jenkins job's name is buildimage. Jenkins serves the image in a container registry (Docker Hub in this case), and the name of the container image is test:latest, which is the tag for the container image. Every time the code is changed, a new Docker image will be created with the updated tag. Raj provides an architecture image:

![1](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/49e7c958-fe84-4f8c-93b5-dc116c0e391d)

## GitHub Repositories:
In the GitHub, there is another repo for the Kubernetes manifest files named kubernetesmanifest, which houses the deployment.yaml file in the registry. The deployment.yaml file references the newly created container image. It does this because Jenkins, after creating the Docker container image, triggers a second Jenkins job that updates the manifest (updates the image in deployment.yaml).

## GitOps Portion:
In the GitOps portion of the lab, we are using ArgoCD (but this approach would work with Flux as well). GitOps continuously monitors the Kubernetesmanifest repo, and if the state in the Kubernetes cluster deviates from the manifest file in the repo, GitOps will grab the changes from the GitHub repo and deploy it to the Kubernetes cluster. There is no container running in the Kubernetes cluster, and GitOps sees that, so it is going to deploy the deployment.yaml file to the cluster. 

## What if the application code app.py gets changed again?
In this case, the job BuildImage would build a new container image and save the container with a new tag test:11. This Jenkins job would trigger the updatemanifest Jenkins job, which will update the image reference in the deployment.yaml file. Next, ArgoCD (GitOps) will detect that the Kubernetes cluster is running with the tag 10 while the deployment.yaml file is referencing tag 11. So ArgoCD will stop the container with the older tag and create a container with the newest tag.

## Jenkins Job Roles:
The Jenkins job that is building the Docker image and updating the manifest file is the CI (Developer), while the GitOps that is deploying the deployment.yaml file into the cluster is the CD (Ops).

## Code Section:
Included in the lab are app.py, a simple Python program; requirements.txt, listing external library Flask; Dockerfile, which dockerizes the Python program; and Jenkinsfile, the job that creates the Docker container image.

## SSH Key Pair:
I created a key pair (.ppk because I'll be using PuTTY) named RajKubernetesLab.

## EC2 Instance Setup:
I created a security group named RajKubernetesLabSG and allowed inbound SSH from my IP address with a /32 subnet. I also allowed HTTP traffic from port 8080.

![3](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/1acdb4de-d09d-43ab-afaa-a81a3c4ca19b)

![4](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/73be99db-d44d-451d-b80d-2b4efa3d1361)

## Jenkins Installation:
After Jenkins was installed, I connected to my server using my instance's public DNS (http://<your_server_public_DNS>:8080). I used the sudo cat /var/lib/jenkins/secrets/initialAdminPassword command to find the password on my EC2 instance. I then installed the initial suggested plugins.

## Jenkins Plugins:
I managed my plugins and installed the Amazon EC2 plugin.

![7](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/55d14965-ec02-4cd4-8880-d27aaf0a8ffd)

## Docker Installation:
Next, I installed Docker on my EC2 using the below commands:

```bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo chmod 666 /var/run/docker.sock
```

![8](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/f4eb7e8e-fa3c-4418-836a-f318ff260b85)

## Git Installation:
I also installed Git on my EC2 with:

```bash
sudo yum install git
```

## Credentials Setup:
I created additional credentials for Jenkins for my Docker and GitHub, ensuring the username matched my GitHub username and the ID dockerhub referenced in my Jenkins file. The password for the GitHub credential was a generated GitHub token, not the GitHub account password. Additionally, I used PuTTYgen to change the PPK format to the OpenSSH format and included it in its entirety (including the "-----BEGIN RSA PRIVATE KEY-----" and "-----END RSA PRIVATE KEY-----") manually in the text for Jenkins. 

![9](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/8cc22ce4-724f-493a-a7a6-2569697eb0ba)

## Build Image Job:
With Jenkins up and running, I started working on the Build Image Job. I created a new item in Jenkins with the name buildimage and selected pipeline. I then selected "Pipeline script from SCM" to grab the script from my GitHub.

![10](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/4b6f5909-f4fb-4801-ba30-32a8583fe9de)

## Update Manifest Job:
Next, I set up the updatemanifest Jenkins job in the same manner. I created a new item in Jenkins named updatemanifest, matching the name used in the Jenkins file, and also made it a pipeline job. I selected the project as being parameterized, and added a string parameter, naming it DOCKERTAG. Likewise, I selected "Pipeline script from SCM" and Git to pull the script from my GitHub, but with this one coming from the Kubernetes-Manifest repo.

## Job Execution:
Next, I tried to run what I've created by navigating to the build image job and selecting "Build Now." I did not add all the required plugins to Jenkins, such as the Docker, Docker Pipeline, GitHub Integration, and Parameterized trigger plugins. Once I did that and slightly modified the code in the files to point toward my own DockerHub and Git repos, the build was successful. The container image is now in my Docker Hub.

![12](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/4ab3047e-4e8c-47f4-9370-0e3104553fef)

![13](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/33feadfe-cf70-43b3-bfbd-2eaec33a2892)

## Deploy Kubernetes cluster using AWS EKS

I utilized the AWS CLI along with the `eksctl create cluster` command (requiring the eksctl CLI tool) to establish my Kubernetes cluster. This cluster serves as the foundation for deploying the application and interacting with ArgoCD.

![15](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/dd808df9-aa30-4262-af3d-0e19710b176a)

## ArgoCD Setup:
Next, I set up ArgoCD. I created a Kubernetes Cluster in AWS EKS and a Cluster service role to allow the Kubernetes control plane to manage AWS resources on my behalf. I installed Argo CD using the following commands:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

I also installed the Argo CD CLI and used port forwarding to connect to the API server without exposing the service:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

I then accessed Argo CD through https://localhost:8080/ on my browser. 

![16](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/fcf15fc1-c116-4784-b3a4-121c08f80b1a)

The initial password for the admin account is auto-generated and stored as clear text in the field password in a secret named argocd-initial-admin-secret in your Argo CD installation namespace. I retrieved the one-time password using the argocd CLI:

```bash
argocd admin initial-password -n argocd
Argo CD Application Setup:
Now we set up the Argo CD part. So, I went to the Argo CD console and pointed the GitOps Argo CD to the Kubernetes manifest repo and deployed the app by clicking the new app button. I named the app flaskdemo to match the deployment.yaml document, project default, and a sync policy automatic (it checks the cluster and GitHub repository every 3 minutes to ensure they are in sync). I pointed the ArgoCD repo URL to my kubernetesmanifest repo.
```

I then created the application. The guide was outdated, so I ran the logs for a pod to help identify the problem, which seems to be an incompatibility with Flask and Werkzeug libraries.

```bash
kubectl logs flaskdemo-58f9d5c7cc-9xvvp -c flaskdemo
```

![19](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/c57ea80e-4087-467b-afbe-2684406e53f8)

So I modified the Dockerfile to explicitly download compatible versions of Flask and Werkzeug:

```bash
Flask==2.2.2
Werkzeug==2.2.2
```

I ran the Jenkins buildimage to rebuild the image and tried again, getting it to work.

![20](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/ba23148e-703d-4e50-9c4e-05762bbb226f)

![22](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/be9e5ac2-6dc8-4568-ba95-43aa33bc42a0)

## Webhook Setup:
Lastly, I needed to automatically trigger the Jenkins job whenever I push Python code to the repo. To set up the push webhook from the code repository, I went to the Jenkins dashboard and copied the URL. Then I went to the Kubernetes code repo, clicked settings, and added webhook. The payload URL was: `http://ec2-52-207-219-99.compute-1.amazonaws.com:8080/`

![23](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/17cf81ea-f6e7-4cc1-948f-fb8435bc2566)

Next, I navigated to Jenkins, my buildimage job, and then in the configuration setting, and selected GitHub hook trigger for GITScm polling before saving.

![24](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/b2df6b11-0f03-41d2-a09d-95445e812148)

Now it is officially zero-touch. When I change my Python code, the job is triggered, building the image, pushing the image, triggering the updatemanifest job. Now, my DockerHub, deployment file tag, and my ArgoCD (which terminates old pods and creates new pods) all update on their own, as well as my application code. We have completed an end-to-end deployment into Kubernetes cluster using Jenkins DevOps and GitOps.

![25](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/c8789e41-8090-40da-bc09-991d6ec71d5a)

![26](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/3353581c-18be-4c24-8ce9-8f01dcaf8d7d)

![27](https://github.com/kevin-wynn-cloud/Kubernetes-with-Jenkins-GitOps-GitHub-Pipeline/assets/144941082/fb5750f2-a350-46f5-a1ef-c4de98d468ea)


