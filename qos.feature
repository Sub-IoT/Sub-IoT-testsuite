Feature: QoS

Scenario: Using QoS with response mode No
    Given a requester
    And a responder, listening for foreground packets
    And an interface configuration with QoS response mode is no
    And a command, forwarded to this interface, which does not require response data
    When the requester starts a session for this command
    Then the responder should receive an unsolicited response
    And the requester should not receive a response
    And the requester's session should complete successfully

#Scenario: Using QoS with response mode No with response data
#    Given a requester
#    And a responder, listening for foreground packets
#    And an interface configuration with QoS response mode is no
#    And a command, forwarded to this interface, which does require response data
#    When the requester starts a session for this command
# TODO this should return an error and the packet should not be transmitted. Stack currently asserts on this


Scenario: Using QoS with response mode Any without response data
    Given a requester
    And a responder, listening for foreground packets
    And an interface configuration with QoS response mode is any
    And a command, forwarded to this interface, which does not require response data
    When the requester starts a session for this command
    Then the responder should receive an unsolicited response
    And the requester should receive a response
    And the requester's session should complete successfully


Scenario: Using QoS with response mode Any with response data
    Given a requester
    And a responder, listening for foreground packets
    And an interface configuration with QoS response mode is any
    And a command, forwarded to this interface, which does require response data
    When the requester starts a session for this command
    Then the requester should receive a response
    And the requester's session should complete successfully