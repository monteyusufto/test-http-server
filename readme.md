# Test HTTP Server

A simple Flask-based HTTP server for uploading and downloading files, containerized using Docker. This server allows users to upload files through a web interface and access/download them via specified URLs.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Clone the Repository](#clone-the-repository)
- [Running the Server using Provided Scripts](#running-the-server-using-provided-scripts)
  - [On Windows](#on-windows)
  - [On Linux](#on-linux)
- [Notes](#notes)
- [License](#license)

## Features

- **File Upload:** Upload files through a simple and intuitive web interface.
- **File Download:** Access and download uploaded files via direct URLs.
- **Dockerized:** Easy deployment using Docker containers.
- **Portability:** The server can run on any system that supports Docker.
- **Automated Setup:** Includes batch and bash scripts for building and running the Docker container effortlessly.

## Prerequisites

- **Docker:** Make sure you have Docker installed on your system. You can download it from [here](https://www.docker.com/get-started).
- **Git:** (Optional) For cloning the repository. Download from [here](https://git-scm.com/downloads).
- **Windows or Linux OS:** The provided scripts are designed for both Windows Command Prompt and Linux Shell.

## Getting Started

## Running the Server using Provided Scripts

### On Windows

To run the server on a Windows machine using the provided batch script:

1. **Ensure Docker is running** on your machine.

2. **Navigate to the Project Directory:**

   Open Command Prompt and navigate to the directory where the project is located:

   ```bash
   cd path\to\test-http-server

### On Linux
1. **Ensure Docker is running** on your machine.
   Open Command Prompt and navigate to the directory where the project is located:
   ```bash
   cd path\to\test-http-server
   ./run_http_server_linux.sh


### Clone the Repository

You can clone this repository using Git:

```bash
git clone https://github.com/monteyusufto/test-http-server.git


