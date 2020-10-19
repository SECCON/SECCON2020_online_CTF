FROM node:14-slim

ADD package.json /
ADD package-lock.json /
ADD solve.js /

RUN npm install

CMD [ "node", "solve.js" ]
