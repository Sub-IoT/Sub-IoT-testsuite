Feature: Access Classes

# continuous FG scanning (Tsched == 0) is already tested in the QoS or channel configurations, we will skip this here

@wip @loop
Scenario: Node performing background scan is accessible
    Given an access profile using <channel_class> channel class <coding> coding with one subband which has a scan automation period of <tsched>
    And a testdevice using this access profile
    And a DUT, using this access profile
    When the testdevice executes a query (in a loop), forwarded to the D7ASP interface using this access class
    Then the requester should receive the responses

    Examples: example1
    | channel_class | coding | tsched  |
    | lo            | PN9    | 1024    |
    | lo            | FEC    | 1024    |
    | lo            | PN9    | 512     |
    | lo            | FEC    | 512     |
    | normal        | PN9    | 1024    |
    | normal        | FEC    | 1024    |
    | normal        | PN9    | 512     |
    | normal        | FEC    | 512     |
    #| hi            | PN9    | 1024    |
    #| hi            | FEC    | 1024    |
    #| hi            | PN9    | 512     |
    #| hi            | FEC    | 512     |