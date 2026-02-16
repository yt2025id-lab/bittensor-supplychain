# AI Supply Chain Demo Video Script

**Duration:** 5-7 minutes

---

## Scene 1: Opening (0:00-0:30)
- [Visual] Project logo with logistics theme (blue/orange). Animated globe with shipping routes. Container ships and trucks.
- [Voice Over] "Welcome to AI Supply Chain Subnet - the decentralized platform for real-time logistics intelligence and disruption prediction, powered by Bittensor. Making global supply chains smarter, together."

## Scene 2: The Problem (0:30-1:00)
- [Visual] News clips: Suez Canal blockage, COVID supply chain chaos, empty shelves. Statistics overlay: "$184B+ annual losses".
- [Voice Over] "Supply chain disruptions cost the global economy over $184 billion every year. From the Suez Canal blockage to COVID-19, we've seen how fragile centralized supply chains are. Data is siloed across manufacturers, shippers, and retailers. Predictions are opaque, and small businesses are left blind."

## Scene 3: The Solution (1:00-1:45)
- [Visual] Animated network of IoT sensors, warehouses, trucks, ships connected by Bittensor nodes. $TAO tokens flowing.
- [Voice Over] "Our solution: a Bittensor subnet that creates a decentralized supply chain oracle. Miners aggregate data from IoT sensors, ERP systems, and shipping APIs to predict delivery times and disruption risks. Validators verify predictions against real outcomes. Accurate predictions earn $TAO rewards, and all data is transparent on-chain."

## Scene 4: Mechanism Design Deep Dive (1:45-3:00)
- [Visual] Animated diagram:
  1. User submits tracking query
  2. Miners aggregate IoT/ERP data and predict
  3. Validators compare predictions to actual outcomes
  4. Scores computed
  5. Rewards distributed
- [Voice Over] "Here's how it works. A user submits a supply chain query - tracking a shipment from Shanghai to Los Angeles. Miners tap into IoT sensors, shipping APIs, and weather data to predict delivery time and disruption risk. Validators compare these predictions against actual shipment outcomes over time. The most accurate miners earn the highest rewards."
- [Visual] Show scoring formula: `Score = 0.5 * PredictionAccuracy + 0.3 * DataFreshness + 0.2 * Coverage`

## Scene 5: Live Demo (3:00-5:00)
- [Visual] Screen recording:
  1. Terminal: `uvicorn main:app --reload`
  2. Open browser/Postman: POST to `/track`
  3. Show JSON request: `{"product": "Electronics", "origin": "Shanghai", "destination": "Los Angeles"}`
  4. Show JSON response with status, prediction, risk_score, recommendation
  5. (Optional) Show dashboard with real-time tracking visualization
- [Voice Over] "Let's see it in action. We start our API, submit a tracking query for electronics shipping from Shanghai to LA. Within seconds, we receive a real-time status, predicted delivery date, disruption risk score, and route optimization recommendations. In production, multiple miners compete to provide the most accurate predictions."

## Scene 6: Go-to-Market & Impact (5:00-6:00)
- [Visual] GTM roadmap. Partner logos (e-commerce, 3PL). Market stats.
- [Voice Over] "We start by partnering with e-commerce platforms and third-party logistics providers who need real-time data. Then we expand to ERP integrations for enterprises using SAP and Oracle. The supply chain analytics market is $22 billion and growing rapidly as companies prioritize resilience."

## Scene 7: Closing & Call to Action (6:00-7:00)
- [Visual] Team info, social links, project logo. "Join Us" call to action.
- [Voice Over] "AI Supply Chain Subnet - bringing decentralized intelligence to global logistics. Join us in building supply chains that are transparent, predictive, and resilient."

---
**Production Tips:**
- Use blue/orange industrial color scheme throughout.
- Include real-world supply chain disruption footage (royalty-free) for impact.
- Background music: dynamic, professional, industrial ambient.
- Voice should be energetic, confident, and data-driven.
