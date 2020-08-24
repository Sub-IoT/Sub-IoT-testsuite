Feature: alp

@alp
Scenario: Using alp to return data using indirect forward
    Given a default access class
    And an access class different from the default one
    And a requester, set to default access class
    And on the requester, create different access class
    And a responder, listening for foreground packets on this access class
    And an interface configuration using this access class
    And a file on the requester, containing this interface configuration
    And a command, indirect forwarded to this file
    When the requester starts a session for this command
    Then the responder should receive an unsolicited response
    And the requester should not receive a response

@alp
Scenario: Using alp to return data using direct forward
    Given a default access class
    And an access class different from the default one
    And a requester, set to default access class
    And on the requester, create different access class
    And a responder, listening for foreground packets on this access class
    And an interface configuration using this access class
    And a command, direct forward using this interface configuration
    When the requester starts a session for this command
    Then the responder should receive an unsolicited response
    And the requester should not receive a response

@alp
Scenario: Using alp to return data when break query succeeds
    Given a default access class
    And a requester, set to default access class
    And a responder, listening for foreground packets on the default access class
    And a file on the requester, containing a predefined byte
    And an interface configuration using this default access class
    And a command, with a break query and a forward using this default interface configuration
    When the requester starts a session for this command
    Then the responder should receive an unsolicited response
    And the requester should not receive a response

@alp
Scenario: Using alp to not return data when break query fails
    Given a default access class
    And a requester, set to default access class
    And a responder, listening for foreground packets on the default access class
    And a file on the requester, not containing a predefined byte
    And an interface configuration using this default access class
    And a command, with a break query and a forward using this default interface configuration
    When the requester starts a session for this command
    Then the responder should not receive an unsolicited response
    And the requester should not receive a response

Scenario: Node performing continuous scan will receive message encoded message larger than 255 bytes
    Given a default access class
    And a requester, set to default access class
    And a responder, listening for foreground packets on the default access class
    And an interface configuration using this default access class
    And a command, with FEC encoding longer than 255 bytes
    When the requester starts a session for this command
    Then the responder should receive an unsolicited response
    And the requester should not receive a response


