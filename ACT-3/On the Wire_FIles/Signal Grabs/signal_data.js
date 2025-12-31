
        // WebSocket connections storage
        const connections = {};
        const maxSignalBits = 500;
        const maxLogMessages = 50;

        // Signal data storage for each wire
        const signalData = {
            'dq': [],
            'mosi': [],
            'sck': [],
            'sda': [],
            'scl': []
        };

        // Zoom level for each wire (pixels per bit)
        const zoomLevels = {
            'dq': 4,
            'mosi': 4,
            'sck': 4,
            'sda': 4,
            'scl': 4
        };

        const MIN_ZOOM = 1;
        const MAX_ZOOM = 20;

        // Canvas settings
        const CANVAS_HEIGHT = 54;
        const HIGH_LEVEL = 8;
        const LOW_LEVEL = CANVAS_HEIGHT - 8;
        const LINE_COLOR = '#00ff41';
        const GLOW_COLOR = 'rgba(0, 255, 65, 0.5)';
        const GRID_COLOR = 'rgba(0, 255, 65, 0.1)';

        // Wire to protocol mapping
        const wireToProtocol = {
            'dq': '1wire',
            'mosi': 'spi',
            'sck': 'spi',
            'sda': 'i2c',
            'scl': 'i2c'
        };

        // Tab switching with auto-connect
        function switchTab(tabName) {
            // Disconnect wires from previous tab
            const previousTab = document.querySelector('.tab-content.active');
            if (previousTab) {
                const previousTabId = previousTab.id.replace('tab-', '');
                const wiresToDisconnect = getProtocolWires(previousTabId);
                wiresToDisconnect.forEach(wire => disconnectWire(wire));
            }

            // Update tab buttons
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.closest('.tab-button').classList.add('active');

            // Update tab content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(`tab-${tabName}`).classList.add('active');

            // Auto-connect wires for new tab
            const wiresToConnect = getProtocolWires(tabName);
            wiresToConnect.forEach(wire => connectWire(wire, tabName));
        }

        // Helper function to get wires for a protocol
        function getProtocolWires(protocol) {
            const protocolWires = {
                '1wire': ['dq'],
                'spi': ['mosi', 'sck'],
                'i2c': ['sda', 'scl']
            };
            return protocolWires[protocol] || [];
        }

        // Initialize canvases
        function initCanvas(wireName) {
            const canvas = document.getElementById(`canvas-${wireName}`);
            if (!canvas) return null;

            const container = canvas.parentElement;
            const width = container.clientWidth - 16;
            canvas.width = width;
            canvas.height = CANVAS_HEIGHT;
            canvas.style.width = width + 'px';
            canvas.style.height = CANVAS_HEIGHT + 'px';

            const ctx = canvas.getContext('2d');
            drawGrid(ctx, width, CANVAS_HEIGHT);
            
            return { canvas, ctx };
        }

        // Draw oscilloscope grid
        function drawGrid(ctx, width, height) {
            ctx.strokeStyle = GRID_COLOR;
            ctx.lineWidth = 1;

            for (let y = 0; y < height; y += 13) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(width, y);
                ctx.stroke();
            }

            for (let x = 0; x < width; x += 16) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, height);
                ctx.stroke();
            }
        }

        // Draw waveform on canvas
        function drawWaveform(wireName) {
            const canvasInfo = initCanvas(wireName);
            if (!canvasInfo) return;

            const { canvas, ctx } = canvasInfo;
            const width = canvas.width;
            const data = signalData[wireName];
            const pixelsPerBit = zoomLevels[wireName];

            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, width, CANVAS_HEIGHT);
            drawGrid(ctx, width, CANVAS_HEIGHT);

            if (data.length === 0) return;

            const maxBitsOnScreen = Math.floor(width / pixelsPerBit);
            const startIdx = Math.max(0, data.length - maxBitsOnScreen);
            const visibleData = data.slice(startIdx);

            // Draw glow effect
            ctx.strokeStyle = GLOW_COLOR;
            ctx.lineWidth = 3;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            drawSignalPath(ctx, visibleData, 0, pixelsPerBit);

            // Draw main signal line
            ctx.strokeStyle = LINE_COLOR;
            ctx.lineWidth = 2;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            drawSignalPath(ctx, visibleData, 0, pixelsPerBit);

            // Draw dots at transitions
            ctx.fillStyle = LINE_COLOR;
            for (let i = 0; i < visibleData.length; i++) {
                const x = i * pixelsPerBit;
                const y = visibleData[i] === 1 ? HIGH_LEVEL : LOW_LEVEL;
                
                if (i === 0 || visibleData[i] !== visibleData[i - 1]) {
                    ctx.beginPath();
                    ctx.arc(x, y, 2, 0, Math.PI * 2);
                    ctx.fill();
                }
            }
        }

        // Draw the signal path
        function drawSignalPath(ctx, data, xOffset, pixelsPerBit) {
            if (data.length === 0) return;

            ctx.beginPath();
            
            let currentY = data[0] === 1 ? HIGH_LEVEL : LOW_LEVEL;
            ctx.moveTo(xOffset, currentY);

            for (let i = 0; i < data.length; i++) {
                const x = i * pixelsPerBit + xOffset;
                const nextY = data[i] === 1 ? HIGH_LEVEL : LOW_LEVEL;

                if (i > 0 && data[i] !== data[i - 1]) {
                    ctx.lineTo(x, currentY);
                    ctx.lineTo(x, nextY);
                } else {
                    ctx.lineTo(x, nextY);
                }

                currentY = nextY;
            }

            ctx.lineTo(data.length * pixelsPerBit + xOffset, currentY);
            ctx.stroke();
        }

        // Handle zoom via mousewheel
        function handleZoom(wireName, event) {
            event.preventDefault();
            
            const zoomDelta = event.deltaY > 0 ? -0.5 : 0.5;
            const newZoom = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, zoomLevels[wireName] + zoomDelta));
            
            if (newZoom !== zoomLevels[wireName]) {
                zoomLevels[wireName] = newZoom;
                drawWaveform(wireName);
                updateZoomIndicator(wireName);
            }
        }

        // Update zoom indicator display
        function updateZoomIndicator(wireName) {
            const indicator = document.getElementById(`zoom-${wireName}`);
            if (indicator) {
                indicator.textContent = `${zoomLevels[wireName].toFixed(1)}x`;
            }
        }

        // Attach zoom handlers to canvases
        function attachZoomHandler(wireName) {
            const canvas = document.getElementById(`canvas-${wireName}`);
            if (canvas) {
                canvas.addEventListener('wheel', (e) => handleZoom(wireName, e), { passive: false });
                canvas.style.cursor = 'zoom-in';
                canvas.title = `Scroll to zoom (${zoomLevels[wireName].toFixed(1)}x)`;
            }
        }

        // Connect to a specific wire
        function connectWire(wireName, protocolName) {
            if (connections[wireName]) {
                addLog(protocolName, `Already connected to ${wireName}`);
                return;
            }

            initCanvas(wireName);

            const proto = location.protocol === 'https:' ? 'wss' : 'ws';
            const host = location.host || location.hostname; // includes port if present in current URL
            const ws = new WebSocket(`${proto}://${host}/wire/${wireName}`);
            connections[wireName] = ws;

            ws.onopen = () => {
                updateStatus(protocolName);
                addLog(protocolName, `Connected to ${wireName}`);
            };

            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    
                    if (data.type === 'welcome') {
                        addLog(protocolName, `Server: ${data.message}`);
                        return;
                    }

                    if (data.line && typeof data.v !== 'undefined') {
                        updateSignal(data.line, data.v, data.t);
                        updateFrameCount(data.line);
                    }
                } catch (e) {
                    console.error('Error parsing message:', e);
                }
            };

            ws.onerror = (error) => {
                console.error(`WebSocket error on ${wireName}:`, error);
                addLog(protocolName, `Error on ${wireName}`);
            };

            ws.onclose = () => {
                delete connections[wireName];
                updateStatus(protocolName);
                addLog(protocolName, `Disconnected from ${wireName}`);
            };
        }

        // Disconnect from a specific wire
        function disconnectWire(wireName) {
            if (connections[wireName]) {
                connections[wireName].close();
                delete connections[wireName];
                const protocol = wireToProtocol[wireName];
                updateStatus(protocol);
            }
        }

        // Connect to all wires in a protocol
        function connectProtocol(protocolName, wires) {
            wires.forEach(wire => connectWire(wire, protocolName));
        }

        // Disconnect from all wires in a protocol
        function disconnectProtocol(wires) {
            wires.forEach(wire => disconnectWire(wire));
        }

        // Update signal display with new bit
        function updateSignal(wireName, value, timestamp) {
            if (!signalData[wireName]) return;

            signalData[wireName].push(value);

            if (signalData[wireName].length > maxSignalBits) {
                signalData[wireName].shift();
            }

            drawWaveform(wireName);
        }

        // Update frame count
        function updateFrameCount(wireName) {
            const countSpan = document.getElementById(`count-${wireName}`);
            if (countSpan) {
                const current = parseInt(countSpan.textContent) || 0;
                countSpan.textContent = current + 1;
            }
        }

        // Update protocol connection status
        function updateStatus(protocolName) {
            const statusBadge = document.getElementById(`status-${protocolName}`);
            if (!statusBadge) return;

            const wires = {
                '1wire': ['dq'],
                'spi': ['mosi', 'sck'],
                'i2c': ['sda', 'scl']
            }[protocolName] || [];

            const connectedCount = wires.filter(w => connections[w]).length;
            const isConnected = connectedCount > 0;

            statusBadge.className = `status-badge ${isConnected ? 'connected' : 'disconnected'}`;
            statusBadge.innerHTML = `<span class="status-dot"></span><span>${isConnected ? `Connected (${connectedCount}/${wires.length})` : 'Disconnected'}</span>`;
        }

        // Add message to log
        function addLog(protocolName, message) {
            const logDiv = document.getElementById(`log-${protocolName}`);
            if (!logDiv) return;

            const timestamp = new Date().toLocaleTimeString();
            const logEntry = document.createElement('div');
            logEntry.innerHTML = `<span class="timestamp">[${timestamp}]</span> ${message}`;
            
            logDiv.appendChild(logEntry);

            while (logDiv.children.length > maxLogMessages) {
                logDiv.removeChild(logDiv.firstChild);
            }

            logDiv.scrollTop = logDiv.scrollHeight;
        }

        // Clear signal display
        function clearSignal(wireName) {
            if (signalData[wireName]) {
                signalData[wireName] = [];
            }
            
            initCanvas(wireName);
            
            const countSpan = document.getElementById(`count-${wireName}`);
            if (countSpan) {
                countSpan.textContent = '0';
            }
        }

        // Clear protocol signals
        function clearProtocol(wires) {
            wires.forEach(wire => clearSignal(wire));
            const protocol = wireToProtocol[wires[0]];
            const logDiv = document.getElementById(`log-${protocol}`);
            if (logDiv) {
                logDiv.innerHTML = '';
            }
        }

        // Initialize canvases on page load
        window.addEventListener('load', () => {
            ['dq', 'mosi', 'sck', 'sda', 'scl'].forEach(wire => {
                initCanvas(wire);
                attachZoomHandler(wire);
            });
            
            // Auto-connect 1-Wire on initial load
            connectWire('dq', '1wire');
        });

        // Handle window resize
        window.addEventListener('resize', () => {
            ['dq', 'mosi', 'sck', 'sda', 'scl'].forEach(wire => {
                drawWaveform(wire);
            });
        });

        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            Object.keys(connections).forEach(wire => disconnectWire(wire));
        });
    