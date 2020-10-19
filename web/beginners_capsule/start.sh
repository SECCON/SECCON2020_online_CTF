docker build file -t capsule
cd dist && npm install && cd -
npm install -g pm2
pm2 start ecosystem.config.js
