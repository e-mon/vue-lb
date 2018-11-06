FROM node:10.11.0-alpine AS build

RUN npm install -g http-server


WORKDIR /app

COPY ./package.json ./yarn.lock ./
RUN yarn install
COPY . .
RUN yarn build

FROM nginx:1.13.12-alpine as prod
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


