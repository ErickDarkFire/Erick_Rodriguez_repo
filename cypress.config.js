const { defineConfig } = require("cypress");
const createBundler = require("@bahmutov/cypress-esbuild-preprocessor");

module.exports = defineConfig({
  e2e: {
    chromeWebSecurity: false, // Vital para navegar del buscador al Tec/CUCBA
    defaultCommandTimeout: 10000,
    specPattern: "cypress/e2e/**/*.feature",
    allowCypressEnv: true,
    async setupNodeEvents(on, config) {
      // 1. Importación dinámica de los módulos
      const preprocessor = await import("@badeball/cypress-cucumber-preprocessor");
      const esbuild = await import("@badeball/cypress-cucumber-preprocessor/esbuild");

      // 2. Usamos el nombre EXACTO que apareció en tu terminal
      // Notarás que es "Preprocessor" y no "Transformer"
      const addPlugin = preprocessor.addCucumberPreprocessorPlugin;
      const createEsbuild = esbuild.createEsbuildPlugin;

      // 3. Registro del plugin
      await addPlugin(on, config);

      on(
        "file:preprocessor",
        createBundler({
          plugins: [createEsbuild(config)],
        })
      );

      return config;
    },
  },
});
