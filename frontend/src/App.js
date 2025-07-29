// frontend/src/App.jsx
import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // For basic styling
import reportWebVitals from './reportWebVitals';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setResumeFile(event.target.files[0]);
  };

  const handleJdChange = (event) => {
    setJobDescription(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setAnalysisResult(null);

    if (!resumeFile || !jobDescription) {
      setError("Please upload both a resume and provide a job description.");
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDescription);

    try {
      const response = await axios.post('/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setAnalysisResult(response.data);
    } catch (err) {
      console.error("Error during analysis:", err);
      setError(err.response?.data?.error || "An unexpected error occurred during analysis. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>ResumeMatch AI</h1>
        <p>Analyze your resume against a job description</p>
      </header>

      <main className="App-main">
        <form onSubmit={handleSubmit} className="analysis-form">
          <div className="form-group">
            <label htmlFor="resume-upload">Upload Resume (PDF/DOCX):</label>
            <input
              type="file"
              id="resume-upload"
              accept=".pdf,.docx"
              onChange={handleFileChange}
              required
            />
            {resumeFile && <p className="file-name">Selected: {resumeFile.name}</p>}
          </div>

          <div className="form-group">
            <label htmlFor="job-description">Job Description:</label>
            <textarea
              id="job-description"
              rows="10"
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={handleJdChange}
              required
            ></textarea>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze My Resume'}
          </button>
        </form>

        {error && <div className="error-message">{error}</div>}

        {analysisResult && (
          <div className="results-container">
            <h2>Analysis Results</h2>
            <p className="match-score">
              Overall Match Score: <strong>{analysisResult.match_score}%</strong>
            </p>

            <h3>Feedback:</h3>
            <p>{analysisResult.feedback}</p>

            {analysisResult.missing_skills && analysisResult.missing_skills.length > 0 && (
              <>
                <h3>Missing Skills:</h3>
                <ul className="skill-list">
                  {analysisResult.missing_skills.map((skill, index) => (
                    <li key={index}>{skill}</li>
                  ))}
                </ul>
              </>
            )}

            {analysisResult.strongest_matches && analysisResult.strongest_matches.length > 0 && (
              <>
                <h3>Strongest Matches (Skills):</h3>
                <ul className="skill-list">
                  {analysisResult.strongest_matches.map((skill, index) => (
                    <li key={index}>{skill}</li>
                  ))}
                </ul>
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
  reportWebVitals();
}

export default App;