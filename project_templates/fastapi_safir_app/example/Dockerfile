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

FROM tiangolo/uvicorn-gunicorn:python3.8-slim as base-image

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

FROM dependencies-image AS install-image

# Use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir .

FROM base-image AS runtime-image

# Copy the virtualenv
COPY --from=install-image /opt/venv /opt/venv

# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# We use a module name other than app, so tell the base image that.  This
# does not copy the app into /app as is recommended by the base Docker
# image documentation and instead relies on the module search path as
# modified by the virtualenv.
ENV MODULE_NAME=example.main

# The default starts 40 workers, which exhausts the available connections
# on a micro Cloud SQL PostgreSQL server and seems excessive since we can
# scale with Kubernetes.  Most of our applications are tiny so cap the
# workers at 2.
ENV MAX_WORKERS=2

# Run on port 8080 instead of the FastAPI default to avoid requiring
# capabilities.
ENV PORT=8080
