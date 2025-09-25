FROM node:20.11.1 AS build

WORKDIR /app

RUN npm install -g pnpm@9.12.0

COPY frontend/package.json frontend/pnpm-lock.yaml ./

RUN pnpm install --frozen-lockfile

COPY frontend /app

RUN pnpm run build

FROM nginx:1.27-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY frontend/nginx.conf /etc/nginx/conf.d/app.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 5173