# Use an official Node.js image for development
FROM node:21-alpine as development

# Install dependencies
WORKDIR /app
COPY package*.json ./
COPY webpack.config.js ./
RUN npm install 

# Copy source code
COPY . .

EXPOSE 3000

# Start development server
CMD ["npm", "start"]