// mockData.js
// A robust database of 50 highly detailed, rule-compliant winning products.

function generateMetrics() {
  const weight = (Math.random() * 4.5 + 0.2).toFixed(1); // 0.2kg to 4.7kg (Strictly < 5kg)
  const monopolyShare = Math.floor(Math.random() * 48) + 12; // 12% to 60% (Strictly < 63%)
  const margin = Math.floor(Math.random() * 25) + 15; // 15% to 40% margin
  const reviews = Math.floor(Math.random() * 250) + 40; // 40 to 290 reviews
  const gap = Math.floor(Math.random() * 5) + 5; // $5 to $10 gap
  return {
    weight: `${weight} kg`,
    priceTrend: "Stable (No Price Wars)",
    trendType: "Evergreen (5Y verified)",
    amazonBasics: "False",
    monopolyRisk: `Top Brand: ${monopolyShare}%`,
    categoryRisk: "Safe (Non-Restricted)",
    netMargin: `${margin}% Net Margin`,
    top10Reviews: `Top 10: < ${reviews} Rev`,
    priceGap: `Gap: $${gap}`,
    variationRisk: "None (No Sizes/Colors)"
  };
}

window.mockProductsData = [
  {
    id: 1, region: "🇺🇸 US (.com)", source: "🌟 New Release",
    name: "Smart Heated Pet House with App Control", amazonLink: "https://www.amazon.com/s?k=smart+heated+pet+house",
    estPrice: "$89.99", whyWins: "Rising trend in premium pet care tech. High margin item not yet dominated by single mega-brands.",
    demandSignal: "Growing 45% YoY", competitionSignal: "Low (Sub 200 Avg Reviews)", profitPotential: "High (~42% ROI after FBA)",
    diffAngle: "Add a removable plush insert and bundle with an outdoor safe extension cord.", mainRisks: "Electronic safety compliance required.", sellerType: "Intermediate",
    ...generateMetrics()
  },
  {
    id: 2, region: "🇬🇧 UK (.co.uk)", source: "📈 Movers & Shakers",
    name: "Portable Travel Espresso Maker Kit", amazonLink: "https://www.amazon.co.uk/s?k=portable+espresso+maker",
    estPrice: "£65.00", whyWins: "Massive coffee niche demand hyper-focused on 'travel/camping'.",
    demandSignal: "Stable High Volume Search", competitionSignal: "Medium-Low (Market fragmentation)", profitPotential: "Medium-High (~35% margin)",
    diffAngle: "Bundle with a hard-shell protective travel case and premium metal tamper.", mainRisks: "Quality Control is vital to avoid leaks.", sellerType: "Intermediate",
    ...generateMetrics()
  },
  {
    id: 3, region: "🇩🇪 DE (.de)", source: "🥇 Best Seller",
    name: "Ergonomic Split Keyboard Wrist Rest", amazonLink: "https://www.amazon.de/s?k=ergonomic+wrist+rest",
    estPrice: "€45.99", whyWins: "Combines two WFH niches into a unique hybrid product with low sourcing cost.",
    demandSignal: "Very High Search Volume", competitionSignal: "Very Low (No direct hybrid competitors)", profitPotential: "Very High (~50% margin)",
    diffAngle: "Use premium memory foam and sustainable walnut wood.", mainRisks: "Easily copied once successful; branding must be superior.", sellerType: "Beginner",
    ...generateMetrics()
  },
  {
    id: 4, region: "🇨🇦 CA (.ca)", source: "🌟 New Release",
    name: "Hydroponic Microgreens Growing Kit with LED", amazonLink: "https://www.amazon.ca/s?k=hydroponic+microgreens+kit",
    estPrice: "$70.00", whyWins: "Hits the price sweet-spot for giftability with strong profit margins built-in.",
    demandSignal: "Consistent Upward Trend", competitionSignal: "Medium (Dominated by poor quality imports)", profitPotential: "High (~38% margin)",
    diffAngle: "Aesthetic modern-matte design instead of gloss white plastic.", mainRisks: "Oversized shipping costs if not functionally flat-packed.", sellerType: "Advanced",
    ...generateMetrics()
  },
  {
    id: 5, region: "🇦🇺 AU (.com.au)", source: "📈 Movers & Shakers",
    name: "Aesthetic Bamboo Laundry Basket with Wheels", amazonLink: "https://www.amazon.com.au/s?k=bamboo+laundry+basket+wheels",
    estPrice: "$85.00", whyWins: "Basic household item upgraded for premium home decor buyers.",
    demandSignal: "Surging local demand for aesthetic home goods", competitionSignal: "Low (Most competitors are cheap plastic)", profitPotential: "High (~45% Margin)",
    diffAngle: "Include an odor-absorbing carbon liner and smooth-glide silicone wheels.", mainRisks: "Shipping volume metrics (dimensional weight).", sellerType: "Beginner",
    ...generateMetrics()
  },
  {
    id: 6, region: "🇺🇸 US (.com)", source: "🥇 Best Seller",
    name: "Foldable Portable Solar Charger Station (100W)", amazonLink: "https://www.amazon.com/s?k=foldable+portable+solar+charger",
    estPrice: "$120.00", whyWins: "Capitalizes on Vanlife and emergency prep trends with high ticket pricing.",
    demandSignal: "Excellent Year-Round Baseline", competitionSignal: "Medium-High, but lacks aesthetic brands", profitPotential: "Very High ($40+ net profit per unit)",
    diffAngle: "Use waterproof ETFE lamination and military-grade fabric cases.", mainRisks: "High initial sourcing cost; electronic failure rates.", sellerType: "Advanced",
    ...generateMetrics()
  },
  {
    id: 7, region: "🇬🇧 UK (.co.uk)", source: "🌟 New Release",
    name: "Invisible Mini Sleep Earbuds (Side-Sleeper)", amazonLink: "https://www.amazon.co.uk/s?k=invisible+mini+sleep+earbuds",
    estPrice: "£55.00", whyWins: "Solves a painful, specific problem (snoring partners) where standard AirPods hurt.",
    demandSignal: "Massive evergreen demand", competitionSignal: "Low for specialized 'side-sleeper' ultra-thin models", profitPotential: "High (Small size = cheap shipping & FBA fees)",
    diffAngle: "Bundle with a soothing white-noise app or premium silk sleep mask.", mainRisks: "Battery life limits in micro-sized tech.", sellerType: "Intermediate",
    ...generateMetrics()
  },
  {
    id: 8, region: "🇩🇪 DE (.de)", source: "📈 Movers & Shakers",
    name: "Smart Posture Corrector with Biofeedback Vibration", amazonLink: "https://www.amazon.de/s?k=smart+posture+corrector",
    estPrice: "€49.99", whyWins: "Traditional correctors are saturated, but 'smart' tech alternatives are rising rapidly.",
    demandSignal: "High sustained awareness", competitionSignal: "Low in the 'Tech/Biofeedback' sub-niche", profitPotential: "Excellent (~60% ROI)",
    diffAngle: "Ensure the strap uses hypoallergenic, breathable mesh (competitors use cheap neoprene).", mainRisks: "Customer returns if the app integration is buggy.", sellerType: "Beginner",
    ...generateMetrics()
  },
  {
    id: 9, region: "🇨🇦 CA (.ca)", source: "🥇 Best Seller",
    name: "Dog Stairs for Car SUV (Heavy Duty)", amazonLink: "https://www.amazon.ca/s?k=dog+stairs+for+suv",
    estPrice: "$110.00", whyWins: "Pet parents will spend highly for their older dogs' joint health.",
    demandSignal: "Extremely stable all year", competitionSignal: "Medium, but clear gap for lightweight aluminum models", profitPotential: "High (Sold for $110, sourced for $25)",
    diffAngle: "Use aerospace aluminum to cut weight in half compared to steel competitors.", mainRisks: "Must hold up to 150lbs; structural failure is a major liability.", sellerType: "Intermediate",
    ...generateMetrics()
  },
  {
    id: 10, region: "🇦🇺 AU (.com.au)", source: "🌟 New Release",
    name: "5-in-1 Automated Makeup Brush Cleaner Machine", amazonLink: "https://www.amazon.com.au/s?k=automated+makeup+brush+cleaner",
    estPrice: "$45.00", whyWins: "Highly viral on TikTok and Instagram; visual transformation sells easily.",
    demandSignal: "Excellent year-round stable demand", competitionSignal: "Medium (but many poor ratings to capitalize on)", profitPotential: "High (Small footprint, cheap FBA)",
    diffAngle: "Include a UV-C sanitizing light feature to destroy bacteria outperforming basic spinners.", mainRisks: "Fad-risk; must build a brand quickly around it.", sellerType: "Beginner",
    ...generateMetrics()
  },
];

const categories = ['Home Gym', 'Kitchen', 'Pet Supplies', 'Office', 'Smart Home', 'Outdoor', 'Decor', 'Travel', 'Gardening'];
const adjectives = ['Premium', 'Foldable', 'Ergonomic', 'Smart', 'Sustainable', 'Heavy-Duty', 'Aesthetic', 'Compact', 'Minimalist', 'Bamboo'];
const nouns = ['Organizer', 'Station', 'Kit', 'Monitor', 'Purifier', 'Blender', 'Carrier', 'Stand', 'Holder', 'Display'];
const regions = ['🇺🇸 US (.com)', '🇬🇧 UK (.co.uk)', '🇩🇪 DE (.de)', '🇨🇦 CA (.ca)', '🇦🇺 AU (.com.au)', '🇮🇹 IT (.it)'];
const sources = ['🌟 New Release', '📈 Movers & Shakers', '🥇 Best Seller'];
const risks = ['Shipping volume', 'Copycat competitors', 'High sourcing cost', 'Fragile materials', 'Quality Control demands', 'Packaging damage'];

for (let i = 11; i <= 150; i++) {
  let adj = adjectives[Math.floor(Math.random() * adjectives.length)];
  let noun = nouns[Math.floor(Math.random() * nouns.length)];
  let cat = categories[Math.floor(Math.random() * categories.length)];
  
  let priceBase = Math.floor(Math.random() * 310) + 40; // 40 to 350
  let estPrice = `$${priceBase}.99`;

  window.mockProductsData.push({
    id: i,
    region: regions[Math.floor(Math.random() * regions.length)],
    source: sources[Math.floor(Math.random() * sources.length)],
    name: `${adj} ${cat} ${noun} Bundle`,
    amazonLink: `https://www.amazon.com/s?k=${adj.toLowerCase()}+${cat.toLowerCase().replace(' ', '+')}+${noun.toLowerCase()}`,
    estPrice: estPrice,
    whyWins: `Capitalizes on the evergreen ${cat} market by solving specific user pain points present in top competitor reviews.`,
    demandSignal: `Solid year-round baseline with ${Math.floor(Math.random()*30)+20}% YoY growth`,
    competitionSignal: `Low to Medium`,
    profitPotential: `Strong`,
    diffAngle: `Improve the packaging and include a high-value accessory to instantly stand out from generic listings.`,
    mainRisks: risks[Math.floor(Math.random() * risks.length)],
    sellerType: (Math.random() > 0.5) ? "Beginner" : "Intermediate",
    ...generateMetrics()
  });
}
