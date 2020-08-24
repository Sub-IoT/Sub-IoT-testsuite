Feature: aes

@aes
Scenario: Send and receive an unencrypted message
  Given a default access class
  And a requester, set to default access class
  And a responder, listening for foreground packets on the default access class
  And an interface configuration using the default scan access class and using no encryption
  And a command, direct forward using this interface configuration
  When the requester starts a session for this command
  Then the responder should receive an unsolicited response


@aes
Scenario: Send and receive an encrypted message using aes ctr with same keys
  Given a default access class
  And a requester, set to default access class
  And a responder, listening for foreground packets on the default access class
  And a key, randomly generated
  And the generated key written to the requester
  And the generated key also written to the responder
  And an interface configuration using the default scan access class and using AES CTR
  And a command, direct forward using this interface configuration
  When the requester starts a session for this command
  Then the responder should receive an unsolicited response


@aes
Scenario: Send and not receive an encrypted message using aes ctr with different keys
  Given a default access class
  And a requester, set to default access class
  And a responder, listening for foreground packets on the default access class
  And a key, randomly generated
  And the generated key written to the requester
  And a key, different from the other one
  And the different key written to the responder
  And an interface configuration using the default scan access class and using AES CTR
  And a command, direct forward using this interface configuration
  When the requester starts a session for this command
  Then the responder should not receive an unsolicited response

@aes
Scenario: Send and receive an encrypted message using aes cbc with same keys
  Given a default access class
  And a requester, set to default access class
  And a responder, listening for foreground packets on the default access class
  And a key, randomly generated
  And the generated key written to the requester
  And the generated key also written to the responder
  And an interface configuration using the default scan access class and using AES CBC
  And a command, direct forward using this interface configuration
  When the requester starts a session for this command
  Then the responder should receive an unsolicited response


@aes
Scenario: Send and not receive an encrypted message using aes cbc with different keys
  Given a default access class
  And a requester, set to default access class
  And a responder, listening for foreground packets on the default access class
  And a key, randomly generated
  And the generated key written to the requester
  And a key, different from the other one
  And the different key written to the responder
  And an interface configuration using the default scan access class and using AES CBC
  And a command, direct forward using this interface configuration
  When the requester starts a session for this command
  Then the responder should not receive an unsolicited response


@aes
Scenario: Send and receive an encrypted message using aes ccm with same keys
  Given a default access class
  And a requester, set to default access class
  And a responder, listening for foreground packets on the default access class
  And a key, randomly generated
  And the generated key written to the requester
  And the generated key also written to the responder
  And an interface configuration using the default scan access class and using AES CCM
  And a command, direct forward using this interface configuration
  When the requester starts a session for this command
  Then the responder should receive an unsolicited response


@aes
Scenario: Send and not receive an encrypted message using aes ccm with different keys
  Given a default access class
  And a requester, set to default access class
  And a responder, listening for foreground packets on the default access class
  And a key, randomly generated
  And the generated key written to the requester
  And a key, different from the other one
  And the different key written to the responder
  And an interface configuration using the default scan access class and using AES CCM
  And a command, direct forward using this interface configuration
  When the requester starts a session for this command
  Then the responder should not receive an unsolicited response

