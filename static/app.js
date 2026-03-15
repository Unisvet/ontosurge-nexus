document.addEventListener('DOMContentLoaded', () => {
    const causalSlider = document.getElementById('causal_adherence');
    const ethicalSlider = document.getElementById('ethical_consistency');
    const causalVal = document.getElementById('causal_val');
    const ethicalVal = document.getElementById('ethical_val');
    const causalWarning = document.getElementById('qnf_warning_causal');
    const ethicalWarning = document.getElementById('qnf_warning_ethical');
    const renderBtn = document.getElementById('renderBtn');
    
    // Output fields
    const qnfStatus = document.getElementById('qnf_status');
    const naiScore = document.getElementById('nai_score');
    const impactAnalysis = document.getElementById('impact_analysis');
    const realityRender = document.getElementById('reality_render');
    const loading = document.getElementById('loading');
    
    // Visualization Controls
    const visualizeBtn = document.getElementById('visualizeBtn');
    const visualizeLoading = document.getElementById('visualizeLoading');
    const visualizeContainer = document.getElementById('visualizeContainer');
    const visualizedImage = document.getElementById('visualizedImage');
    const downloadImageBtn = document.getElementById('downloadImageBtn');
    
    // Forge Entity Controls
    const forgeEntityBtn = document.getElementById('forgeEntityBtn');
    const forgeLoading = document.getElementById('forgeLoading');
    const targetEntityInput = document.getElementById('target_entity');

    // Update Slider UI
    function updateSliders() {
        causalVal.textContent = causalSlider.value;
        ethicalVal.textContent = ethicalSlider.value;

        // Visual warning for Quantum Narrative Fluctuations (below 0.3 weight per Constitution)
        causalWarning.style.display = parseFloat(causalSlider.value) < 0.3 ? 'block' : 'none';
        ethicalWarning.style.display = parseFloat(ethicalSlider.value) < 0.3 ? 'block' : 'none';
    }

    causalSlider.addEventListener('input', updateSliders);
    ethicalSlider.addEventListener('input', updateSliders);

    // Forge New Entity Request
    forgeEntityBtn.addEventListener('click', async () => {
        const description = prompt("Enter a description for the Entity Forge (e.g., 'A rogue AI in a cyberpunk city'):");
        if (!description) return;
        
        forgeLoading.style.display = 'block';
        forgeEntityBtn.disabled = true;
        
        try {
            const response = await fetch('/api/v1/generate_entity', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ description })
            });
            const data = await response.json();
            
            if (data.name) {
                targetEntityInput.value = data.name;
                causalSlider.value = data.baseline_causal_adherence || 0.8;
                ethicalSlider.value = data.baseline_ethical_consistency || 0.8;
                updateSliders();
                
                realityRender.textContent = `=== [ NEW ENTITY FORGED ] ===\\n\\nName: ${data.name}\\nBackground: ${data.background}\\n\\nEntity is awaiting gravitational inversion...`;
                impactAnalysis.textContent = '';
                qnfStatus.textContent = 'STABLE';
                qnfStatus.style.color = 'var(--accent)';
                naiScore.textContent = '0.0';
            } else {
                alert("Failed to forge entity. See console for details.");
                console.error("Forge Error:", data);
            }
        } catch (e) {
            console.error(e);
            alert("Error connecting to Entity Forge.");
        } finally {
            forgeLoading.style.display = 'none';
            forgeEntityBtn.disabled = false;
        }
    });

    // Initiate Gravity Inversion Request
    renderBtn.addEventListener('click', async () => {
        const targetEntity = document.getElementById('target_entity').value;
        const action = document.getElementById('action').value;
        const causalStr = `causal_adherence: ${causalSlider.value}`;
        const ethicalStr = `ethical_consistency: ${ethicalSlider.value}`;

        // Reset UI
        impactAnalysis.textContent = '';
        realityRender.textContent = '';
        qnfStatus.textContent = 'PENDING';
        qnfStatus.style.color = 'var(--accent)';
        naiScore.textContent = '0.0';
        loading.style.display = 'block';
        renderBtn.disabled = true;

        visualizeContainer.style.display = 'none';
        visualizeLoading.style.display = 'block'; // Start loading background image immediately
        visualizeBtn.style.display = 'none'; // Hide manual button

        try {
            const response = await fetch('/api/v1/manipulate_reality', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    target_entity: targetEntity,
                    action: action,
                    dial_adjustments: {
                        "causal_adherence": parseFloat(causalSlider.value),
                        "ethical_consistency": parseFloat(ethicalSlider.value)
                    },
                    session_id: "demo_architect_01"
                })
            });

            if (!response.ok) {
                throw new Error(`Server returned ${response.status}`);
            }

            // Handle the Server-Sent Event text stream parsing
            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let buffer = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                buffer += decoder.decode(value, { stream: true });
                let chunks = buffer.split('\n\n');
                buffer = chunks.pop(); // keep the last partial chunk in buffer

                for (let chunk of chunks) {
                    chunk = chunk.trim();
                    if (chunk === '') continue;
                    if (chunk.startsWith('data: ')) {
                        try {
                            const eventData = JSON.parse(chunk.substring(6));
                            
                            if (eventData.type === 'root_update') {
                                if (eventData.data.qnf_triggered !== undefined) {
                                    qnfStatus.textContent = eventData.data.qnf_triggered ? "ACTIVE (⚠)" : "STABLE";
                                    qnfStatus.style.color = eventData.data.qnf_triggered ? "var(--warning)" : "var(--accent)";
                                }
                                if (eventData.data.nai_dissonance_score !== undefined) {
                                    naiScore.textContent = eventData.data.nai_dissonance_score.toFixed(2);
                                }
                                if (eventData.data.impact_analysis !== undefined) {
                                    impactAnalysis.textContent = eventData.data.impact_analysis;
                                }
                            } else if (eventData.type === 'env_chunk') {
                                let formattedData = eventData.data.replace(/===\[ ENVIRONMENT RENDER \]===/g, '<br><br><span style="color: var(--accent); font-weight: bold; font-family: \'Orbitron\', sans-serif;">===[ ENVIRONMENT RENDER ]===</span><br>');
                                formattedData = formattedData.replace(/\\n/g, '<br>').replace(/\n/g, '<br>'); // Render both explicit text breaks and actual newline control bytes
                                realityRender.innerHTML += formattedData;
                            } else if (eventData.type === 'char_chunk') {
                                let formattedData = eventData.data.replace(/===\[ ENTITY SUBCONSCIOUS \]===/g, '<br><br><span style="color: var(--accent); font-weight: bold; font-family: \'Orbitron\', sans-serif;">===[ ENTITY SUBCONSCIOUS ]===</span><br>');
                                formattedData = formattedData.replace(/\\n/g, '<br>').replace(/\n/g, '<br>'); // Render both explicit text breaks and actual newline control bytes
                                realityRender.innerHTML += formattedData;
                            } else if (eventData.type === 'error') {
                                realityRender.innerHTML += "<br><br><span style='color: var(--warning);'>[Nexus Error]: " + eventData.data + "</span>";
                                if (eventData.data.includes("Background image")) {
                                    visualizeLoading.style.display = 'none';
                                    visualizeBtn.style.display = 'block'; // Show button again so they can manually retry
                                }
                            } else if (eventData.type === 'image_url') {
                                visualizedImage.src = eventData.data;
                                downloadImageBtn.href = eventData.data;
                                visualizeContainer.style.display = 'block';
                                visualizeLoading.style.display = 'none';
                            }
                        } catch (e) {
                            console.error("Error parsing SSE chunk:", chunk, e);
                        }
                    }
                }
            }

        } catch (error) {
            console.error("Fetch Error:", error);
            realityRender.textContent = "Connection to Ontosurge Core lost.";
        } finally {
            loading.style.display = 'none';
            renderBtn.disabled = false;
            visualizeLoading.style.display = 'none'; // Stop loading if stream terminates or fails
        }
    });

    // Request Visual Manifestation (Image Gen)
    visualizeBtn.addEventListener('click', async () => {
        const environmentText = realityRender.textContent;
        if (!environmentText) return;
        
        visualizeLoading.style.display = 'block';
        visualizeBtn.disabled = true;
        visualizeContainer.style.display = 'none';
        
        try {
            const response = await fetch('/api/v1/visualize_space', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ environment_text: environmentText })
            });
            const data = await response.json();
            
            if (data.image_url) {
                visualizedImage.src = data.image_url;
                downloadImageBtn.href = data.image_url;
                visualizeContainer.style.display = 'block';
            } else {
                alert("Failed to synthesize visual manifestation. Check terminal logs.");
                console.error("Visualize Error:", data);
            }
        } catch (e) {
            console.error(e);
            alert("Connection error to Visual Synthesizer.");
        } finally {
            visualizeLoading.style.display = 'none';
            visualizeBtn.disabled = false;
        }
    });
});
