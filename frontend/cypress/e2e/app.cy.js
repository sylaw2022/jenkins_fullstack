describe('Jenkins Fullstack App E2E Tests', () => {
  beforeEach(() => {
    // Visit the app
    cy.visit('/')
  })

  it('should display the main header', () => {
    cy.contains('h1', 'Jenkins Fullstack Application').should('be.visible')
    cy.contains('p', 'Deployed with Jenkins CI/CD & Render.com').should('be.visible')
  })

  it('should check API health status', () => {
    // Wait for health check to complete
    cy.contains('API Health Status', { timeout: 10000 }).should('be.visible')
    
    // Check for success status
    cy.contains('ok', { matchCase: false }).should('be.visible')
  })

  it('should display backend message', () => {
    cy.contains('Backend Message').should('be.visible')
    cy.contains('Hello from the backend API', { timeout: 10000 }).should('be.visible')
  })

  it('should submit data form successfully', () => {
    const testName = 'Cypress Test User'
    const testMessage = 'This is a test message from Cypress'

    // Fill in the form
    cy.get('input[id="name"]').type(testName)
    cy.get('textarea[id="message"]').type(testMessage)

    // Submit the form
    cy.get('button[type="submit"]').click()

    // Wait for success message
    cy.contains('Success', { timeout: 10000 }).should('be.visible')
    cy.contains(testName).should('be.visible')
    cy.contains(testMessage).should('be.visible')
  })

  it('should validate required form fields', () => {
    // Try to submit empty form
    cy.get('button[type="submit"]').click()

    // HTML5 validation should prevent submission
    cy.get('input[id="name"]:invalid').should('exist')
    cy.get('textarea[id="message"]:invalid').should('exist')
  })

  it('should handle form submission with minimal data', () => {
    // Fill only name
    cy.get('input[id="name"]').type('Test User')
    cy.get('textarea[id="message"]').type('Test')

    // Submit
    cy.get('button[type="submit"]').click()

    // Should show success
    cy.contains('Success', { timeout: 10000 }).should('be.visible')
  })

  it('should be responsive on mobile viewport', () => {
    cy.viewport('iphone-x')
    cy.contains('Jenkins Fullstack Application').should('be.visible')
    cy.get('input[id="name"]').should('be.visible')
  })
})

