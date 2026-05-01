// ***********************************************************
// This example support/e2e.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'

chromeWebSecurity: false

// Este código evita que Cypress falle el test si la página web
// (como la del Tec o CUCBA) tiene errores internos de JavaScript.
Cypress.on('uncaught:exception', (err, runnable) => {
  // Retornar false impide que Cypress detenga el test
  return false;
});
