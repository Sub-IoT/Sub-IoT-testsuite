Feature: Dormant session

@wip
Scenario: Registering a dormant session for a requester which does unicast requests
    Given a requester, which does not scan
    And a responder, continuously listening for foreground packets
    And a dormant session registered at the responder for the UID of the requester
    When the requester starts a unicast session to the responder
    Then the requester's session should complete successfully
    And the responder should receive an unsolicited response
    And the requester should receive the dormant session
    And the responders's dormant session should complete successfully

