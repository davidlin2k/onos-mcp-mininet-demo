FROM python:3.12

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Astral UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN ln -s /usr/local/bin/uv /usr/bin/uv

WORKDIR /root
RUN git clone https://github.com/davidlin2k/onos-mcp-server.git

# Set working directory
WORKDIR /app

# Optional: Set environment variables for OpenAI
# ENV OPENAI_API_KEY="your-api-key-here"

# Copy your application files
COPY . .

ENTRYPOINT ["/root/.local/bin/uv", "run"]
CMD ["src/agents/network_summary.py"]
