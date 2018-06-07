Feature: Dormant session

@wip
Scenario: Dormant session succeeds for a requester which does unicast requests
    Given a requester, which does not scan
    And a responder, continuously listening for foreground packets
    And a dormant session registered at the responder for the UID of the requester
    When the requester starts a unicast session to the responder
    Then the requester's session should complete successfully
    And the responder should receive an unsolicited response
    And the requester should receive the dormant session
    And the responders's dormant session should complete successfully

@wip
Scenario: Dormant session fails for a requester which does broadcast requests
    Given a requester, which does not scan
    And a responder, continuously listening for foreground packets
    And a dormant session registered at the responder for the UID of the requester
    When the requester starts a broadcast session to the responder
    Then the requester's session should complete successfully
    And the responder should receive an unsolicited response
    And the requester should not receive the dormant session
    # TODO And the responders's dormant session should not complete successfully

@wip
Scenario: Dormant session times out as expected and fails when no response
    Given a requester, which does not scan
    And a responder, continuously listening for foreground packets
    And a dormant session registered at the responder for the UID of the requester
    When waiting for the dormant session to time out
    Then the responders's dormant session should not complete successfully

@wip
Scenario: Dormant session times out as expected and succeeds on response
    Given a requester, which scans continuously
    And a responder, continuously listening for foreground packets
    And a dormant session registered at the responder for the UID of the requester
    When waiting for the dormant session to time out
    Then the responders's dormant session should complete successfully