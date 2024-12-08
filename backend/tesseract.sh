apt update

apt install poppler-utils -y

# Add necessary repositories (for Ubuntu)
add-apt-repository universe

# Update package lists again after adding repositories
apt update

# Install tesseract-ocr
apt install tesseract-ocr -y