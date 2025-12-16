import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import LoadingSpinner from './components/LoadingSpinner';
import ResultsDisplay from './components/ResultsDisplay';
import { ocrAPI } from './services/api';
import './App.css';

function App() {
    const [isProcessing, setIsProcessing] = useState(false);
    const [results, setResults] = useState(null);
    const [jobId, setJobId] = useState(null);
    const [error, setError] = useState(null);
    const [healthStatus, setHealthStatus] = useState(null);

    // Check API health on component mount
    useEffect(() => {
        checkHealth();
    }, []);

    const checkHealth = async () => {
        try {
            const health = await ocrAPI.getHealth();
            setHealthStatus(health);
        } catch (err) {
            console.error('Health check failed:', err);
            setHealthStatus({ status: 'unhealthy', error: err.message });
        }
    };

    const handleFilesSelected = async (files) => {
        setError(null);
        setResults(null);
        setJobId(null);
        setIsProcessing(true);

        try {
            // Upload files
            const uploadResponse = await ocrAPI.uploadFiles(files);
            setJobId(uploadResponse.job_id);

            // Poll for results
            const finalResult = await ocrAPI.pollForResults(
                uploadResponse.job_id,
                (update) => {
                    // Handle status updates if needed
                    console.log('Job status:', update.status);
                }
            );

            if (finalResult.status === 'completed') {
                setResults(finalResult.results);
            } else if (finalResult.status === 'failed') {
                setError(finalResult.error_message || 'OCR processing failed');
            }

        } catch (err) {
            console.error('OCR processing error:', err);
            setError(err.message || 'An error occurred during processing');
        } finally {
            setIsProcessing(false);
        }
    };

    const handleReset = () => {
        setResults(null);
        setJobId(null);
        setError(null);
        setIsProcessing(false);
    };

    return (
        <div className="App">
            <header className="app-header">
                <div className="container">
                    <h1>OCR Document Digitizer</h1>
                    <p>Extract text from images and PDFs with high accuracy</p>

                    {healthStatus && (
                        <div className={`health-status ${healthStatus.status}`}>
                            <span className="status-indicator"></span>
                            <span>
                                API Status: {healthStatus.status}
                                {healthStatus.tesseract_version && ` • Tesseract ${healthStatus.tesseract_version}`}
                            </span>
                        </div>
                    )}
                </div>
            </header>

            <main className="app-main">
                <div className="container">
                    {error && (
                        <div className="error-message">
                            <div className="error-content">
                                <h3>❌ Processing Error</h3>
                                <p>{error}</p>
                                <button className="btn btn-primary" onClick={handleReset}>
                                    Try Again
                                </button>
                            </div>
                        </div>
                    )}

                    {!isProcessing && !results && !error && (
                        <FileUpload
                            onFilesSelected={handleFilesSelected}
                            isProcessing={isProcessing}
                        />
                    )}

                    {isProcessing && (
                        <LoadingSpinner message="Processing your documents..." />
                    )}

                    {results && !isProcessing && (
                        <div className="results-section">
                            <ResultsDisplay results={results} jobId={jobId} />
                            <div className="reset-section">
                                <button className="btn btn-secondary" onClick={handleReset}>
                                    📤 Process More Files
                                </button>
                            </div>
                        </div>
                    )}

                    {!isProcessing && !results && !error && (
                        <div className="features-section">
                            <h2>Features</h2>
                            <div className="features-grid">
                                <div className="feature-card">
                                    <div className="feature-icon">📄</div>
                                    <h3>Multi-Format Support</h3>
                                    <p>Process PNG, JPG, JPEG, WEBP, and PDF files with ease</p>
                                </div>
                                <div className="feature-card">
                                    <div className="feature-icon">🎯</div>
                                    <h3>High Accuracy</h3>
                                    <p>Advanced preprocessing and Tesseract OCR for optimal results</p>
                                </div>
                                <div className="feature-card">
                                    <div className="feature-icon">⚡</div>
                                    <h3>Batch Processing</h3>
                                    <p>Upload and process multiple files simultaneously</p>
                                </div>
                                <div className="feature-card">
                                    <div className="feature-icon">🌍</div>
                                    <h3>Multi-Language</h3>
                                    <p>Automatic language detection and support for 100+ languages</p>
                                </div>
                                <div className="feature-card">
                                    <div className="feature-icon">📊</div>
                                    <h3>Confidence Scoring</h3>
                                    <p>Per-word confidence levels with visual indicators</p>
                                </div>
                                <div className="feature-card">
                                    <div className="feature-icon">💾</div>
                                    <h3>Export Options</h3>
                                    <p>Copy to clipboard or download as TXT file</p>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </main>

            <footer className="app-footer">
                <div className="container">
                    <p>&copy; 2024 OCR Document Digitizer. Built with React and FastAPI.</p>
                    <div className="footer-links">
                        <span>Supported formats: PNG, JPG, JPEG, WEBP, PDF</span>
                        <span>Max file size: 10MB</span>
                        <span>Batch limit: 10 files</span>
                    </div>
                </div>
            </footer>
        </div>
    );
}

export default App;