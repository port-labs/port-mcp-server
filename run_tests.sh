#!/bin/bash

# Simple test runner for the Port MCP Server project

function print_help {
    echo "Port MCP Server Test Runner"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help      Show this help message"
    echo "  -a, --all       Run all tests (default)"
    echo "  -u, --unit      Run only unit tests"
    echo "  -i, --integration Run only integration tests"
    echo "  -c, --coverage  Run tests with coverage report"
    echo "  -v, --verbose   Run tests with verbose output"
    echo ""
    echo "Examples:"
    echo "  $0 -u -c        Run unit tests with coverage"
    echo "  $0 -i -v        Run integration tests with verbose output"
}

# Default values
RUN_UNIT=false
RUN_INTEGRATION=false
RUN_COVERAGE=false
VERBOSE=false

# If no arguments, run all tests
if [ $# -eq 0 ]; then
    RUN_UNIT=true
    RUN_INTEGRATION=true
fi

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            print_help
            exit 0
            ;;
        -a|--all)
            RUN_UNIT=true
            RUN_INTEGRATION=true
            shift
            ;;
        -u|--unit)
            RUN_UNIT=true
            shift
            ;;
        -i|--integration)
            RUN_INTEGRATION=true
            shift
            ;;
        -c|--coverage)
            RUN_COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            print_help
            exit 1
            ;;
    esac
done

# Build test command
CMD="python -m pytest"

# Add verbosity
if [ "$VERBOSE" = true ]; then
    CMD="$CMD -v"
else
    CMD="$CMD -q"
fi

# Add coverage
if [ "$RUN_COVERAGE" = true ]; then
    CMD="$CMD --cov=src/mcp_server_port --cov-report=term-missing"
fi

# Add test paths
TEST_PATHS=""
if [ "$RUN_UNIT" = true ] && [ "$RUN_INTEGRATION" = true ]; then
    TEST_PATHS="tests"
elif [ "$RUN_UNIT" = true ]; then
    TEST_PATHS="tests/unit"
elif [ "$RUN_INTEGRATION" = true ]; then
    TEST_PATHS="tests/integration"
fi

# Run tests
echo "Running command: $CMD $TEST_PATHS"
$CMD $TEST_PATHS 