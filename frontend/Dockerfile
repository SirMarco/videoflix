FROM node:20.12.2 AS build

WORKDIR /usr/src/app

COPY . .

RUN npm install

RUN npm run build

FROM nginx:alpine

COPY --from=build /usr/src/app/dist/frontend_videoflix/browser /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]