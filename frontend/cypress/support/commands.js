// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

// Custom command to wait for API to be ready
Cypress.Commands.add('waitForApi', () => {
  cy.request({
    method: 'GET',
    url: 'http://localhost:5000/api/health',
    failOnStatusCode: false,
  }).then((response) => {
    if (response.status !== 200) {
      cy.wait(1000)
      cy.waitForApi()
    }
  })
})

