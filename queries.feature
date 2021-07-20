Feature: Queries

@queries
Scenario: When predicate of Break Query action fails all subsequent actions are dropped
    Given a command containing a Break Query action, which results in a fail, and a Read action
    When the testdevice executes the command
    Then the command executes successfully
    And the Read action does not return a result

@queries
Scenario: When predicate of Break Query action succeeds all subsequent actions are executed
    Given a command containing a Break Query action, which results in a success, and a Read action
    When the testdevice executes the command
    Then the command executes successfully
    And the Read action does return a result

@queries
Scenario: Validate correct execution of queries with arithmetic comparison
    Given a command containing a query with a <comp_type> comparison comparing a known value with a value which is <value_comparison>, and a Read action
    When the testdevice executes the command
    Then the command executes successfully
    And the Read action does return <result_count> results

    Examples: example1
    | comp_type | value_comparison  | result_count  |
    | >         | bigger            | 0             |
    | >         | equal             | 0             |
    | >         | smaller           | 1             |
    | >=        | bigger            | 0             |
    | >=        | equal             | 1             |
    | >=        | smaller           | 1             |
    | <         | bigger            | 1             |
    | <         | equal             | 0             |
    | <         | smaller           | 0             |
    | <=        | bigger            | 1             |
    | <=        | equal             | 1             |
    | <=        | smaller           | 0             |
    | ==        | bigger            | 0             |
    | ==        | equal             | 1             |
    | ==        | smaller           | 0             |
    | !=        | bigger            | 1             |
    | !=        | equal             | 0             |
    | !=        | smaller           | 1             |