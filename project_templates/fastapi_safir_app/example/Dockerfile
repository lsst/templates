# This Dockerfile has three stages:
#
# base-image
#   Updates the base Python image with security patches and common system
#   packages. This image becomes the base of all other images.
# install-image
#   Installs third-party dependencies (requirements/main.txt) and the
#   application into a virtual environment. This virtual environment is ideal
#   for copying across build stages.
# runtime-image
#   - Copies the virtual environment into place.
#   - Runs a non-root user.
#   - Sets up the entrypoint and port.

FROM python:3.12.5-slim-bookworm AS base-image

# Update system packages.
COPY scripts/install-base-packages.sh .
RUN ./install-base-packages.sh && rm ./install-base-packages.sh

FROM base-image AS install-image

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv

# Install system packages only needed for building dependencies.
COPY scripts/install-dependency-packages.sh .
RUN ./install-dependency-packages.sh

# Create a Python virtual environment.
ENV VIRTUAL_ENV=/opt/venv
RUN uv venv $VIRTUAL_ENV

# Make sure we use the virtualenv.
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install the app's Python runtime dependencies.
COPY requirements/main.txt ./requirements.txt
RUN uv pip install --compile-bytecode --verify-hashes --no-cache \
    -r requirements.txt

# Install the application itself.
COPY . /workdir
WORKDIR /workdir
RUN uv pip install --compile-bytecode --no-cache .

FROM base-image AS runtime-image

# Create a non-root user.
RUN useradd --create-home appuser

# Copy the virtualenv.
COPY --from=install-image /opt/venv /opt/venv

# Make sure we use the virtualenv.
ENV PATH="/opt/venv/bin:$PATH"

# Switch to the non-root user.
USER appuser

# Expose the port.
EXPOSE 8080

# Run the application.
CMD ["uvicorn", "example.main:app", "--host", "0.0.0.0", "--port", "8080"]
