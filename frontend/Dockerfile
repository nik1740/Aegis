FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* bun.lockb* ./
# We can use npm install even if bun.lockb is present
RUN npm install

COPY . .

EXPOSE 8080

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
