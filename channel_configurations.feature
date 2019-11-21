Feature: Channel configurations

Scenario: Communication using 868, normal rate class, channel index 0
    Given a channel configuration using 868 band, normal rate class and channel index 0
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration
    And there should be no reboots

Scenario: Communication using 868, normal rate class, channel index 270
    Given a channel configuration using 868 band, normal rate class and channel index 270
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration
    And there should be no reboots

Scenario: Communication using 868, hi rate class, channel index 0
    Given a channel configuration using 868 band, hi rate class and channel index 0
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration
    And there should be no reboots


Scenario: Communication using 868, hi rate class, channel index 270
    Given a channel configuration using 868 band, hi rate class and channel index 270
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration
    And there should be no reboots

Scenario: Communication using 868, lo rate class, channel index 0
    Given a channel configuration using 868 band, lo rate class and channel index 0
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration
    And there should be no reboots


Scenario: Communication using 868, lo rate class, channel index 279
    Given a channel configuration using 868 band, lo rate class and channel index 279
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration
    And there should be no reboots

@band433
Scenario: Communication using 433, normal rate class, channel index 0
    Given a channel configuration using 433 band, normal rate class and channel index 0
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration
    And there should be no reboots

@band915
Scenario: Communication using 915, normal rate class, channel index 0
    Given a channel configuration using 915 band, normal rate class and channel index 0
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration
    And there should be no reboots

@lora
Scenario: Communication using 868, lora class, channel index 0
    Given a channel configuration using 868 band, lora class and channel index 0
    And a testdevice using an access profile based on this channel configuration
    And a DUT, using an access profile based on this channel configuration and listening for foreground packets
    When the testdevice executes a command forwarded to the D7ASP interface using this access profile
    Then the responder should receive this command on the expected channel configuration
    And there should be no reboots