Feature: Google Search
  As a user
  I want to search for "<Search>" on Google
  So that I can see the search results page

  Scenario Outline: Searching for "<Search>" on Google
    Given I am on the DuckDuckGo homepage
    When I search for "<Search>" and enter the first result
    When I navigate to the "<Section>" section
    Then I should see a list of available programs

  Examples:
  | Search          | Section           |
  | ITESO           | Carreras          |
  | ITESO           | Posgrados         |
  | ITESO           | Prepa             |
  | Tec de monterrey| Campus profesional|
  | UVM             | Carreras          |
