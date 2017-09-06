Feature: Channel configurations

Scenario: Communication using 868, normal rate, channel index 0
    Given a channel configuration using 868 band, normal rate and channel index 0
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration


Scenario: Communication using 868, normal rate, channel index 270
    Given a channel configuration using 868 band, normal rate and channel index 270
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration

Scenario: Communication using 868, hi rate, channel index 0
    Given a channel configuration using 868 band, hi rate and channel index 0
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration


Scenario: Communication using 868, hi rate, channel index 270
    Given a channel configuration using 868 band, hi rate and channel index 270
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration

Scenario: Communication using 868, lo rate, channel index 0
    Given a channel configuration using 868 band, lo rate and channel index 0
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration


Scenario: Communication using 868, lo rate, channel index 279
    Given a channel configuration using 868 band, lo rate and channel index 279
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration