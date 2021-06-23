from setuptools import setup


with open("README.md", "r", encoding="utf-8") as file:
    LONG_DESCRIPTION = file.read()


extras = {"quality": ["black", "flake8", "isort"]}

setup(
    name="kompose-example",
    version="1.0.0.dev0",
    author="Ben Cunningham",
    author_email="benjamescunningham@gmail.com",
    description="Moving from Docker Compose to Kubernetes",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/benjcunningham/kompose-example",
    extras_require=extras,
    python_requires=">=3.9.0",
)
