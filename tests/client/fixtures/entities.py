"""Mock data for entity tests."""

# Sample mock data based on actual responses but with generic data
MOCK_ENTITIES_DATA = {
    "service": [
        {
            "identifier": "svc-001",
            "title": "Payment Processing Service",
            "blueprint": "service",
            "icon": "Server",
            "properties": {
                "team": "Platform",
                "url": "https://payments.internal.example",
                "healthStatus": "Healthy",
                "language": "Java"
            },
            "relations": {
                "deployments": ["dep-001", "dep-002"],
                "dependencies": ["svc-002"]
            },
            "team": ["Platform"],
            "createdAt": "2024-01-15T08:30:00.000Z",
            "createdBy": "user|abc123",
            "updatedAt": "2024-03-01T14:15:00.000Z",
            "updatedBy": "user|abc123"
        },
        {
            "identifier": "svc-002",
            "title": "User Management Service",
            "blueprint": "service",
            "icon": "Users",
            "properties": {
                "team": "Identity",
                "url": "https://users.internal.example",
                "healthStatus": "Healthy",
                "language": "TypeScript"
            },
            "relations": {
                "deployments": ["dep-003"],
                "dependencies": []
            },
            "team": ["Identity"],
            "createdAt": "2024-01-10T10:00:00.000Z",
            "createdBy": "user|xyz789",
            "updatedAt": "2024-02-28T16:45:00.000Z",
            "updatedBy": "user|xyz789"
        }
    ],
    "deployment": [
        {
            "identifier": "dep-001",
            "title": "Payment Service Production",
            "blueprint": "deployment",
            "icon": "Cloud",
            "properties": {
                "version": "2.4.1",
                "environment": "Production",
                "cluster": "cluster-east-1",
                "replicas": 5,
                "deployedAt": "2024-03-01T12:00:00.000Z"
            },
            "relations": {
                "service": "svc-001",
                "components": ["comp-001", "comp-002"]
            },
            "createdAt": "2024-03-01T12:00:00.000Z",
            "createdBy": "user|abc123",
            "updatedAt": "2024-03-01T12:00:00.000Z",
            "updatedBy": "user|abc123"
        }
    ],
    "component": [
        {
            "identifier": "comp-001",
            "title": "Payment Processor",
            "blueprint": "component",
            "icon": "Component",
            "properties": {
                "type": "API",
                "language": "Java",
                "repository": "https://github.com/example/payment-processor",
                "owner": "platform-team@example.com"
            },
            "relations": {
                "service": "svc-001",
                "dependencies": ["comp-002"]
            },
            "createdAt": "2024-01-15T08:30:00.000Z",
            "createdBy": "user|abc123",
            "updatedAt": "2024-03-01T14:15:00.000Z",
            "updatedBy": "user|abc123"
        }
    ]
} 