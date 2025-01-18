# ----------------------------------- #

FROM node:20.0.0-bullseye AS build-stage

WORKDIR /app
COPY "frontend/package*.json" /app/
RUN npm install
COPY ./frontend /app/
RUN npm run build

# -------------------------- #

FROM nginx:1.25.0-alpine

COPY --from=build-stage /app/build/ /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY frontend/nginx.conf /etc/nginx/conf.d
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]