Feature: Queries

Scenario: When predicate of Break Query action fails all subsequent actions are dropped
    Given a command containing a Break Query action, which results in a fail, and a Read action
    When the testdevice executes the command
    Then the command executes successfully
    And the Read action does not return a result

Scenario: When predicate of Break Query action succeeds all subsequent actions are executed
    Given a command containing a Break Query action, which results in a success, and a Read action
    When the testdevice executes the command
    Then the command executes successfully
    And the Read action does return a result
