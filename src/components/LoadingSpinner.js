import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({ message = "Processing...", progress = null }) => {
    return (
        <div className="loading-container">
            <div className="loading-content">
                <div className="spinner-wrapper">
                    <div className="spinner"></div>
                    {progress !== null && (
                        <div className="progress-ring">
                            <svg className="progress-svg" viewBox="0 0 36 36">
                                <path
                                    className="progress-bg"
                                    d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                                />
                                <path
                                    className="progress-bar"
                                    strokeDasharray={`${progress}, 100`}
                                    d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                                />
                            </svg>
                            <div className="progress-text">{Math.round(progress)}%</div>
                        </div>
                    )}
                </div>

                <div className="loading-message">
                    <h3>{message}</h3>
                    <p>This may take a few moments depending on file size and complexity</p>
                </div>

                <div className="loading-steps">
                    <div className="step active">
                        <div className="step-icon">📤</div>
                        <span>Uploading files</span>
                    </div>
                    <div className="step active">
                        <div className="step-icon">🔄</div>
                        <span>Preprocessing images</span>
                    </div>
                    <div className="step active">
                        <div className="step-icon">👁️</div>
                        <span>Extracting text</span>
                    </div>
                    <div className="step">
                        <div className="step-icon">✅</div>
                        <span>Finalizing results</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoadingSpinner;