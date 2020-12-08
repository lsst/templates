# This Dockerfile has four stages:
#
# base-image
#   Updates the base Python image with security patches and common system
#   packages. This image becomes the base of all other images.
# dependencies-image
#   Installs third-party dependencies (requirements/main.txt) into a virtual
#   environment. This virtual environment is ideal for copying across build
#   stages.
# install-image
#   Installs the app into the virtual environment.
# runtime-image
#   - Copies the virtual environment into place.
#   - Runs a non-root user.
#   - Sets up the entrypoint and port.

FROM python:3.9-slim-buster AS base-image

# Update system packages
COPY scripts/install-base-packages.sh .
RUN ./install-base-packages.sh && rm ./install-base-packages.sh

FROM base-image AS dependencies-image

# Install system packages only needed for building dependencies.
COPY scripts/install-dependency-packages.sh .
RUN ./install-dependency-packages.sh

# Create a Python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
# Make sure we use the virtualenv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Put the latest pip and setuptools in the virtualenv
RUN pip install --upgrade --no-cache-dir pip setuptools wheel

# Install the app's Python runtime dependencies
COPY requirements/main.txt ./requirements.txt
RUN pip install --quiet --no-cache-dir -r requirements.txt

FROM base-image AS install-image

# Use the virtualenv
COPY --from=dependencies-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir .

FROM base-image AS runtime-image

# Create a non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser

# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=install-image /opt/venv /opt/venv

# Switch to non-root user
USER appuser

EXPOSE 8080

ENTRYPOINT ["{{ cookiecutter.package_name }}", "run", "--port", "8080"]
