Feature: alp

@alp
Scenario: Using alp to read data using indirect forward
    Given an access class different from the default one
    And a requester, set to default access class but with different access class created
    And a responder, listening for foreground packets on this access class
    And an interface configuration using this access class
    And a file on the requester, containing this interface configuration
    And a command, indirect forwarded to this file
    When the requester starts a session for this command
    Then the responder should receive an unsolicited response
    And the requester should not receive a response

