<h1 align="center">
  ☸️ kompose-example
</h1>

An example of a small, multi-container web application developed with Docker
Compose and moved to Kubernetes with `kompose`. Built as a weekend hack to
experiment with quick-and-dirty development patterns for
[Kompose](https://kompose.io/) and [k3d](https://k3d.io/).

> 🤔 __Why?__ Because as a data scientist, I build a lot of machine learning
products but don't always get to be hands-on with the "real" Kubernetes
clusters. I want to understand as much of my team's stack as possible, and
Kompose seems like a good way to bridge that gap between something I'm already
comfortable with (Docker Compose) and something I want to do more often (hand
off Kube YAML to \*Ops).

## Overview

The core service is a simple Hello World application built with Python using
[Streamlit](https://streamlit.io/) and [FastAPI](https://fastapi.tiangolo.com/).
The development pattern emulated here is something similar to:

- Build a Python application and containerize components
- Serve an initial version locally with Docker Compose
- Prove basic Kubernetes viability with deployment to k3d cluster

## Usage

Create and activate a Python virtual environment, for example:

```bash
conda create -n kompose-example python=3.9
conda activate kompose-example
make install
```

Optionally build and serve the application with Docker Compose using:

```bash
# Build and run
docker-compose up --build

# Access the UI at localhost:80

# Shutdown the service
docker-compose down
```

Setup a lightweight Kubernetes cluster on your development machine.
Instructions here are for the in-Docker variant of [k3s](https://k3s.io/), k3d,
installed with `brew install k3d`. Create a cluster and optional local image
registry with:

```bash
k3d cluster create dev --port 8080:80@loadbalancer --port 8443:443@loadbalancer
```

Make sure to update the `REGISTRY` environment variable in `.env` depending on
whether you opt for a local registry or a remote one like Docker Hub. You may
also need to update `services.<service>.image` attributes in
`docker-compose.yaml` as well if you use another registry.

Note that you can use `k3d cluster [delete | start | stop] dev` once the k3d
setup is complete.

Finally, create a namespace for the project and create the deployment:

```bash
kubectl create namespace kompose-example
```

The easiest way to access the UI in your browser on-the-fly (i.e., without
spending a bunch of time on Ingress or NodePort is:

```bash
kubectl port-forward service/frontend 12345:80 -n kompose-example
```

Then access the page at <localhost:12345>.

## Makefile Reference

```
Usage:
  make [command]

Available Commands:
  install  Install Python dependencies for local dev
  clean    Delete the Kube YAML created by Kompose
  build    Build and push the Docker images
  quality  Check Python code quality
  style    Auto-format Python code
```

## Notes

During development, I learned that `kompose convert` doesn't (fully) support
variable substitution from `.env` at runtime. This led me to the solution I have
today, which is to use `dotenv` to handle the substitution. I don't
particularly like this extra dependency, so will continue to play around with
alternatives. Here are some interesting failed attempts:

```bash
kompose convert -f "<(docker-compose config)"
```

I was very proud of myself for thinking of this one, until I realized the
process substitution caused all kinds of problems:

- Kompose seems to want a YAML/JSON file extension, which requires refactoring
  as `TMPSUFFIX=.yaml; ... "=(docker-compose config)"`, which is Zsh-specific.
- Kompose wants a seekable file, not a file descriptor.

So I gave up a little bit of perceived elegance for:

```bash
docker-compose config > .docker-compose.yaml
kompose convert -f .docker-compose.yaml
```

This seemed surefire at first, but I quickly discovered that `docker-compose
config` _also_ resolves relative paths (e.g., `context: "."` becomes `context:
"/Users/ben/kompose-example"`), which in turn causes Kompose to fail.
