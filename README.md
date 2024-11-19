# CSC340 AI Group Project

This repository contains the source code for our CSC340 AI course project, focused on developing and deploying an AI-based application. The project utilizes Ollama's Llama3 and Llama3.2 models for enhanced AI capabilities.

## Project Structure

- **client/**: Contains the frontend code for the application.
- **server/**: Contains the backend code, including API logic and model integration.
- **requirements.txt**: Lists dependencies required to run the project.

## Prerequisites

To run this project locally, you need to have **Ollama** installed with **Llama3** and **Llama3.2** models. Make sure these are correctly set up on your machine before proceeding.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/KMKyaw/LLM-Quiz-Generator
   cd LLM-Quiz-Generator
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Ollama with Llama3 and Llama3.2 is properly installed.

## Running the Project

1. **Server**: Start the server by navigating to the `server` folder and running:

   ```bash
   python app.py
   ```

2. **Client**: Navigate to the `client` folder and running:
   ```bash
   python request.py
   ```

## Usage

Once the server and client are running, you can access the application via your browser. Follow the instructions on-screen to interact with the AI models.

## Contributing

Please follow the Git workflow:

1. Fork the repository.
2. Create a new branch for each feature or bug fix.
3. Commit and push your changes to your forked repository.
4. Submit a pull request for review.

## License

This project is for educational purposes and follows the course guidelines for CSC340.

## Authors

Group Members:

- Dylan Mac Yves
- Kaung Myat Kyaw
- Cornelius Grau
- Passapol Phukhang
- Khang Hoang
- Jan Hejdušek

---

**Note**: Please ensure that all project dependencies are compatible with the installed Llama3 models on your local machine.
