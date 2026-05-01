import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

// Variable para saber en qué universidad estamos (como hacías con context.current_university)
let currentUniversity = "";

Given("I am on the DuckDuckGo homepage", () => {
  cy.visit("https://duckduckgo.com");
});

When("I search for {string} and enter the first result", (searchTerm) => {
  currentUniversity = searchTerm.toLowerCase();

  // Anti-desprendimiento del DOM en DuckDuckGo
  cy.get('#searchbox_input').should('be.visible').type(searchTerm);
  cy.get('#searchbox_input').type('{enter}');

  // Clic forzado al primer resultado
  cy.get('a[data-testid="result-title-a"]', { timeout: 15000 })
    .first()
    .click();
});

When("I navigate to the {string} section", (sectionName) => {
  // LÓGICA PARA EL ITESO
  if (currentUniversity.includes("iteso")) {
    cy.get('body').should('be.visible');
    // Intenta clic en el icono de lupa
    cy.get('#icon-search', { timeout: 10000 }).click({ force: true });
    cy.get('#ipt-search').type(`${sectionName}{enter}`);
  }

  // LÓGICA PARA EL TEC DE MONTERREY
  else if (currentUniversity.includes("tec")) {
    // 1. Abrir el buscador del menú
    cy.get('div.menu-buscador', { timeout: 15000 }).should('be.visible').click();
    // 2. Escribir la sección
    cy.get("input[data-drupal-selector='edit-search']").type(sectionName);
    // 3. Esperar la sugerencia específica (usando el texto de tu Selenium)
    cy.contains('span.autocomplete-suggestion-label', 'Campus Profesional', { timeout: 10000 })
      .click();
  }

  // LÓGICA PARA CUCBA (UdeG)
  else if (currentUniversity.includes("cucba")) {
    cy.scrollTo('top');
    // Drupal ID exacto de tu código Selenium
    cy.get('input#edit-search-block-form--2', { timeout: 15000 })
      .should('be.visible')
      .clear()
      .type(`${sectionName}{enter}`);
  }
});

Then("I should see a list of available programs", () => {
  // Selectores de resultados finales de tu código Selenium
  let selector = "a";
  if (currentUniversity.includes("iteso")) selector = "a.gs-title";
  if (currentUniversity.includes("cucba")) selector = "div.view-content a";

  cy.get(selector, { timeout: 20000 }).first().should('be.visible');
});
