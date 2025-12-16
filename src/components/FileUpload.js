import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import './FileUpload.css';

const FileUpload = ({ onFilesSelected, isProcessing }) => {
    const [dragActive, setDragActive] = useState(false);

    const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
        if (rejectedFiles.length > 0) {
            const errors = rejectedFiles.map(file =>
                `${file.file.name}: ${file.errors.map(e => e.message).join(', ')}`
            );
            alert(`Some files were rejected:\n${errors.join('\n')}`);
        }

        if (acceptedFiles.length > 0) {
            onFilesSelected(acceptedFiles);
        }
    }, [onFilesSelected]);

    const {
        getRootProps,
        getInputProps,
        isDragActive,
        isDragAccept,
        isDragReject
    } = useDropzone({
        onDrop,
        accept: {
            'image/png': ['.png'],
            'image/jpeg': ['.jpg', '.jpeg'],
            'image/webp': ['.webp'],
            'application/pdf': ['.pdf']
        },
        maxSize: 10 * 1024 * 1024, // 10MB
        maxFiles: 10,
        disabled: isProcessing
    });

    const getDropzoneClassName = () => {
        let className = 'dropzone';
        if (isDragActive) className += ' drag-active';
        if (isDragAccept) className += ' drag-accept';
        if (isDragReject) className += ' drag-reject';
        if (isProcessing) className += ' disabled';
        return className;
    };

    return (
        <div className="file-upload-container">
            <div {...getRootProps({ className: getDropzoneClassName() })}>
                <input {...getInputProps()} />

                <div className="dropzone-content">
                    <div className="upload-icon">
                        📄
                    </div>

                    {isDragActive ? (
                        <div className="dropzone-text">
                            <h3>Drop files here...</h3>
                        </div>
                    ) : (
                        <div className="dropzone-text">
                            <h3>Drag & drop files here</h3>
                            <p>or click to select files</p>
                            <div className="supported-formats">
                                <strong>Supported formats:</strong> PNG, JPG, JPEG, WEBP, PDF
                            </div>
                            <div className="file-limits">
                                Max 10MB per file • Up to 10 files at once
                            </div>
                        </div>
                    )}

                    {isProcessing && (
                        <div className="processing-overlay">
                            <div className="spinner"></div>
                            <p>Processing files...</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default FileUpload;