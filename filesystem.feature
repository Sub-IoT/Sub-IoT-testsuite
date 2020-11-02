Feature: Filesystem

Scenario: Creating a user file
    Given a serial modem
    When creating a user file
    Then the new file should be accessible
    And the new file header should be as expected

Scenario: System file is defined, having the correct header and the file data be parsed
    Given a serial modem
    When reading system file <system_file> header and data
    Then the data should be parseable according to system file <system_file>
    And the file permissions of <system_file> should equal <permissions>
    And the properties of <system_file> should be as expected

Examples: example1
    | system_file | permissions |
    | 0           | r--r--      | # UID
    # TODO | 1           | r--r--      | # Factory settings
    # | 2           | r--r--      | # Firmware version
    # TODO | 3           | r--r--      | # Device capacity
    # TODO | 4           | r--r--      | # Device status
    # TODO | 5           | r--r--      | # Engineering mode
    # TODO | 6           | r--r--      | # VID
    # TODO | 8           | r--r--      | # PHY config
    # TODO | 9           | r--r--      | # PHY status
    | 10          | r--r--      | # DLL config
    # TODO | 11          | r--r--      | # DLL status
    # TODO | 12          | r--r--      | # NWL routing
    # TODO | 13          | r--r--      | # NWL security
    # NWL security key is tested separately, since it is not readable
    # TODO | 15          | r--r--      | # NWL security state register
    # TODO | 16          | r--r--      | # NWL status
    # TODO | 17          | r--r--      | # TRL status
    # TODO | 18          | r--r--      | # SEL config
    # TODO | 19          | r--r--      | # FOF status
    # TODO | 23          | r--r--      | # Location data
    | 32          | r--r--      | # AP
    | 33          | r--r--      | # AP
    | 34          | r--r--      | # AP
    | 35          | r--r--      | # AP
    | 36          | r--r--      | # AP
    | 37          | r--r--      | # AP
    | 38          | r--r--      | # AP
    | 39          | r--r--      | # AP
    | 40          | r--r--      | # AP
    | 41          | r--r--      | # AP
    | 42          | r--r--      | # AP
    | 43          | r--r--      | # AP
    | 44          | r--r--      | # AP
    | 45          | r--r--      | # AP
    | 46          | r--r--      | # AP


#TODO test NWL security key
#Scenario: NWL security key file is defined, having the correct header and the file cannot be read
#    Given a serial modem
#    When reading system file <system_file> header and data
#    Then the data should be parseable according to system file <system_file>
#    And the file permissions of <system_file> should equal <permissions>
#    And the properties of <system_file> should be as expected


