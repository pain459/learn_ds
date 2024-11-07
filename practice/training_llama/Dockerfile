# Use a suitable base image with CUDA if you have a GPU
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install essential packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    openssh-server \
    wget \
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up SSH for accessing the container
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22

# Copy the requirements file and install dependencies
COPY requirements.txt /opt/llama/requirements.txt
RUN pip3 install -r /opt/llama/requirements.txt

# Clone LLaMA repository if it does not already exist
RUN [ ! -d "/opt/llama" ] && git clone https://github.com/facebookresearch/llama.git /opt/llama || echo "LLaMA repository already exists."
WORKDIR /opt/llama

# Run SSH service
CMD ["/usr/sbin/sshd", "-D"]
