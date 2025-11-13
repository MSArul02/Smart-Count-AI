
// simple_factory_script.js - Simple, Functional Interface Logic

class SimpleFactoryCounter {
    constructor() {
        this.isProcessing = false;
        this.initializeElements();
        this.setupEventListeners();
        this.initializeCamera();
        this.startStatsUpdates();
    }

    initializeElements() {
        // Camera and capture
        this.video = document.getElementById('video');
        this.captureBtn = document.getElementById('captureBtn');
        this.fileInput = document.getElementById('fileInput');
        this.uploadZone = document.getElementById('uploadZone');
        this.uploadPlaceholder = document.getElementById('uploadPlaceholder');

        // Settings
        this.confidenceSlider = document.getElementById('confidenceSlider');
        this.confidenceValue = document.getElementById('confidenceValue');

        // Results
        this.detectedCount = document.getElementById('detectedCount');
        this.confidenceScore = document.getElementById('confidenceScore');
        this.mostFrequentCount = document.getElementById('mostFrequentCount');
        this.consistencyScore = document.getElementById('consistencyScore');
        this.recommendation = document.getElementById('recommendation');

        // Image display
        this.resultImage = document.getElementById('resultImage');
        this.imagePlaceholder = document.getElementById('imagePlaceholder');
        this.loadingOverlay = document.getElementById('loadingOverlay');

        // Classification
        this.nutsCount = document.getElementById('nutsCount');
        this.boltsCount = document.getElementById('boltsCount');
        this.screwsCount = document.getElementById('screwsCount');
        this.washersCount = document.getElementById('washersCount');

        // Session stats
        this.totalImages = document.getElementById('totalImages');
        this.sessionTime = document.getElementById('sessionTime');
        this.averageCount = document.getElementById('averageCount');
        this.countRange = document.getElementById('countRange');

        // Actions
        this.exportBtn = document.getElementById('exportBtn');
        this.resetBtn = document.getElementById('resetBtn');

        // Notifications
        this.notifications = document.getElementById('notifications');
    }

    setupEventListeners() {
        // Primary controls
        this.captureBtn.addEventListener('click', () => this.captureAndAnalyze());
        this.fileInput.addEventListener('change', (e) => this.handleFileUpload(e));

        // Drag and drop
        this.uploadZone.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadZone.addEventListener('drop', (e) => this.handleDrop(e));
        this.uploadZone.addEventListener('click', () => this.fileInput.click());

        // Settings
        this.confidenceSlider.addEventListener('input', (e) => {
            this.confidenceValue.textContent = e.target.value;
        });

        // Actions
        this.exportBtn.addEventListener('click', () => this.exportData());
        this.resetBtn.addEventListener('click', () => this.resetSession());
    }

    async initializeCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' }
            });
            this.video.srcObject = stream;
            this.video.style.display = 'block';
            this.uploadPlaceholder.style.display = 'none';
        } catch (error) {
            console.warn('Camera not available:', error);
            this.video.style.display = 'none';
            this.uploadPlaceholder.style.display = 'flex';
        }
    }

    startStatsUpdates() {
        // Update session statistics every 5 seconds
        setInterval(() => {
            this.updateSessionStats();
        }, 5000);
    }

    async captureAndAnalyze() {
        if (this.isProcessing) return;

        if (!this.video.videoWidth) {
            this.showNotification('Camera not ready. Please upload an image.', 'warning');
            return;
        }

        try {
            const canvas = document.createElement('canvas');
            canvas.width = this.video.videoWidth;
            canvas.height = this.video.videoHeight;

            const ctx = canvas.getContext('2d');
            ctx.drawImage(this.video, 0, 0);

            canvas.toBlob((blob) => {
                if (blob) {
                    this.analyzeImage(blob);
                }
            }, 'image/jpeg', 0.9);
        } catch (error) {
            this.showNotification('Capture failed. Please try again.', 'error');
        }
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        if (!file.type.startsWith('image/')) {
            this.showNotification('Please select a valid image file', 'error');
            return;
        }

        this.analyzeImage(file);
    }

    handleDragOver(event) {
        event.preventDefault();
        this.uploadZone.style.borderColor = 'var(--primary-color)';
    }

    handleDrop(event) {
        event.preventDefault();
        this.uploadZone.style.borderColor = '';

        const files = event.dataTransfer.files;
        if (files.length > 0 && files[0].type.startsWith('image/')) {
            this.analyzeImage(files[0]);
        } else {
            this.showNotification('Please drop a valid image file', 'error');
        }
    }

    async analyzeImage(imageFile) {
        if (this.isProcessing) return;

        this.setProcessingState(true);

        try {
            const formData = new FormData();
            formData.append('image', imageFile);
            formData.append('min_confidence', this.confidenceSlider.value);

            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.ok) {
                this.updateResults(result);
                this.showNotification(
                    `Analysis complete: ${result.count} objects detected`, 
                    'success'
                );
            } else {
                this.showNotification(result.error || 'Analysis failed', 'error');
            }

        } catch (error) {
            console.error('Analysis failed:', error);
            this.showNotification('Analysis failed. Please try again.', 'error');
        } finally {
            this.setProcessingState(false);
        }
    }

    updateResults(result) {
        // Update main metrics
        this.animateNumber(this.detectedCount, result.count);
        this.animateNumber(this.confidenceScore, Math.round(result.confidence * 100), '%');

        // Update vibration analysis
        const vibration = result.vibration_analysis;
        this.animateNumber(this.mostFrequentCount, vibration.most_frequent_count);
        this.animateNumber(this.consistencyScore, Math.round(vibration.consistency_score * 100), '%');
        this.recommendation.textContent = vibration.recommendation;

        // Update classifications
        const classifications = result.classifications;
        this.animateNumber(this.nutsCount, classifications.nuts || 0);
        this.animateNumber(this.boltsCount, classifications.bolts || 0);
        this.animateNumber(this.screwsCount, classifications.screws || 0);
        this.animateNumber(this.washersCount, classifications.washers || 0);

        // Update result image
        if (result.result_path) {
            this.resultImage.src = result.result_path + '?t=' + Date.now();
            this.resultImage.classList.add('show');
            this.imagePlaceholder.style.display = 'none';
        }
    }

    async updateSessionStats() {
        try {
            const response = await fetch('/api/session-stats');
            const data = await response.json();

            if (data.ok) {
                const stats = data.statistics;
                this.totalImages.textContent = stats.total_images;
                this.sessionTime.textContent = `${stats.session_duration_minutes} min`;
                this.averageCount.textContent = stats.average_count;
                this.countRange.textContent = `${stats.min_count} - ${stats.max_count}`;
            }
        } catch (error) {
            console.warn('Failed to update session stats:', error);
        }
    }

    async exportData() {
        try {
            this.showNotification('Exporting session data...', 'info');

            const response = await fetch('/api/export-data', {
                method: 'POST'
            });

            const result = await response.json();

            if (result.ok) {
                // Create download link
                const link = document.createElement('a');
                link.href = result.download_url;
                link.download = result.filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                this.showNotification('Data exported successfully', 'success');
            } else {
                this.showNotification('Export failed', 'error');
            }
        } catch (error) {
            this.showNotification('Export failed', 'error');
        }
    }

    async resetSession() {
        const confirmed = confirm('Are you sure you want to reset the session? All data will be lost.');
        if (!confirmed) return;

        try {
            const response = await fetch('/api/reset-session', {
                method: 'POST'
            });

            const result = await response.json();

            if (result.ok) {
                this.clearAllDisplays();
                this.showNotification('Session reset successfully', 'success');
            } else {
                this.showNotification('Reset failed', 'error');
            }
        } catch (error) {
            this.showNotification('Reset failed', 'error');
        }
    }

    setProcessingState(processing) {
        this.isProcessing = processing;

        if (processing) {
            this.captureBtn.disabled = true;
            this.captureBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Processing...</span>';
            this.loadingOverlay.classList.add('show');
        } else {
            this.captureBtn.disabled = false;
            this.captureBtn.innerHTML = '<i class="fas fa-camera"></i><span>Capture & Analyze</span>';
            this.loadingOverlay.classList.remove('show');
        }
    }

    clearAllDisplays() {
        // Reset metrics
        this.detectedCount.textContent = '0';
        this.confidenceScore.textContent = '0%';
        this.mostFrequentCount.textContent = '0';
        this.consistencyScore.textContent = '0%';
        this.recommendation.textContent = 'Take multiple images after physically vibrating the plate';

        // Reset classifications
        this.nutsCount.textContent = '0';
        this.boltsCount.textContent = '0';
        this.screwsCount.textContent = '0';
        this.washersCount.textContent = '0';

        // Reset image
        this.resultImage.classList.remove('show');
        this.imagePlaceholder.style.display = 'flex';

        // Reset session stats
        this.totalImages.textContent = '0';
        this.sessionTime.textContent = '0.0 min';
        this.averageCount.textContent = '0';
        this.countRange.textContent = '0 - 0';
    }

    animateNumber(element, targetValue, suffix = '') {
        const currentValue = parseInt(element.textContent) || 0;
        const increment = (targetValue - currentValue) / 20;
        let current = currentValue;

        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= targetValue) || 
                (increment < 0 && current <= targetValue)) {
                element.textContent = targetValue + suffix;
                clearInterval(timer);
            } else {
                element.textContent = Math.round(current) + suffix;
            }
        }, 50);
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;

        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };

        notification.innerHTML = `
            <i class="fas fa-${icons[type]}"></i>
            <span>${message}</span>
        `;

        this.notifications.appendChild(notification);

        // Auto remove after 4 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.animation = 'slideIn 0.3s ease reverse';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }
        }, 4000);
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.simpleFactoryCounter = new SimpleFactoryCounter();
    console.log('🏭 Simple Factory Counter initialized');
});
