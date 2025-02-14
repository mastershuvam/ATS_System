# ATS Resume Analyzer

## Project Overview
The **ATS Resume Analyzer** is a Streamlit-based web application that helps users analyze resumes against job descriptions. It leverages Google's Generative AI API for advanced analysis and MongoDB for storing user data and analysis history. The app provides features like resume evaluation, improvement tips, and match percentage calculation, aiming to assist users in creating stronger resumes for job applications.

---

## Live Demo

You can try out the live application here:
[ats-system-1-2ikc.onrender.com](https://ats-system-1-2ikc.onrender.com)


## Features
1. **User Authentication**:
   - Secure login and registration using MongoDB and bcrypt for password hashing.
2. **Resume Analysis**:
   - Upload a PDF resume and analyze it against job descriptions.
3. **Generative AI Integration**:
   - Use Google Generative AI (Gemini) for evaluating resumes and providing actionable feedback.
4. **Match Percentage**:
   - Calculate the percentage match between a resume and a job description.
5. **Improvement Tips**:
   - Suggest skills or certifications to improve alignment with the desired role.
6. **Dashboard**:
   - User-friendly interface with a chatbot assistant for queries and support.

---

## Technologies Used

### Backend:
- **MongoDB**: For storing user data and analysis logs.
- **Google Generative AI**: For analyzing resumes and job descriptions.
- **Python**: Core programming language.

### Frontend:
- **Streamlit**: For building the web interface.

### Libraries:
- `python-dotenv`: To manage environment variables.
- `bcrypt`: For secure password hashing.
- `Pillow`: For image processing.
- `pdf2image`: To extract images from PDF files.

---

## Prerequisites
1. **Python 3.8+**
2. **MongoDB instance** (local or cloud-based like MongoDB Atlas).
3. **Google API Key** for Generative AI (Gemini).
4. **Streamlit** installed globally or in a virtual environment.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ats-resume-analyzer.git
   cd ats-resume-analyzer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the `.env` file with the following variables:
   ```env
   MONGODB_URI=your_mongo_connection_string
   GOOGLE_API_KEY=your_google_api_key
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## File Structure
```
project-root/
|-- app.py                # Main application file
|-- login.py              # User authentication module
|-- requirements.txt      # Dependencies
|-- .env                  # Environment variables
|-- README.md             # Project documentation
|-- helpers/              # Helper functions (e.g., PDF processing)
|-- static/               # CSS or images for custom styling
|-- templates/            # Any reusable components or templates
```

---

## Usage
1. Launch the application.
2. Register or log in.
3. Paste a job description in the provided text area.
4. Upload your resume in PDF format.
5. Select the desired analysis option (e.g., Evaluation, Improvement Tips, Match Percentage).
6. View and save the analysis results.

---

## Known Issues and Limitations
- The resume must be in PDF format.
- Requires a stable internet connection for Generative AI API calls.
- AI-generated results are for guidance and may require manual validation.

---

## Future Enhancements
- Add a feature to recommend companies based on the candidate’s profile.
- Improve the chatbot assistant to provide contextual help.
- Expand analysis options (e.g., skill gap analysis, industry-specific recommendations).
- Add Docker support for easier deployment.

---

## Contributors
- **Shuvam Ghosh** - Project Lead and Developer ([GitHub](https://github.com/avikalp987))

---

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

---

## Contact
For questions or suggestions, reach out to:
- Email: your-email@example.com
- GitHub Issues: [Create an Issue](https://github.com/your-username/ats-resume-analyzer/issues)

---

Happy coding! 🚀

