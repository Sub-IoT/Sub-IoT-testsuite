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

@wip
Scenario: The > comparator of a query with arithmetic comparison succeeds with a bigger value
    Given a command containing a query with a > comparison with a value bigger than a known value, and a Read action
    When the testdevice executes the command
    Then the command executes successfully
    And the Read action does return a result

@wip
Scenario: The > comparator of a query with arithmetic comparison fails with a smaller value
    Given a command containing a query with a > comparison with a smaller bigger than a known value, and a Read action
    When the testdevice executes the command
    Then the command executes successfully
    And the Read action does not return a result

@wip
Scenario: The > comparator of a query with arithmetic comparison fails with an equal value
    Given a command containing a query with a > comparison with an a value equal to a known value, and a Read action
    When the testdevice executes the command
    Then the command executes successfully
    And the Read action does not return a result

@wip
Scenario: The >= comparator of a query with arithmetic comparison succeeds with a bigger value
    Given a command containing a query with a >= comparison with a value bigger than a known value, and a Read action
    When the testdevice executes the command
    Then the command executes successfully
    And the Read action does return a result

@wip
Scenario: The >= comparator of a query with arithmetic comparison fails with a smaller value
    Given a command containing a query with a >= comparison with a value smaller than a known value, and a Read action
    When the testdevice executes the command
    Then the command executes successfully
    And the Read action does not return a result

@wip
Scenario: The >= comparator of a query with arithmetic comparison succeeds with an equal value
    Given a command containing a query with a >= comparison with an a value equal to a known value, and a Read action
    When the testdevice executes the command
    Then the command executes successfully
    And the Read action does return a result
