# Set the base image
FROM ubuntu:jammy

# Install Python and Streamlit
RUN apt-get update && \
    apt-get install python3 -y && \
    apt-get install -y python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install streamlit


# Install Java 8    
RUN apt-get update && \
    apt-get install openjdk-8-jdk-headless -y

# Install Spark
ENV SPARK_VERSION=3.2.3
RUN apt-get install -y wget && \
    wget -q https://archive.apache.org/dist/spark/spark-3.2.3/spark-3.2.3-bin-hadoop3.2.tgz && \
    tar -xzf spark-3.2.3-bin-hadoop3.2.tgz && \
    mv spark-3.2.3-bin-hadoop3.2 /usr/local/spark && \
    rm spark-3.2.3-bin-hadoop3.2.tgz && \
    ln -s /usr/local/spark/bin/spark-submit /usr/bin/spark-submit

ENV SPARK_HOME=/usr/local/spark
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Install MongoDB client
RUN touch /etc/apt/sources.list.d/mongodb-org-6.0.list
RUN apt-get install -y gnupg 
RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list 
RUN apt-get update && \
    apt-get install -y mongodb-org-shell

# Set environment variables
ENV MONGO_URI=mongodb://localhost:27017
ENV MONGO_DB=MONGO_URI["knoxquack"]

# Copy the app files
WORKDIR /app
COPY . .

ENV PIPENV_VENV_IN_PROJECT=1

# Install app dependencies
RUN pip3 install pipenv
RUN pip3 install -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "app.py"]
