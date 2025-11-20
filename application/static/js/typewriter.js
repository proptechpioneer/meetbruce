// Typewriter Animation - Separate Message Boxes
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - starting typewriter...');
    
    const messageElement = document.getElementById('typed-message');
    const ctaButtons = document.getElementById('cta-buttons');
    const chatContainer = document.getElementById('chat-container');
    
    if (messageElement && chatContainer) {
        // Hide the original message element since we'll create new boxes
        messageElement.style.display = 'none';
        
        // Remove any existing message bubbles from the template
        const existingBubbles = chatContainer.querySelectorAll('.flex.items-start.space-x-3.mb-6');
        existingBubbles.forEach(bubble => {
            if (!bubble.querySelector('#cta-buttons')) {
                bubble.remove();
            }
        });
        
        // Start typewriter immediately
        setTimeout(() => {
            console.log('Starting separate box typewriter...');
            
            // 📝 EDIT YOUR LINES HERE - Each line appears in its own box
            const lines = [
                "Did you know that most landlords have advanced software platforms to manage their properties",
                "These platforms help them efficiently manage every element of their property, collect the rent on time and get as much rent as possible",
                "Did you know there is no equivalent for tenants",
                "Until now...",
                "Hello! I'm Bruce the world's first AI-powered Tenant Advocate",
                "I help tenants navigate their relationship with their landlords",
                "On 1 May 2026, the Renters' Rights Act will become law in England",
                "This will be the biggest shake up of the English rental market in 40 years",
                "It gives you new powers to challenge unfair rental practices",
                "I'm on a mission to help drive rogue landlords from the market",
                "I can help you...",
                "Make sure your landlord is following the law",
                "Monitor landlords proposed rent increases to make sure you get the best deal",
                "Log and escalate repairs",
                "Help you understand your rights",
                "Ready to get started?",
                "Click 'Get Started' below to begin! 🚀"
            ];
            
            // ⚙️ TIMING SETTINGS
            const typingSpeed = 50;        // Speed of typing each character (lower = faster)
            const linePauseTime = 1200;    // Pause between lines (milliseconds)
            
            let currentLineIndex = 0;
            
            function createMessageBox(lineIndex) {
                // Create a new message box for this line
                const messageBox = document.createElement('div');
                messageBox.className = 'flex items-start space-x-3 mb-6';
                messageBox.innerHTML = `
                    <div class="bg-white rounded-2xl rounded-tl-sm shadow-sm p-6 max-w-3xl">
                        <div id="message-line-${lineIndex}" class="text-gray-800 text-lg leading-relaxed font-medium">
                            <!-- Text will be typed here -->
                        </div>
                    </div>
                `;
                
                // Add the message box to the chat container (before the CTA buttons)
                const ctaContainer = document.querySelector('.text-center.mt-8');
                if (ctaContainer) {
                    chatContainer.insertBefore(messageBox, ctaContainer);
                } else {
                    chatContainer.appendChild(messageBox);
                }
                
                // Scroll to show the new message box immediately with padding
                setTimeout(() => {
                    const containerHeight = chatContainer.clientHeight;
                    const scrollTarget = chatContainer.scrollHeight - containerHeight + 100; // 100px gap from bottom
                    chatContainer.scrollTo({
                        top: Math.max(0, scrollTarget),
                        behavior: 'smooth'
                    });
                }, 50);
                
                return document.getElementById(`message-line-${lineIndex}`);
            }
            
            function typeNextLine(lineIndex) {
                if (lineIndex >= lines.length) {
                    // All lines done - show buttons
                    if (ctaButtons) {
                        setTimeout(() => {
                            ctaButtons.style.display = 'block';
                            ctaButtons.classList.add('animate-fade-in');
                            console.log('All lines complete - buttons shown');
                        }, 500);
                    }
                    return;
                }
                
                const currentLine = lines[lineIndex];
                const lineElement = createMessageBox(lineIndex);
                
                let charIndex = 0;
                
                // Type the current line character by character
                function typeChar() {
                    if (charIndex < currentLine.length) {
                        lineElement.textContent += currentLine.charAt(charIndex);
                        charIndex++;
                        setTimeout(typeChar, typingSpeed);
                    } else {
                        // Line fully typed
                        console.log(`Line ${lineIndex + 1} complete: "${currentLine}"`);
                        
                        // Check if this is the final line
                        if (lineIndex === lines.length - 1) {
                            // Final line - show buttons after a pause and ensure they're visible
                            if (ctaButtons) {
                                setTimeout(() => {
                                    ctaButtons.style.display = 'block';
                                    ctaButtons.classList.add('animate-fade-in');
                                    console.log('Final line - showing buttons');
                                    
                                    // Scroll to ensure buttons are visible with padding
                                    setTimeout(() => {
                                        chatContainer.scrollTo({
                                            top: chatContainer.scrollHeight,
                                            behavior: 'smooth'
                                        });
                                    }, 200);
                                }, 1000);
                            }
                        } else {
                            // Move to next line after a pause
                            setTimeout(() => {
                                console.log(`Moving to line ${lineIndex + 2}`);
                                typeNextLine(lineIndex + 1);
                            }, linePauseTime);
                        }
                    }
                }
                
                typeChar();
            }
            
            // Start with the first line after a brief delay
            typeNextLine(0);
        }, 1000);
        
    } else {
        console.error('Could not find required elements!');
    }
});