FROM node:alpine

WORKDIR /app

COPY sent_app/package.json /app/package.json
COPY sent_app/package-lock.json /app/package-lock.json

RUN npm i

COPY ./sent_app/src /app/src
COPY ./sent_app/public /app/public

EXPOSE 3000

CMD ["npm", "start"]
