FROM python:3.11

# Set workdir
WORKDIR /app

# Signing key
RUN install -d -m 0755 /etc/apt/keyrings && \
    wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null && \
    echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null && \
    echo "Package: *\nPin: origin packages.mozilla.org\nPin-Priority: 1000" | tee /etc/apt/preferences.d/mozilla

# Install Firefox
RUN apt update && apt install firefox -y

# Copy test requirements
COPY requirements-test.txt .

# Install test requirements
RUN pip install --no-cache-dir --upgrade -r requirements-test.txt

# Copy app
COPY . .

# Install app
RUN pip install --no-cache-dir --upgrade .
