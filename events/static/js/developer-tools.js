/**
 * Momenta Developer Tools - Frontend JavaScript Debugging Utilities
 * 
 * This script provides browser-based debugging tools for the Momenta Event Management System
 */

class MomentaDevTools {
    constructor() {
        this.isEnabled = this.checkDebugMode();
        this.logs = [];
        this.performanceMetrics = {};
        this.ajaxRequests = [];
        
        if (this.isEnabled) {
            this.init();
        }
    }
    
    checkDebugMode() {
        // Check if we're in debug mode by looking for debug indicators
        return document.querySelector('meta[name="debug-mode"]')?.content === 'true' ||
               window.location.hostname === 'localhost' ||
               window.location.hostname === '127.0.0.1';
    }
    
    init() {
        console.log('🔧 Momenta Developer Tools Initialized');
        
        // Add developer tools to window for global access
        window.MomentaDevTools = this;
        
        // Initialize components
        this.setupPerformanceMonitoring();
        this.setupAjaxInterception();
        this.setupErrorHandling();
        this.setupKeyboardShortcuts();
        this.createDevToolsPanel();
        
        // Log initial page load
        this.log('Page loaded', 'info');
    }
    
    setupPerformanceMonitoring() {
        // Monitor page load performance
        window.addEventListener('load', () => {
            const perfData = performance.getEntriesByType('navigation')[0];
            this.performanceMetrics.pageLoad = {
                domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
                totalTime: perfData.loadEventEnd - perfData.fetchStart
            };
            
            this.log(`Page load completed in ${this.performanceMetrics.pageLoad.totalTime.toFixed(2)}ms`, 'performance');
        });
        
        // Monitor resource loading
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.duration > 1000) { // Log slow resources (>1s)
                    this.log(`Slow resource: ${entry.name} (${entry.duration.toFixed(2)}ms)`, 'warning');
                }
            }
        });
        observer.observe({entryTypes: ['resource']});
    }
    
    setupAjaxInterception() {
        // Intercept fetch requests
        const originalFetch = window.fetch;
        window.fetch = (...args) => {
            const startTime = performance.now();
            const url = args[0];
            
            this.log(`AJAX Request: ${url}`, 'ajax');
            
            return originalFetch.apply(this, args)
                .then(response => {
                    const duration = performance.now() - startTime;
                    this.ajaxRequests.push({
                        url,
                        method: args[1]?.method || 'GET',
                        status: response.status,
                        duration,
                        timestamp: new Date()
                    });
                    
                    this.log(`AJAX Response: ${url} (${response.status}) - ${duration.toFixed(2)}ms`, 'ajax');
                    return response;
                })
                .catch(error => {
                    this.log(`AJAX Error: ${url} - ${error.message}`, 'error');
                    throw error;
                });
        };
        
        // Intercept XMLHttpRequest
        const originalXHR = window.XMLHttpRequest;
        window.XMLHttpRequest = function() {
            const xhr = new originalXHR();
            const originalOpen = xhr.open;
            const originalSend = xhr.send;
            
            xhr.open = function(method, url) {
                this._devtools_method = method;
                this._devtools_url = url;
                this._devtools_startTime = performance.now();
                return originalOpen.apply(this, arguments);
            };
            
            xhr.send = function() {
                window.MomentaDevTools.log(`XHR Request: ${this._devtools_method} ${this._devtools_url}`, 'ajax');
                
                this.addEventListener('loadend', () => {
                    const duration = performance.now() - this._devtools_startTime;
                    window.MomentaDevTools.log(`XHR Response: ${this._devtools_url} (${this.status}) - ${duration.toFixed(2)}ms`, 'ajax');
                });
                
                return originalSend.apply(this, arguments);
            };
            
            return xhr;
        };
    }
    
    setupErrorHandling() {
        // Global error handler
        window.addEventListener('error', (event) => {
            this.log(`JavaScript Error: ${event.message} at ${event.filename}:${event.lineno}`, 'error');
        });
        
        // Unhandled promise rejection handler
        window.addEventListener('unhandledrejection', (event) => {
            this.log(`Unhandled Promise Rejection: ${event.reason}`, 'error');
        });
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            // Ctrl+Shift+D to toggle dev tools panel
            if (event.ctrlKey && event.shiftKey && event.key === 'D') {
                event.preventDefault();
                this.toggleDevPanel();
            }
            
            // Ctrl+Shift+C to clear console
            if (event.ctrlKey && event.shiftKey && event.key === 'C') {
                event.preventDefault();
                this.clearLogs();
            }
            
            // Ctrl+Shift+P to show performance metrics
            if (event.ctrlKey && event.shiftKey && event.key === 'P') {
                event.preventDefault();
                this.showPerformanceMetrics();
            }
        });
    }
    
    createDevToolsPanel() {
        // Create floating dev tools panel
        const panel = document.createElement('div');
        panel.id = 'momenta-dev-panel';
        panel.innerHTML = `
            <div class="dev-panel-header">
                <span>🔧 Momenta Dev Tools</span>
                <button onclick="MomentaDevTools.toggleDevPanel()">×</button>
            </div>
            <div class="dev-panel-content">
                <div class="dev-tabs">
                    <button class="dev-tab active" onclick="MomentaDevTools.showTab('console')">Console</button>
                    <button class="dev-tab" onclick="MomentaDevTools.showTab('network')">Network</button>
                    <button class="dev-tab" onclick="MomentaDevTools.showTab('performance')">Performance</button>
                </div>
                <div id="dev-console-tab" class="dev-tab-content active">
                    <div id="dev-console-output"></div>
                    <input type="text" id="dev-console-input" placeholder="Enter JavaScript command..." />
                </div>
                <div id="dev-network-tab" class="dev-tab-content">
                    <div id="dev-network-output"></div>
                </div>
                <div id="dev-performance-tab" class="dev-tab-content">
                    <div id="dev-performance-output"></div>
                </div>
            </div>
        `;
        
        // Add styles
        const styles = `
            <style>
                #momenta-dev-panel {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    width: 400px;
                    height: 300px;
                    background: #1e1e1e;
                    color: #fff;
                    border-radius: 8px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                    z-index: 10000;
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    display: none;
                }
                
                .dev-panel-header {
                    background: #333;
                    padding: 8px 12px;
                    border-radius: 8px 8px 0 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    cursor: move;
                }
                
                .dev-panel-header button {
                    background: none;
                    border: none;
                    color: #fff;
                    cursor: pointer;
                    font-size: 16px;
                }
                
                .dev-tabs {
                    display: flex;
                    background: #2a2a2a;
                }
                
                .dev-tab {
                    background: none;
                    border: none;
                    color: #ccc;
                    padding: 8px 12px;
                    cursor: pointer;
                    border-bottom: 2px solid transparent;
                }
                
                .dev-tab.active {
                    color: #fff;
                    border-bottom-color: #007acc;
                }
                
                .dev-tab-content {
                    display: none;
                    height: 220px;
                    overflow-y: auto;
                    padding: 8px;
                }
                
                .dev-tab-content.active {
                    display: block;
                }
                
                #dev-console-output {
                    height: 180px;
                    overflow-y: auto;
                    margin-bottom: 8px;
                    padding: 4px;
                    background: #000;
                    border-radius: 4px;
                }
                
                #dev-console-input {
                    width: 100%;
                    background: #333;
                    border: 1px solid #555;
                    color: #fff;
                    padding: 4px;
                    border-radius: 4px;
                }
                
                .log-entry {
                    margin-bottom: 2px;
                    padding: 2px 4px;
                    border-radius: 2px;
                }
                
                .log-info { color: #87CEEB; }
                .log-warning { color: #FFA500; background: rgba(255,165,0,0.1); }
                .log-error { color: #FF6B6B; background: rgba(255,107,107,0.1); }
                .log-ajax { color: #98FB98; }
                .log-performance { color: #DDA0DD; }
            </style>
        `;
        
        document.head.insertAdjacentHTML('beforeend', styles);
        document.body.appendChild(panel);
        
        // Setup console input
        document.getElementById('dev-console-input').addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                const command = event.target.value;
                if (command.trim()) {
                    this.executeCommand(command);
                    event.target.value = '';
                }
            }
        });
        
        // Make panel draggable
        this.makeDraggable(panel);
    }
    
    makeDraggable(element) {
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        const header = element.querySelector('.dev-panel-header');
        
        header.onmousedown = dragMouseDown;
        
        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;
        }
        
        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            element.style.top = (element.offsetTop - pos2) + "px";
            element.style.left = (element.offsetLeft - pos1) + "px";
            element.style.bottom = 'auto';
            element.style.right = 'auto';
        }
        
        function closeDragElement() {
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }
    
    log(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = {
            message,
            type,
            timestamp
        };
        
        this.logs.push(logEntry);
        
        // Also log to browser console
        console.log(`[Momenta DevTools] ${message}`);
        
        // Update dev panel if visible
        this.updateConsoleOutput();
    }
    
    updateConsoleOutput() {
        const output = document.getElementById('dev-console-output');
        if (output) {
            output.innerHTML = this.logs.map(log => 
                `<div class="log-entry log-${log.type}">[${log.timestamp}] ${log.message}</div>`
            ).join('');
            output.scrollTop = output.scrollHeight;
        }
    }
    
    toggleDevPanel() {
        const panel = document.getElementById('momenta-dev-panel');
        if (panel) {
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
            if (panel.style.display === 'block') {
                this.updateConsoleOutput();
                this.updateNetworkOutput();
                this.updatePerformanceOutput();
            }
        }
    }
    
    showTab(tabName) {
        // Hide all tabs
        document.querySelectorAll('.dev-tab').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('.dev-tab-content').forEach(content => content.classList.remove('active'));
        
        // Show selected tab
        document.querySelector(`button[onclick="MomentaDevTools.showTab('${tabName}')"]`).classList.add('active');
        document.getElementById(`dev-${tabName}-tab`).classList.add('active');
        
        // Update content
        if (tabName === 'network') this.updateNetworkOutput();
        if (tabName === 'performance') this.updatePerformanceOutput();
    }
    
    updateNetworkOutput() {
        const output = document.getElementById('dev-network-output');
        if (output) {
            output.innerHTML = this.ajaxRequests.map(req => 
                `<div class="log-entry">
                    <strong>${req.method}</strong> ${req.url}<br>
                    Status: ${req.status} | Duration: ${req.duration.toFixed(2)}ms
                </div>`
            ).join('');
        }
    }
    
    updatePerformanceOutput() {
        const output = document.getElementById('dev-performance-output');
        if (output) {
            let content = '<div class="log-entry"><strong>Page Load Metrics:</strong></div>';
            
            if (this.performanceMetrics.pageLoad) {
                const metrics = this.performanceMetrics.pageLoad;
                content += `
                    <div class="log-entry">DOM Content Loaded: ${metrics.domContentLoaded.toFixed(2)}ms</div>
                    <div class="log-entry">Load Complete: ${metrics.loadComplete.toFixed(2)}ms</div>
                    <div class="log-entry">Total Time: ${metrics.totalTime.toFixed(2)}ms</div>
                `;
            }
            
            content += '<div class="log-entry"><strong>Memory Usage:</strong></div>';
            if (performance.memory) {
                content += `
                    <div class="log-entry">Used: ${(performance.memory.usedJSHeapSize / 1048576).toFixed(2)} MB</div>
                    <div class="log-entry">Total: ${(performance.memory.totalJSHeapSize / 1048576).toFixed(2)} MB</div>
                    <div class="log-entry">Limit: ${(performance.memory.jsHeapSizeLimit / 1048576).toFixed(2)} MB</div>
                `;
            }
            
            output.innerHTML = content;
        }
    }
    
    executeCommand(command) {
        this.log(`> ${command}`, 'info');
        
        try {
            const result = eval(command);
            this.log(String(result), 'info');
        } catch (error) {
            this.log(`Error: ${error.message}`, 'error');
        }
    }
    
    clearLogs() {
        this.logs = [];
        this.updateConsoleOutput();
        console.clear();
        this.log('Console cleared', 'info');
    }
    
    showPerformanceMetrics() {
        console.group('🚀 Performance Metrics');
        console.log('Page Load:', this.performanceMetrics.pageLoad);
        console.log('AJAX Requests:', this.ajaxRequests);
        console.log('Memory Usage:', performance.memory);
        console.groupEnd();
    }
    
    // Public API methods
    inspect(element) {
        console.log('🔍 Element Inspector:', element);
        console.log('Properties:', Object.getOwnPropertyNames(element));
        console.log('Computed Style:', window.getComputedStyle(element));
    }
    
    measurePerformance(fn, name = 'Function') {
        const start = performance.now();
        const result = fn();
        const end = performance.now();
        this.log(`${name} executed in ${(end - start).toFixed(2)}ms`, 'performance');
        return result;
    }
}

// Initialize developer tools when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new MomentaDevTools();
    });
} else {
    new MomentaDevTools();
}

// Add keyboard shortcut info to console
console.log(`
🔧 Momenta Developer Tools Loaded
Keyboard Shortcuts:
  Ctrl+Shift+D - Toggle Dev Panel
  Ctrl+Shift+C - Clear Console
  Ctrl+Shift+P - Show Performance Metrics

Available Commands:
  MomentaDevTools.inspect(element) - Inspect DOM element
  MomentaDevTools.measurePerformance(fn, name) - Measure function performance
  MomentaDevTools.toggleDevPanel() - Toggle dev panel
`);