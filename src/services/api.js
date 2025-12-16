import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 300000, // 5 minutes for OCR processing
});

export const ocrAPI = {
    /**
     * Upload files for OCR processing
     * @param {FileList} files - Files to upload
     * @returns {Promise} API response with job_id
     */
    uploadFiles: async (files) => {
        const formData = new FormData();

        // Add all files to form data
        Array.from(files).forEach((file) => {
            formData.append('files', file);
        });

        const response = await api.post('/api/ocr/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        return response.data;
    },

    /**
     * Get OCR results for a job
     * @param {string} jobId - Job ID
     * @returns {Promise} API response with results
     */
    getResults: async (jobId) => {
        const response = await api.get(`/api/ocr/result/${jobId}`);
        return response.data;
    },

    /**
     * Poll for job completion
     * @param {string} jobId - Job ID
     * @param {function} onUpdate - Callback for status updates
     * @param {number} maxAttempts - Maximum polling attempts
     * @returns {Promise} Final results
     */
    pollForResults: async (jobId, onUpdate = null, maxAttempts = 60) => {
        let attempts = 0;

        while (attempts < maxAttempts) {
            try {
                const result = await ocrAPI.getResults(jobId);

                if (onUpdate) {
                    onUpdate(result);
                }

                if (result.status === 'completed' || result.status === 'failed') {
                    return result;
                }

                // Wait 2 seconds before next poll
                await new Promise(resolve => setTimeout(resolve, 2000));
                attempts++;

            } catch (error) {
                console.error('Polling error:', error);
                attempts++;

                if (attempts >= maxAttempts) {
                    throw new Error('Polling timeout');
                }

                // Wait before retry
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }

        throw new Error('Job processing timeout');
    },

    /**
     * Get health status
     * @returns {Promise} Health status
     */
    getHealth: async () => {
        const response = await api.get('/api/health');
        return response.data;
    },

    /**
     * Get supported file formats
     * @returns {Promise} Supported formats info
     */
    getSupportedFormats: async () => {
        const response = await api.get('/api/supported-formats');
        return response.data;
    },

    /**
     * Delete a job
     * @param {string} jobId - Job ID to delete
     * @returns {Promise} Deletion confirmation
     */
    deleteJob: async (jobId) => {
        const response = await api.delete(`/api/ocr/job/${jobId}`);
        return response.data;
    }
};

export default api;