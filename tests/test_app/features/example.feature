Feature: Addition

    Scenario: Simple addition between two numbers
        Given the number "1"
        When the number "1" is added to it
        Then the result should be "2"

    Scenario: Tricky addition between three numbers
        Given the number "1"
        And the number "7"
        When the number "6" is added to them
        Then the result should be "14"