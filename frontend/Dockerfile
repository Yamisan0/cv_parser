FROM node:22

# Set the working directory
WORKDIR /frontend

# Copy package.json and package-lock.json and install dependencies
COPY package.json yarn.lock ./
RUN corepack enable && yarn install

# Copy the rest of the application
COPY . .

# Expose port 3000 and start the application
EXPOSE 3000
CMD ["sh", "entrypoint.sh"]