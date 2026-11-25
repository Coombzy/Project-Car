FROM node:22-slim
WORKDIR /app
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 NEXT_TELEMETRY_DISABLED=1
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN useradd --uid 10001 --create-home --user-group web && chown -R web:web /app
ENV HOSTNAME=0.0.0.0
USER 10001
CMD ["sh", "-c", "export HOSTNAME=0.0.0.0; exec ./node_modules/.bin/next start --hostname 0.0.0.0 --port 3000"]
