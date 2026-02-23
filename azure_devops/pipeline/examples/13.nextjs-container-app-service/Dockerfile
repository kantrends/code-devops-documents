ARG NODE_VERSION=20
FROM premiercommonacr.azurecr.io/node:${NODE_VERSION} as base

ARG PNPM_VERSION=9.6.0

# switching to root to install pnpm globally
USER root
RUN npm install -g pnpm@${PNPM_VERSION}

# switching to default "core" user
USER core

WORKDIR /ui

COPY --chown=core:core . .

RUN pnpm config set registry https://nexus.premierinc.com/artifacts/repository/npm ; \
		pnpm i --frozen-lockfile ; \
		pnpm run build

EXPOSE 3000

CMD ["pnpm", "run", "start"]
