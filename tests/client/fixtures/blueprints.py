"""Mock data for blueprint tests."""

# Sample mock data based on actual responses
MOCK_BLUEPRINTS_DATA = [
    {
        "identifier": "service",
        "title": "Service",
        "description": "A microservice deployed in our platform",
        "icon": "Cloud",
        "createdAt": "2023-06-15T14:21:33.456Z",
        "createdBy": "google-oauth2|104372024031887754721",
        "updatedAt": "2023-09-28T08:17:45.123Z",
        "updatedBy": "google-oauth2|104372024031887754721",
        "schema": {
            "properties": {
                "team": {
                    "type": "string",
                    "title": "Team",
                    "icon": "Team",
                    "enum": [
                        "Backend",
                        "Frontend",
                        "DevOps",
                        "Data"
                    ],
                    "enumColors": {
                        "Backend": "blue",
                        "Frontend": "green",
                        "DevOps": "purple",
                        "Data": "yellow"
                    }
                },
                "url": {
                    "type": "string",
                    "title": "Service URL",
                    "format": "url",
                    "icon": "Link"
                },
                "healthStatus": {
                    "type": "string",
                    "title": "Health Status",
                    "default": "Healthy",
                    "enum": [
                        "Healthy",
                        "Degraded",
                        "Down"
                    ],
                    "enumColors": {
                        "Healthy": "green",
                        "Degraded": "yellow",
                        "Down": "red"
                    }
                },
                "language": {
                    "type": "string",
                    "title": "Language",
                    "enum": [
                        "TypeScript",
                        "Python",
                        "Java",
                        "Go"
                    ]
                }
            },
            "required": [
                "team",
                "healthStatus"
            ]
        },
        "relations": {
            "deployments": {
                "title": "Deployments",
                "target": "deployment",
                "required": False,
                "many": True
            },
            "dependencies": {
                "title": "Dependencies",
                "target": "service",
                "required": False,
                "many": True
            }
        }
    },
    {
        "identifier": "deployment",
        "title": "Deployment",
        "description": "A deployment of a service in our Kubernetes cluster",
        "icon": "Package",
        "createdAt": "2023-06-17T09:42:18.789Z",
        "createdBy": "google-oauth2|104372024031887754721",
        "updatedAt": "2023-10-05T11:23:56.432Z",
        "updatedBy": "google-oauth2|104372024031887754721",
        "schema": {
            "properties": {
                "version": {
                    "type": "string",
                    "title": "Version",
                    "icon": "Tag"
                },
                "environment": {
                    "type": "string",
                    "title": "Environment",
                    "default": "Development",
                    "enum": [
                        "Development",
                        "Staging",
                        "Production"
                    ],
                    "enumColors": {
                        "Development": "blue",
                        "Staging": "yellow",
                        "Production": "green"
                    }
                },
                "cluster": {
                    "type": "string",
                    "title": "Cluster",
                    "enum": [
                        "us-west",
                        "us-east",
                        "eu-central"
                    ]
                },
                "replicas": {
                    "type": "number",
                    "title": "Replicas",
                    "default": 1
                },
                "deployedAt": {
                    "type": "string",
                    "format": "date-time",
                    "title": "Deployed At"
                }
            },
            "required": [
                "version",
                "environment",
                "cluster"
            ]
        },
        "relations": {
            "service": {
                "title": "Service",
                "target": "service",
                "required": True,
                "many": False
            },
            "components": {
                "title": "Components",
                "target": "component",
                "required": False,
                "many": True
            }
        }
    },
    {
        "identifier": "component",
        "title": "Component",
        "description": "A software component that makes up a service",
        "icon": "Puzzle",
        "createdAt": "2023-07-22T16:31:29.654Z",
        "createdBy": "google-oauth2|104372024031887754721",
        "updatedAt": "2023-11-12T13:45:09.876Z",
        "updatedBy": "google-oauth2|104372024031887754721",
        "schema": {
            "properties": {
                "type": {
                    "type": "string",
                    "title": "Type",
                    "enum": [
                        "UI",
                        "API",
                        "Database",
                        "Cache",
                        "Queue"
                    ],
                    "enumColors": {
                        "UI": "green",
                        "API": "blue",
                        "Database": "purple",
                        "Cache": "orange",
                        "Queue": "teal"
                    }
                },
                "language": {
                    "type": "string",
                    "title": "Language",
                    "enum": [
                        "TypeScript",
                        "Python",
                        "Java",
                        "Go",
                        "C#",
                        "Ruby"
                    ]
                },
                "repository": {
                    "type": "string",
                    "title": "Repository",
                    "format": "url",
                    "icon": "Github"
                },
                "owner": {
                    "type": "string",
                    "title": "Owner",
                    "format": "user"
                }
            },
            "required": [
                "type",
                "language"
            ]
        },
        "relations": {
            "service": {
                "title": "Service",
                "target": "service",
                "required": True,
                "many": False
            },
            "dependencies": {
                "title": "Dependencies",
                "target": "component",
                "required": False,
                "many": True
            }
        }
    }
] 