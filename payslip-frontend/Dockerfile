FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json* bun.lockb* ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]