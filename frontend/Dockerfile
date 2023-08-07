FROM node:18

# Create app directory
WORKDIR /frontend

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
#COPY package.json package.json
#COPY package-lock.json package-lock.json
COPY . . 
RUN npm i


# Bundle app source
#COPY . .
RUN npm run build
ENV NODE_ENV=production
EXPOSE 3000
CMD [ "node", "build" ]
