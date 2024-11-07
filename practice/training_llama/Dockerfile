# Use a suitable base image with CUDA if you have a GPU
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install essential packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    openssh-server \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set up SSH for accessing the container
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22

# Clone LLaMA and install dependencies
RUN git clone https://github.com/facebookresearch/llama.git /opt/llama
WORKDIR /opt/llama
RUN pip3 install -r requirements.txt

# Install additional libraries for handling PDFs
RUN pip3 install PyMuPDF transformers sentence-transformers

# Run SSH service
CMD ["/usr/sbin/sshd", "-D"]
