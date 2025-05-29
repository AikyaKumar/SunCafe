# Use official Node image
FROM node:20

# Set working directory
WORKDIR /app

# Copy and install deps
COPY . .
RUN npm install

# Build app
RUN npm run build

# Serve with simple static server
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]

EXPOSE 3000
