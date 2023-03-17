FROM node:19
# Copy the frontend code into the container
WORKDIR /app
COPY ./frontend .
# Install pnpm and the frontend dependencies
RUN npm install -g pnpm
RUN pnpm install

# Build the frontend
RUN pnpm build

CMD [ "node", ".output/server/index.mjs" ]
