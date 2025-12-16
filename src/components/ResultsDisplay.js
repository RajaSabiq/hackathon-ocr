import React, { useState } from 'react';
import './ResultsDisplay.css';

const ResultsDisplay = ({ results, jobId }) => {
    const [selectedResult, setSelectedResult] = useState(0);
    const [showBoundingBoxes, setShowBoundingBoxes] = useState(false);
    const [copySuccess, setCopySuccess] = useState(false);

    if (!results || results.length === 0) {
        return null;
    }

    const currentResult = results[selectedResult];

    const handleCopyText = async () => {
        try {
            await navigator.clipboard.writeText(currentResult.text);
            setCopySuccess(true);
            setTimeout(() => setCopySuccess(false), 2000);
        } catch (err) {
            console.error('Failed to copy text:', err);
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = currentResult.text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            setCopySuccess(true);
            setTimeout(() => setCopySuccess(false), 2000);
        }
    };

    const handleDownloadText = () => {
        const blob = new Blob([currentResult.text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${currentResult.filename.replace(/\.[^/.]+$/, '')}_extracted.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const getConfidenceColor = (confidence) => {
        if (confidence >= 0.8) return '#28a745'; // Green
        if (confidence >= 0.6) return '#ffc107'; // Yellow
        return '#dc3545'; // Red
    };

    const getConfidenceLabel = (confidence) => {
        if (confidence >= 0.8) return 'High';
        if (confidence >= 0.6) return 'Medium';
        return 'Low';
    };

    const renderBoundingBoxInfo = () => {
        if (!showBoundingBoxes || !currentResult.bbox_data) {
            return null;
        }

        const lowConfidenceWords = currentResult.bbox_data.filter(bbox => bbox.confidence < 0.6);

        return (
            <div className="bounding-box-info">
                <h4>Text Analysis</h4>
                <div className="bbox-stats">
                    <div className="stat">
                        <span className="stat-label">Total Words:</span>
                        <span className="stat-value">{currentResult.bbox_data.length}</span>
                    </div>
                    <div className="stat">
                        <span className="stat-label">Low Confidence:</span>
                        <span className="stat-value" style={{ color: '#dc3545' }}>
                            {lowConfidenceWords.length}
                        </span>
                    </div>
                </div>

                {lowConfidenceWords.length > 0 && (
                    <div className="low-confidence-words">
                        <h5>Words with Low Confidence:</h5>
                        <div className="word-list">
                            {lowConfidenceWords.map((bbox, index) => (
                                <span
                                    key={index}
                                    className="low-confidence-word"
                                    title={`Confidence: ${(bbox.confidence * 100).toFixed(1)}%`}
                                >
                                    {bbox.text}
                                </span>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        );
    };

    return (
        <div className="results-container">
            <div className="results-header">
                <h2>OCR Results</h2>
                <div className="job-info">
                    <span className="job-id">Job ID: {jobId}</span>
                    <span className="results-count">{results.length} file{results.length > 1 ? 's' : ''} processed</span>
                </div>
            </div>

            {results.length > 1 && (
                <div className="file-selector">
                    <label htmlFor="file-select">Select file:</label>
                    <select
                        id="file-select"
                        value={selectedResult}
                        onChange={(e) => setSelectedResult(parseInt(e.target.value))}
                    >
                        {results.map((result, index) => (
                            <option key={index} value={index}>
                                {result.filename}
                            </option>
                        ))}
                    </select>
                </div>
            )}

            <div className="result-card">
                <div className="result-header">
                    <div className="file-info">
                        <h3>{currentResult.filename}</h3>
                        <div className="metadata">
                            <span className="language">Language: {currentResult.language.toUpperCase()}</span>
                            <span
                                className="confidence"
                                style={{ color: getConfidenceColor(currentResult.confidence) }}
                            >
                                Confidence: {getConfidenceLabel(currentResult.confidence)} ({(currentResult.confidence * 100).toFixed(1)}%)
                            </span>
                            {currentResult.page_number && (
                                <span className="page-number">Page: {currentResult.page_number}</span>
                            )}
                        </div>
                    </div>

                    <div className="result-actions">
                        <button
                            className="btn btn-secondary"
                            onClick={() => setShowBoundingBoxes(!showBoundingBoxes)}
                        >
                            {showBoundingBoxes ? 'Hide' : 'Show'} Analysis
                        </button>
                        <button
                            className={`btn btn-primary ${copySuccess ? 'success' : ''}`}
                            onClick={handleCopyText}
                        >
                            {copySuccess ? '✓ Copied!' : '📋 Copy Text'}
                        </button>
                        <button
                            className="btn btn-success"
                            onClick={handleDownloadText}
                        >
                            💾 Download TXT
                        </button>
                    </div>
                </div>

                <div className="text-content">
                    <div className="text-stats">
                        <span>Characters: {currentResult.text.length}</span>
                        <span>Words: {currentResult.text.split(/\s+/).filter(word => word.length > 0).length}</span>
                        <span>Lines: {currentResult.text.split('\n').length}</span>
                    </div>

                    <div className="extracted-text">
                        <h4>Extracted Text:</h4>
                        <div className="text-output">
                            {currentResult.text || <em>No text detected</em>}
                        </div>
                    </div>
                </div>

                {renderBoundingBoxInfo()}
            </div>
        </div>
    );
};

export default ResultsDisplay;