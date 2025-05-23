FROM node:22-alpine

ARG VITE_DEFAULT_AVATAR
ARG VITE_DEFAULT_BACKGROUND

ENV VITE_DEFAULT_AVATAR=$VITE_DEFAULT_AVATAR
ENV VITE_DEFAULT_BACKGROUND=$VITE_DEFAULT_BACKGROUND

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE 5050
# CMD ["npm", "run", "dev"]
CMD ["npm", "run", "preview", "--", "--port", "5050", "--host", "0.0.0.0"]