"""Mock data for scorecard tests."""

# Sample scorecard data based on API response
MOCK_SCORECARDS_DATA = [
    {
        "id": "sc_3cAtWg4HHCJkd8Dl",
        "identifier": "ProductionReadiness",
        "title": "Production Readiness",
        "levels": [
            {
                "color": "paleBlue",
                "title": "Basic"
            },
            {
                "color": "bronze",
                "title": "Bronze"
            },
            {
                "color": "silver",
                "title": "Silver"
            },
            {
                "color": "gold",
                "title": "Gold"
            }
        ],
        "blueprint": "service",
        "rules": [
            {
                "identifier": "hasReadme",
                "description": "Checks if the service has a readme file in the repository",
                "title": "Has a readme",
                "level": "Bronze",
                "query": {
                    "combinator": "and",
                    "conditions": [
                        {
                            "operator": "isNotEmpty",
                            "property": "readme"
                        }
                    ]
                }
            },
            {
                "identifier": "usesSupportedLang",
                "description": "Checks if the service uses one of the supported languages. ",
                "title": "Uses a supported language",
                "level": "Silver",
                "query": {
                    "combinator": "or",
                    "conditions": [
                        {
                            "operator": "=",
                            "property": "language",
                            "value": "Python"
                        },
                        {
                            "operator": "=",
                            "property": "language",
                            "value": "JavaScript"
                        },
                        {
                            "operator": "=",
                            "property": "language",
                            "value": "React"
                        },
                        {
                            "operator": "=",
                            "property": "language",
                            "value": "TypeScript"
                        }
                    ]
                }
            }
        ],
        "createdAt": "2024-06-05T19:38:17.772Z",
        "createdBy": "google-oauth2|116901613151982285771",
        "updatedAt": "2024-07-30T06:58:57.834Z",
        "updatedBy": "google-oauth2|116901613151982285771"
    },
    {
        "id": "sc_Hs7CpLG0Y3qj1CIx",
        "identifier": "configuration",
        "title": "Configuration Checks",
        "levels": [
            {
                "color": "paleBlue",
                "title": "Basic"
            },
            {
                "color": "bronze",
                "title": "Bronze"
            },
            {
                "color": "silver",
                "title": "Silver"
            },
            {
                "color": "gold",
                "title": "Gold"
            }
        ],
        "blueprint": "workload",
        "rules": [
            {
                "identifier": "notPrivileged",
                "level": "Bronze",
                "query": {
                    "combinator": "and",
                    "conditions": [
                        {
                            "operator": "!=",
                            "property": "hasPrivileged",
                            "value": True
                        }
                    ]
                },
                "title": "No privilged containers"
            },
            {
                "identifier": "hasLimits",
                "level": "Bronze",
                "query": {
                    "combinator": "and",
                    "conditions": [
                        {
                            "operator": "=",
                            "property": "hasLimits",
                            "value": True
                        }
                    ]
                },
                "title": "All containers have CPU and Memory limits"
            }
        ],
        "createdAt": "2024-08-01T06:31:35.062Z",
        "createdBy": "GiypjgSxnmNbFSldqkJuYrGHh1XHSREx",
        "updatedAt": "2024-08-01T06:31:35.062Z",
        "updatedBy": "GiypjgSxnmNbFSldqkJuYrGHh1XHSREx"
    },
    {
        "id": "sc_egymGQWQ0pBAcR06",
        "identifier": "DORA",
        "title": "DORA Metrics",
        "levels": [
            {
                "color": "paleBlue",
                "title": "Basic"
            },
            {
                "color": "bronze",
                "title": "Bronze"
            },
            {
                "color": "silver",
                "title": "Silver"
            },
            {
                "color": "gold",
                "title": "Gold"
            }
        ],
        "blueprint": "domain",
        "rules": [
            {
                "identifier": "DeploymentFrequency",
                "title": "Deployment Frequency > 3",
                "level": "Bronze",
                "query": {
                    "combinator": "and",
                    "conditions": [
                        {
                            "operator": ">",
                            "property": "deployment_frequency",
                            "value": 3
                        }
                    ]
                }
            }
        ],
        "createdAt": "2024-09-18T08:51:49.625Z",
        "createdBy": "google-oauth2|116901613151982285771",
        "updatedAt": "2024-09-18T08:51:49.625Z",
        "updatedBy": "google-oauth2|116901613151982285771"
    }
]

# Dictionary mapping scorecard identifiers to their data
MOCK_SCORECARD_DICT = {scorecard["identifier"]: scorecard for scorecard in MOCK_SCORECARDS_DATA} 