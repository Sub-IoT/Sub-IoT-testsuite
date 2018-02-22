Feature: Access Classes

# continuous FG scanning (Tsched == 0) is already tested in the QoS or channel configurations, we will skip this here

Scenario: Node performing background scan is accessible
    Given an access profile with one subband which has a scan automation period
    And a testdevice using this access profile
    And a DUT, using this access profile
    When the testdevice executes a command forwarded to the D7ASP interface using this access class
    Then the responder should receive this command
