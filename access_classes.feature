Feature: Access Classes

# continuous FG scanning (Tsched == 0) is already tested in the QoS or channel configurations, we will skip this here

Scenario: Node performing background scan is accessible
    Given an access profile with one subband which has a scan automation period
    And an access profile with one subband which does not have a scan automation period
    And a testdevice configured with these access profiles, and using access class with the second access profile
    And a DUT, configured with these access profiles, and with active class referring to the first access profile
    When the testdevice executes a command forwarded to the D7ASP interface using the access class referring to the first access profile
    Then the responder should receive this command

# TODO use only one AP? (thus both are scanning)