# Test data for real estate analysis evaluation

WATERFRONT_RESIDENCE_DATA = {
    "unitData": {
        "address": "19-01, Waterfront Residences",
        "floor": 15,
        "stack": "A",
        "sqft": 1200,
        "config": "2 Bedroom",
        "orientation": "Unblocked water view"
    },
    "pricingData": {
        "currentListing": {
            "askingPrice": 2400000
        }
    },
    "projectData": {
        "name": "Waterfront Residences",
        "neighborhood": "Central District",
        "completionYear": 2010,
        "tenure": "Freehold",
        "amenities": [
            "Swimming Pool",
            "Gym",
            "BBQ Area"
        ],
        "pois": [
            {
                "name": "Central Station",
                "type": "METRO",
                "walkingDurationMins": 5
            },
            {
                "name": "Food Court Plaza",
                "type": "FOOD",
                "walkingDurationMins": 6
            }
        ]
    },
    "marketContext": {
        "competitiveListings": [
            {
                "sqft": 750,
                "askingPsf": 2100,
                "daysOnMarket": 25
            },
            {
                "sqft": 1210,
                "askingPsf": 2050,
                "daysOnMarket": 95
            },
            {
                "sqft": 780,
                "askingPsf": 2080,
                "daysOnMarket": 40
            }
        ],
        "pastTransactions": [
            {
                "sqft": 760,
                "transactedPsf": 2050,
                "saleDate": "2025-05-10"
            },
            {
                "sqft": 755,
                "transactedPsf": 2045,
                "saleDate": "2025-04-22"
            },
            {
                "sqft": 1200,
                "transactedPsf": 1990,
                "saleDate": "2025-02-15"
            }
        ]
    }
}

# Additional test scenarios for comprehensive evaluation
COMPACT_TOWERS_SCENARIO = {
    "unitData": {
        "address": "05-12, The Compact Towers",
        "floor": 5,
        "stack": "C",
        "sqft": 750,
        "config": "2 Bedroom",
        "orientation": "City view"
    },
    "pricingData": {
        "currentListing": {
            "askingPrice": 1600000
        }
    },
    "projectData": {
        "name": "The Compact Towers",
        "neighborhood": "Business District",
        "completionYear": 2009,
        "tenure": "99-year leasehold",
        "amenities": [
            "Sky Gardens",
            "Multi-purpose Hall"
        ],
        "pois": [
            {
                "name": "Business District Station",
                "type": "METRO",
                "walkingDurationMins": 3
            }
        ]
    },
    "marketContext": {
        "competitiveListings": [
            {
                "sqft": 760,
                "askingPsf": 2100,
                "daysOnMarket": 30
            },
            {
                "sqft": 755,
                "askingPsf": 2120,
                "daysOnMarket": 22
            },
            {
                "sqft": 1200,
                "askingPsf": 1950,
                "daysOnMarket": 120
            }
        ],
        "pastTransactions": [
            {
                "sqft": 750,
                "transactedPsf": 2080,
                "saleDate": "2025-06-15"
            },
            {
                "sqft": 765,
                "transactedPsf": 2090,
                "saleDate": "2025-05-20"
            }
        ]
    }
}

PREMIUM_TOWERS_SCENARIO = {
    "unitData": {
        "address": "25-01, Premium Towers",
        "floor": 25,
        "stack": "A",
        "sqft": 1500,
        "config": "3 Bedroom",
        "orientation": "Waterfront view"
    },
    "pricingData": {
        "currentListing": {
            "askingPrice": 3200000
        }
    },
    "projectData": {
        "name": "Premium Towers",
        "neighborhood": "Financial District",
        "completionYear": 2008,
        "tenure": "Freehold",
        "amenities": [
            "Infinity Pool",
            "Private Dining",
            "Concierge Service"
        ],
        "pois": [
            {
                "name": "Financial District Station",
                "type": "METRO",
                "walkingDurationMins": 2
            },
            {
                "name": "Riverside Entertainment",
                "type": "ENTERTAINMENT",
                "walkingDurationMins": 8
            }
        ]
    },
    "marketContext": {
        "competitiveListings": [
            {
                "sqft": 750,
                "askingPsf": 2200,
                "daysOnMarket": 18
            },
            {
                "sqft": 800,
                "askingPsf": 2180,
                "daysOnMarket": 25
            },
            {
                "sqft": 1480,
                "askingPsf": 2100,
                "daysOnMarket": 150
            }
        ],
        "pastTransactions": [
            {
                "sqft": 780,
                "transactedPsf": 2150,
                "saleDate": "2025-07-01"
            },
            {
                "sqft": 1520,
                "transactedPsf": 2000,
                "saleDate": "2025-03-10"
            }
        ]
    }
}

# Maintain backward compatibility with old variable names
MARINA_BAY_DATA = WATERFRONT_RESIDENCE_DATA
YIELD_INVESTOR_SCENARIO = COMPACT_TOWERS_SCENARIO  
LEGACY_BUYER_SCENARIO = PREMIUM_TOWERS_SCENARIO
