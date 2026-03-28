document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-search-btn');
    const homeBtn = document.getElementById('home-btn');
    
    // Sections
    const heroSection = document.getElementById('hero-section');
    const resultsSection = document.getElementById('results-section');
    const savedNichesSection = document.getElementById('saved-niches-section');
    
    // Grids
    const productGrid = document.getElementById('product-grid');
    const savedGrid = document.getElementById('saved-grid');
    
    // UI Elements
    const template = document.getElementById('product-card-template');
    const loadingSequence = document.getElementById('loading-sequence');
    const loadingText = document.getElementById('loading-text');
    const progressBar = document.getElementById('progress-bar');
    
    // Nav Items
    const navDashboard = document.getElementById('nav-dashboard');
    const navSavedNiches = document.getElementById('nav-saved-niches');
    const savedCount = document.getElementById('saved-count');

    // State Tracking
    let shownProductIds = new Set();
    const BATCH_SIZE = 25;
    
    // LocalStorage State
    let savedNiches = JSON.parse(localStorage.getItem('amazonBotSavedNiches')) || [];
    updateSavedCountUI();

    const processingSteps = [
        "Connecting to Amazon APIs globally...",
        "Scanning BSR (Best Sellers Rank) & Movers...",
        "Applying strict rules (>$40, Low Comp)...",
        "Analyzing search volume & profitability...",
        "Generating unique untracked batch..."
    ];

    // --- NAVIGATION LOGIC ---
    homeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        switchToDashboard();
        resultsSection.classList.add('hidden');
        heroSection.classList.remove('hidden');
        startBtn.style.display = 'block';
        loadingSequence.classList.add('hidden');
        productGrid.innerHTML = ''; 
    });

    navDashboard.addEventListener('click', (e) => {
        e.preventDefault();
        switchToDashboard();
        // Just show hero if results are empty, otherwise show results
        if (productGrid.innerHTML.trim() === '') {
            resultsSection.classList.add('hidden');
            heroSection.classList.remove('hidden');
            startBtn.style.display = 'block';
        } else {
            heroSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');
        }
    });

    navSavedNiches.addEventListener('click', (e) => {
        e.preventDefault();
        switchToSavedNiches();
        renderSavedItems();
    });

    function switchToDashboard() {
        navDashboard.classList.add('active');
        navSavedNiches.classList.remove('active');
        savedNichesSection.classList.add('hidden');
    }

    function switchToSavedNiches() {
        navSavedNiches.classList.add('active');
        navDashboard.classList.remove('active');
        heroSection.classList.add('hidden');
        resultsSection.classList.add('hidden');
        savedNichesSection.classList.remove('hidden');
    }

    // --- IDLE AGENT ANIMATION ---
    const idleTerminal = document.getElementById('idle-log-feed');
    if (idleTerminal) {
        const fakeLogs = [
            "<span class='system'>> [SCANNING] Movers & Shakers (UK .co.uk)...</span>",
            "<span class='alert'>> [FILTER] Removing 4,203 saturated niches...</span>",
            "<span class='success'>> [MATCH] Found Best Seller (DE .de) meeting 15% margin rule.</span>",
            "<span class='system'>> [SCANNING] New Releases (USA .com)...</span>",
            "<span class='alert'>> [FILTER] Discarding 891 electronics (Battery risk).</span>",
            "<span class='success'>> [MATCH] Verified Price Gap < $10 on 12 new niches.</span>"
        ];
        let logIndex = 0;
        setInterval(() => {
            const cursor = document.querySelector('.blinking-cursor');
            if(cursor) cursor.remove();
            
            idleTerminal.insertAdjacentHTML('beforeend', `<p class="log-line">${fakeLogs[logIndex]}</p><p class="log-line blinking-cursor">_</p>`);
            
            // Keep only last 4 lines to prevent overflow
            while(idleTerminal.children.length > 5) {
                idleTerminal.removeChild(idleTerminal.firstChild);
            }
            
            logIndex = (logIndex + 1) % fakeLogs.length;
        }, 3500);
    }

    // --- SEARCH LOGIC ---
    startBtn.addEventListener('click', () => {
        const availableProducts = window.mockProductsData.filter(p => !shownProductIds.has(p.id));
        
        if (availableProducts.length === 0) {
            alert("Bot Memory Exhausted: You have seen all available high-tier mock products! Refresh page to reset memory.");
            return;
        }

        startBtn.style.display = 'none';
        loadingSequence.classList.remove('hidden');
        
        let step = 0;
        let progress = 0;
        
        const interval = setInterval(() => {
            if (step < processingSteps.length) {
                loadingText.innerText = processingSteps[step];
                progress += (100 / processingSteps.length);
                progressBar.style.width = `${progress}%`;
                step++;
            } else {
                clearInterval(interval);
                setTimeout(() => revealResults(availableProducts), 400);
            }
        }, 400); 
    });

    // --- RENDERING CORE ---
    function renderProductCard(prod, containerElement, applyStagger = false, index = 0) {
        const clone = template.content.cloneNode(true);
        const card = clone.querySelector('.product-card');
        
        if (applyStagger) {
            card.style.animationDelay = `${(index % 10) * 0.1}s`;
        } else {
            card.style.animationDelay = `0s`; // Instantly show
        }
        
        // Populate standard content
        card.querySelector('.product-name').textContent = prod.name;
        
        // Make product name a clickable Amazon link
        const nameLink = card.querySelector('.product-name-link');
        if (nameLink) nameLink.href = prod.amazonLink;
        
        card.querySelector('.amazon-link').href = prod.amazonLink;
        card.querySelector('.est-price').textContent = prod.estPrice;
        card.querySelector('.why-wins').textContent = prod.whyWins;
        card.querySelector('.demand-signal').textContent = prod.demandSignal;
        card.querySelector('.competition-signal').textContent = prod.competitionSignal;
        card.querySelector('.profit-potential').textContent = prod.profitPotential;
        card.querySelector('.diff-angle').textContent = prod.diffAngle;
        card.querySelector('.main-risks').textContent = prod.mainRisks;
        card.querySelector('.seller-type strong').textContent = prod.sellerType;
        card.querySelector('.region-badge').textContent = prod.region;
        card.querySelector('.source-badge').textContent = prod.source;

        // Advanced Metrics
        if (card.querySelector('.weight-val')) {
            card.querySelector('.weight-val').textContent = prod.weight;
            card.querySelector('.trend-val').textContent = prod.trendType;
            card.querySelector('.monopoly-val').textContent = prod.monopolyRisk;
            card.querySelector('.price-val').textContent = prod.priceTrend;
            card.querySelector('.amz-val').textContent = prod.amazonBasics;
            card.querySelector('.cat-val').textContent = prod.categoryRisk;
            
            // New strict numerical metrics
            card.querySelector('.margin-val').textContent = prod.netMargin;
            card.querySelector('.reviews-val').textContent = prod.top10Reviews;
            card.querySelector('.gap-val').textContent = prod.priceGap;
            card.querySelector('.variation-val').textContent = prod.variationRisk;
        }

        // Save Button Logic
        const saveBtn = card.querySelector('.btn-save');
        
        // Initial state logic
        const isSaved = savedNiches.some(savedItem => savedItem.id === prod.id);
        if (isSaved) {
            saveBtn.classList.add('saved');
            saveBtn.innerHTML = '💔 Unsave';
        }

        saveBtn.addEventListener('click', () => {
            const currentlySaved = savedNiches.some(savedItem => savedItem.id === prod.id);
            if (currentlySaved) {
                // Remove from local storage array
                savedNiches = savedNiches.filter(item => item.id !== prod.id);
                saveBtn.classList.remove('saved');
                saveBtn.innerHTML = '❤️ Save';
                
                // If we are currently IN the saved view, remove the card from DOM instantly
                if (!savedNichesSection.classList.contains('hidden')) {
                    card.classList.add('hidden'); // or card.remove()
                    setTimeout(() => card.remove(), 200);
                }
            } else {
                // Add to local storage array
                savedNiches.push(prod);
                saveBtn.classList.add('saved');
                saveBtn.innerHTML = '💔 Unsave';
            }
            
            localStorage.setItem('amazonBotSavedNiches', JSON.stringify(savedNiches));
            updateSavedCountUI();
            
            // Sync any other visible identical cards
            syncSaveButtonsAcrossDOM(prod.id, !currentlySaved);
        });
        
        card.setAttribute('data-product-id', prod.id);
        containerElement.appendChild(clone);
    }

    function revealResults(availableProducts) {
        // Prevent regenerating if no memory left
        if (availableProducts.length === 0) {
            document.getElementById('generate-more-btn').classList.add('hidden');
            document.getElementById('exhausted-msg').classList.remove('hidden');
            return;
        }
        
        // Shuffle and Slice
        for (let i = availableProducts.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [availableProducts[i], availableProducts[j]] = [availableProducts[j], availableProducts[i]];
        }
        const batch = availableProducts.slice(0, BATCH_SIZE);
        batch.forEach(p => shownProductIds.add(p.id));

        heroSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');
        productGrid.innerHTML = '';
        
        batch.forEach((prod, index) => {
            renderProductCard(prod, productGrid, true, index);
        });
        
        setTimeout(() => {
            progressBar.style.width = '0%';
            loadingText.innerText = 'Connecting to Amazon API...';
        }, 1000);
        
        // Check if exhausted after this pull
        if (shownProductIds.size >= window.mockProductsData.length) {
            document.getElementById('generate-more-btn').classList.add('hidden');
            document.getElementById('exhausted-msg').classList.remove('hidden');
        } else {
            document.getElementById('generate-more-btn').classList.remove('hidden');
            document.getElementById('exhausted-msg').classList.add('hidden');
        }
    }

    // Wiring up Generate More Button
    const generateMoreBtn = document.getElementById('generate-more-btn');
    if (generateMoreBtn) {
        generateMoreBtn.addEventListener('click', () => {
            generateMoreBtn.innerText = 'Processing Database...';
            setTimeout(() => {
                const available = window.mockProductsData.filter(p => !shownProductIds.has(p.id));
                revealResults(available);
                generateMoreBtn.innerText = 'Generate More Products';
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }, 500);
        });
    }

    function renderSavedItems() {
        savedGrid.innerHTML = '';
        if (savedNiches.length === 0) {
            savedGrid.innerHTML = `<p style="grid-column: 1/-1; color: var(--text-muted);">You haven't saved any winning niches yet. Head back to the dashboard to find some!</p>`;
            return;
        }

        // Just reverse to show newest saves first
        const sortedSaves = [...savedNiches].reverse();
        sortedSaves.forEach(prod => {
            renderProductCard(prod, savedGrid, false);
        });
    }

    // Ensures that if a product is in BOTH the Results Grid and Saved Grid, toggling one updates the other visually
    function syncSaveButtonsAcrossDOM(productId, nowSaved) {
        const matchingCards = document.querySelectorAll(`.product-card[data-product-id="${productId}"]`);
        matchingCards.forEach(card => {
            const btn = card.querySelector('.btn-save');
            if (nowSaved) {
                btn.classList.add('saved');
                btn.innerHTML = '💔 Unsave';
            } else {
                btn.classList.remove('saved');
                btn.innerHTML = '❤️ Save';
            }
        });
    }

    function updateSavedCountUI() {
        savedCount.innerText = savedNiches.length;
    }
});
