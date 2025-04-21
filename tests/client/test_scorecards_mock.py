import pytest
import sys

# Add the src directory to the path so we can import our modules
sys.path.append('src')

from src.mcp_server_port.models.scorecards import PortScorecardList, PortScorecard
from .fixtures.scorecards import MOCK_SCORECARDS_DATA

class TestPortScorecardClientMock:
    """Tests for the Port Scorecard Client functionality using mocks."""

    @pytest.mark.asyncio
    async def test_get_scorecards_mock(self, mock_client):
        """Test getting all scorecards with mocked data."""
        print("\nTesting get_scorecards with mock data")
        
        # Get scorecards with mocked data
        scorecard_list = await mock_client.get_all_scorecards()
        
        # Validate the response
        assert isinstance(scorecard_list, PortScorecardList)
        assert isinstance(scorecard_list.scorecards, list)
        assert len(scorecard_list.scorecards) == len(MOCK_SCORECARDS_DATA)
        
        # Validate each scorecard
        for i, scorecard in enumerate(scorecard_list.scorecards):
            mock_scorecard = MOCK_SCORECARDS_DATA[i]
            assert isinstance(scorecard, PortScorecard)
            assert scorecard.identifier == mock_scorecard["identifier"]
            assert scorecard.title == mock_scorecard["title"]
            assert scorecard.blueprint == mock_scorecard["blueprint"]
            
            # Check rules if present
            if "rules" in mock_scorecard:
                assert len(scorecard.rules) == len(mock_scorecard["rules"])
            
            # Check levels if present
            if "levels" in mock_scorecard:
                assert len(scorecard.levels) == len(mock_scorecard["levels"])

    @pytest.mark.asyncio
    async def test_get_scorecard_mock(self, mock_client):
        """Test getting a specific scorecard by identifier with mocked data."""
        # Test getting each scorecard from our mock data
        for mock_scorecard in MOCK_SCORECARDS_DATA:
            scorecard_id = mock_scorecard["identifier"]
            blueprint_id = mock_scorecard["blueprint"]
            print(f"\nTesting get_scorecard with ID: {scorecard_id} and blueprint: {blueprint_id}")
            
            # Get the specific scorecard
            scorecard = await mock_client.get_scorecard_details(scorecard_id, blueprint_id)
            
            # Validate the response
            assert isinstance(scorecard, PortScorecard)
            assert scorecard.identifier == scorecard_id
            assert scorecard.blueprint == blueprint_id
            assert scorecard.title == mock_scorecard["title"]
            
            # Check rules if present
            if "rules" in mock_scorecard:
                assert len(scorecard.rules) == len(mock_scorecard["rules"])
                
                # Validate the first rule if available
                if mock_scorecard["rules"]:
                    first_mock_rule = mock_scorecard["rules"][0]
                    first_actual_rule = scorecard.rules[0]
                    assert first_actual_rule["identifier"] == first_mock_rule["identifier"]
                    assert first_actual_rule["title"] == first_mock_rule["title"]
            
            # Check levels if present
            if "levels" in mock_scorecard:
                assert len(scorecard.levels) == len(mock_scorecard["levels"])
                
                # Validate the first level if available
                if mock_scorecard["levels"]:
                    first_mock_level = mock_scorecard["levels"][0]
                    first_actual_level = scorecard.levels[0]
                    assert first_actual_level["title"] == first_mock_level["title"]
                    assert first_actual_level["color"] == first_mock_level["color"]
    
    @pytest.mark.asyncio
    async def test_create_and_delete_scorecard_mock(self, mock_client):
        """Test creating a new scorecard and then deleting it with mocked data."""
        print("\nTesting create_and_delete_scorecard with mock data")
        
        # Define a test blueprint ID
        test_blueprint_id = "test_blueprint"
        
        # Create a test scorecard data
        test_scorecard_data = {
            "identifier": "test_scorecard_mock",
            "title": "Test Scorecard Mock",
            "rules": [
                {
                    "identifier": "test_rule_mock",
                    "title": "Test Rule for Mock",
                    "description": "A test rule for mock testing",
                    "level": "Silver",  # Associate rules with non-base levels
                    "query": {
                        "combinator": "and",
                        "conditions": [
                            {
                                "property": "status",
                                "operator": "=",
                                "value": "active"
                            }
                        ]
                    }
                }
            ],
            "levels": [
                {
                    "title": "Basic",  # Base level (no rules)
                    "color": "blue"
                },
                {
                    "title": "Silver",
                    "color": "silver"
                },
                {
                    "title": "Gold",
                    "color": "gold"
                }
            ]
        }
        
        # Create the scorecard
        created_scorecard = await mock_client.create_new_scorecard(test_blueprint_id, test_scorecard_data)
        
        # Validate the response
        assert isinstance(created_scorecard, PortScorecard)
        assert created_scorecard.identifier == "test_scorecard_mock"
        assert created_scorecard.title == "Test Scorecard Mock"
        assert len(created_scorecard.rules) == 1
        assert len(created_scorecard.levels) == 3
        
        # We need to add the test scorecard to our mock data for deletion to work
        from .fixtures.scorecards import MOCK_SCORECARDS_DATA
        
        # Create a proper mock scorecard entry
        mock_scorecard_entry = {
            "identifier": "test_scorecard_mock",
            "title": "Test Scorecard Mock",
            "blueprint": test_blueprint_id,
            "rules": test_scorecard_data["rules"],
            "levels": test_scorecard_data["levels"],
        }
        
        # Add it to the mock data
        MOCK_SCORECARDS_DATA.append(mock_scorecard_entry)
        
        try:
            # Delete the scorecard
            deletion_result = await mock_client.delete_scorecard("test_scorecard_mock", test_blueprint_id)
            assert deletion_result is True
        finally:
            # Clean up mock data
            MOCK_SCORECARDS_DATA.remove(mock_scorecard_entry) 